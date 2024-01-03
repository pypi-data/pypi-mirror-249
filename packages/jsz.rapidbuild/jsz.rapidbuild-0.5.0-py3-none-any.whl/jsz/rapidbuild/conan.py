from __future__ import annotations

from typing import Any
import importlib.resources
import fs
import os.path
import json

from . import base
from . import conan_generator


class SystemConfigManifestProviderConan(base.SystemConfigManifestProvider):
    TOOLCHAIN_MANIFEST_FILENAME = "toolchain_gen.json"
    THIRD_PARTY_MANIFEST_FILENAME = "third_party_gen.json"

    IMPORTS_BIN_DIRNAME = "imports_bin"
    IMPORTS_LIB_DIRNAME = "imports_lib"

    SUPPORTED_CONAN_BUILD_TYPES = [
        "Debug",
        "Release"
    ]

    def __init__(self, *, logger, process_runner, conanfile_path, execute_conan, base_to_conan_build_type):
        self.logger = logger
        self.process_runner = process_runner
        self.conanfile_path = conanfile_path
        self.execute_conan = execute_conan
        self.base_to_conan_build_type = base_to_conan_build_type

        for build_type, conan_build_type in self.base_to_conan_build_type.items():
            if conan_build_type not in self.SUPPORTED_CONAN_BUILD_TYPES:
                raise RuntimeError(f"Unsupported conan build type '{conan_build_type}'")

        self.third_party_manifest: dict[str, Any] = {}
        self.toolchains_manifest: dict[str, Any] = {}

    @staticmethod
    def get_install_dir_name(build_type: str) -> str:
        return f"install-{build_type}"

    def run(self, working_dir_abs_path, build_types):

        for build_type in build_types:
            if build_type not in self.base_to_conan_build_type.keys():
                raise RuntimeError(f"Unsupported build type '{build_type}'")

        conan_export_invocation = []
        conan_export_resource = ""

        for resource in importlib.resources.contents(conan_generator):
            if resource == "conanfile.py":
                with importlib.resources.path(conan_generator, resource) as conan_generator_path:
                    conan_export_resource = resource
                    conan_export_invocation = ["conan", "export", f"{conan_generator_path}"]
                break

        if conan_export_resource == "":
            raise RuntimeError("Internal error: unable to find Conan generator resource.")

        conan_install_invocations = []
        conan_install_build_types = []

        # Run toolchain discovery process (in the generator) only for a single build type.
        toolchains_discovery_requested_for_build_type = None
        
        for build_type in build_types:
            install_dir_abs_path = fs.path.join(working_dir_abs_path, self.get_install_dir_name(build_type))

            request_discovery = False
            if toolchains_discovery_requested_for_build_type is None:
                request_discovery = True
                toolchains_discovery_requested_for_build_type = build_type

            argv = [
                "conan", "install",
                "-s", f"build_type={self.base_to_conan_build_type[build_type]}",
                "-o", f"development={request_discovery}",
                f"--install-folder={install_dir_abs_path}",
                "--build=missing",
                f"{self.conanfile_path}"
            ]

            conan_install_invocations.append(argv)
            conan_install_build_types.append(build_type)

        if self.execute_conan:
            env = os.environ.copy()
            # env["CONAN_USER_HOME"] = fs.path.join(working_dir_abs_path, "conan_home")
            env["CONAN_ERROR_ON_OVERRIDE"] = "True"

            with importlib.resources.path(conan_generator, conan_export_resource) as conan_generator_path:
                self.logger.log_info("Invoking: {}".format(" ".join(conan_export_invocation)))
                self.process_runner.run(conan_export_invocation, env=env, check=True)

            for args in conan_install_invocations:
                self.logger.log_info("Invoking: {}".format(" ".join(args)))
                self.process_runner.run(args, env=env, check=True)

        with fs.open_fs(working_dir_abs_path) as work_fs:

            for build_type in conan_install_build_types:
                install_dir_name = self.get_install_dir_name(build_type)

                if build_type == toolchains_discovery_requested_for_build_type:
                    path = fs.path.join(install_dir_name, self.TOOLCHAIN_MANIFEST_FILENAME)
                    if not work_fs.exists(path):
                        raise RuntimeError(f"Expected generated file '{path}' does not exist.")

                path = fs.path.join(install_dir_name, self.THIRD_PARTY_MANIFEST_FILENAME)
                if not work_fs.exists(path):
                    raise RuntimeError(f"Expected generated file '{path}' does not exist.")

            for build_type in conan_install_build_types:
                install_dir_name = self.get_install_dir_name(build_type)

                if build_type == toolchains_discovery_requested_for_build_type:
                    toolchains_manifest_path = fs.path.join(install_dir_name, self.TOOLCHAIN_MANIFEST_FILENAME)
                    with work_fs.open(toolchains_manifest_path, "r") as f:
                        manifest = json.load(f)

                    for k, v in manifest.items():
                        if k not in self.toolchains_manifest.keys():
                            self.toolchains_manifest[k] = v

                # Gathe per-package 'imports' - dlls and dylibs required at runtime.
                package_dlls = {}

                for file in work_fs.glob(fs.path.join(install_dir_name, self.IMPORTS_BIN_DIRNAME, "*", "*.dll")):
                    abs_path = fs.path.join(working_dir_abs_path, fs.path.relpath(file.path))
                    package_name = fs.path.parts(file.path)[-2]
                    if package_name not in package_dlls:
                        package_dlls[package_name] = [abs_path]
                    else:
                        package_dlls[package_name].append(abs_path)

                for file in work_fs.glob(fs.path.join(install_dir_name, self.IMPORTS_LIB_DIRNAME, "*", "*.dylib")):
                    abs_path = fs.path.join(working_dir_abs_path, fs.path.relpath(file.path))
                    package_name = fs.path.parts(file.path)[-2]
                    if package_name not in package_dlls:
                        package_dlls[package_name] = [abs_path]
                    else:
                        package_dlls[package_name].append(abs_path)

                third_party_manifest_path = fs.path.join(install_dir_name, self.THIRD_PARTY_MANIFEST_FILENAME)
                with work_fs.open(third_party_manifest_path, "r") as f:
                    manifest = json.load(f)

                    for package_name in manifest.keys():
                        manifest[package_name]["load_time_libs"] = []

                    for package_name, paths in package_dlls.items():
                        manifest[package_name]["load_time_libs"] = paths

                    for k, v in manifest.items():
                        iface_key = base.build_target_key(k, base.TOOLCHAIN_DEFAULT, build_type)
                        assert (iface_key not in self.third_party_manifest.keys())
                        self.third_party_manifest[iface_key] = v

            with work_fs.open("debug_third_party_manifest.json", "w") as f:
                f.write(json.dumps(self.third_party_manifest, indent=4))

    def get_toolchains_manifest(self):
        return self.toolchains_manifest

    def get_third_party_manifest(self):

        third_party_manifest_2 = {}
        for k, v in self.third_party_manifest.items():
            third_party_manifest_2[k] = base.ThirdPartyTargetInterface.from_dict(v)

        return third_party_manifest_2
