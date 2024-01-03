#!/usr/bin/env
from typing import Any, Union

import bentoudev.dataclass.yaml_loader
import yaml
import os.path
import fs.path
from fs.base import FS
from fs.osfs import OSFS
import fs.errors

from . import base
from .conan import SystemConfigManifestProviderConan
from .fastbuild import BuildScriptEmitterFastbuild
from .target_graph import create_targets_interfaces_and_implementations
from .toolchain import ToolchainSettingsProviderDefault
from .workspace_def import (
    WorkspaceDefinition,
    WorkspaceInvalidFormat,
)


def _validate_third_party_manifest(manifest):
    if not isinstance(manifest, dict):
        return False
    return True


def _validate_toolchains_manifest(manifest, supported_toolchains):
    if not isinstance(manifest, dict):
        return False
    if len(manifest.keys()) == 0:
        return False
    return True


def _validate_toolchains_settings(settings):
    if not isinstance(settings, dict):
        return False
    if len(settings.keys()) == 0:
        return False
    return True


class Workspace:
    def __init__(self, *,
                 name: str,
                 wks_fs: FS,
                 logger: base.Logger,
                 system_config_provider: base.SystemConfigManifestProvider,
                 toolchain_settings_provider: base.ToolchainSettingsProvider,
                 build_script_emitter: base.BuildScriptEmitter
                 ):

        # TODO: sanitize name string: only alphanum + _, no spaces
        self.name = name
        self.fs = wks_fs

        self.configure_dir_name = "configure"
        self.source_dir_name = "src"
        self.build_dir_name = "build"

        self.workspace_def: Union[WorkspaceDefinition, None] = None
        self.third_party_manifest: dict[str, Any] = {}
        self.toolchains_manifest: dict[str, Any] = {}

        self.build_types = [
            base.BUILD_TYPE_DEBUG,
            base.BUILD_TYPE_RELEASE,
            base.BUILD_TYPE_PROFILING
        ]
        self.supported_toolchains = [
            base.TOOLCHAIN_VS16_MSVC,
            base.TOOLCHAIN_VS16_LLVM13,
            base.TOOLCHAIN_VS17_MSVC,
            base.TOOLCHAIN_VS17_LLVM13,
        ]

        self.logger = logger
        self.system_config_provider = system_config_provider
        self.toolchain_settings_provider = toolchain_settings_provider
        self.build_script_emitter = build_script_emitter

    def __del__(self):
        self.fs.close()
        pass

    def _get_source_dir_path(self):
        return self.source_dir_name

    def _get_source_dir_abs_path(self):
        if self.fs.hassyspath(self.source_dir_name):
            return self.fs.getsyspath(self.source_dir_name)
        return f"wks://{self.source_dir_name}"

    def _get_configure_dir_abs_path(self):
        if self.fs.hassyspath(self.configure_dir_name):
            return self.fs.getsyspath(self.configure_dir_name)
        return f"wks://{self.configure_dir_name}"

    def _get_build_dir_abs_path(self):
        if self.fs.hassyspath(self.build_dir_name):
            return self.fs.getsyspath(self.build_dir_name)
        return f"wks://{self.build_dir_name}"

    TARGETS_FILENAME = "rapid_targets.yml"
    USE_BENTOUDEV_LOADER = False # TODO: Current yaml structure is too far off from the code data structures

    def configure(self) -> bool:

        #
        # Load workspace target definitions
        #

        targets_file_path = fs.path.join(self.source_dir_name, self.TARGETS_FILENAME)
        self.logger.log_info(f"Reading workspace definition '{targets_file_path}'...")


        if self.USE_BENTOUDEV_LOADER:
            file_contents = ""
            try:
                with self.fs.open(targets_file_path, 'r') as f:
                    file_contents = f.read()
            except fs.errors.ResourceNotFound:
                self.logger.log_error(f"File '{targets_file_path}' does not exist.")
                return False

            try:
                try:
                    self.workspace_def = bentoudev.dataclass.yaml_loader.load_yaml_dataclass(
                        WorkspaceDefinition, self.TARGETS_FILENAME, file_contents)
                except bentoudev.dataclass.yaml_loader.DataclassLoadError as err:
                    self.logger.log_error(f"Error location line '{err.source.line_number}', column '{err.source.column_number}'.")
                    raise WorkspaceInvalidFormat()
            except WorkspaceInvalidFormat:
                self.logger.log_error(f"File '{targets_file_path}' is not a valid targets definition file.")
                return False

        else:
            try:
                with self.fs.open(targets_file_path, 'r') as f:
                    if not yaml.__with_libyaml__:
                        self.logger.log_info("Warning: using yaml module without C bindings.")
                    targets_defs = yaml.load(f, yaml.SafeLoader)
            except fs.errors.ResourceNotFound:
                self.logger.log_error(f"File '{targets_file_path}' does not exist.")
                return False

            try:
                self.workspace_def = WorkspaceDefinition.from_dict(targets_defs)
            except WorkspaceInvalidFormat:
                self.logger.log_error(f"File '{targets_file_path}' is not a valid targets definition file.")
                return False

        self.logger.log_info("Workspace definition loaded.")

        # print(json.dumps(target_defs, indent=2))

        #
        # Prepare configuration directory, provide manifests
        #
        self.fs.makedir(self.configure_dir_name, recreate=True)

        self.system_config_provider.run(self._get_configure_dir_abs_path(), self.build_types)

        self.third_party_manifest = self.system_config_provider.get_third_party_manifest()

        if not _validate_third_party_manifest(self.third_party_manifest):
            self.logger.log_error("Provided third party manifest is invalid.")
            return False

        self.toolchains_manifest = self.system_config_provider.get_toolchains_manifest()

        if not _validate_toolchains_manifest(self.toolchains_manifest, self.supported_toolchains):
            self.logger.log_error("Provided toolchains manifest is invalid.")
            return False

        manifest_toolchains = self.toolchains_manifest.keys()
        if not set(manifest_toolchains).issubset(self.supported_toolchains):
            self.logger.log_error("Manifest toolchains must be a subset of supported toolchains.")
            self.logger.log_error(f"Toolchains in manifest: {sorted(manifest_toolchains)}")
            self.logger.log_error(f"Supported toolchains: {sorted(self.supported_toolchains)}")
            return False

        settings_toolchains = self.toolchain_settings_provider.get_toolchains()
        if not set(manifest_toolchains).issubset(settings_toolchains):
            self.logger.log_error("Settings must be provided for all toolchains from the toolchain manifest.")
            self.logger.log_error(f"Manifest toolchains: {sorted(list(manifest_toolchains))}")
            self.logger.log_error(f"Toolchains for which settings were provided : {sorted(list(settings_toolchains))}")
            return False

        ok = True
        for toolchain in self.toolchain_settings_provider.get_toolchains():
            settings = self.toolchain_settings_provider.get_toolchain_settings(toolchain)
            if settings.get_build_types() != set(self.build_types):
                self.logger.log_error("Settings for all supported build types must be provided.")
                self.logger.log_error(f"Build types in settings for toolchain {toolchain}: "
                                      f"{sorted(list(settings.get_build_types()))}")
                self.logger.log_error(f"Supported build types: {sorted(self.build_types)}")
                ok = False
        if not ok:
            return False


        #
        # Build targets implementations
        #
        targets_interfaces, targets_impls = create_targets_interfaces_and_implementations(
            self._get_source_dir_abs_path(),
            self.toolchains_manifest.keys(),
            self.build_types,
            self.third_party_manifest,
            self.workspace_def
        )

        assert (isinstance(targets_interfaces, dict))
        assert (isinstance(targets_impls, dict) and len(targets_impls.keys()) != 0)

        #
        # Generate build script for targets based on implementations
        #

        build_script_filename = self.build_script_emitter.filename()
        build_script_contents = self.build_script_emitter.contents(
            self.name,
            self._get_source_dir_abs_path(),
            self._get_configure_dir_abs_path(),
            self._get_build_dir_abs_path(),
            self.toolchains_manifest,
            self.toolchain_settings_provider,
            self.build_types,
            [d.name for d in self.workspace_def.targets],
            targets_impls
        )

        build_script_path = fs.path.join(self.configure_dir_name, build_script_filename)

        self.logger.log_info(f"Writing build script '{build_script_path}'...")
        with self.fs.open(build_script_path, 'w') as f:
            f.write(build_script_contents)

        self.logger.log_info("Configuring done.")
        return True


def open_workspace(wks_dir: str, *, name=None, dev_mode=False) -> Workspace:
    logger = base.LoggerDefault()

    wks_fs = OSFS(os.path.abspath(wks_dir))
    wks_name = name if name is not None else wks_dir

    logger.log_info(f"Opening workspace '{name if name is not None else wks_dir}' (dir: '{wks_dir}')...")

    system_config_provider = SystemConfigManifestProviderConan(
        logger=logger,
        process_runner=base.ProcessRunnerDefault(),
        conanfile_path=wks_fs.getsyspath("conanfile.py"),
        execute_conan=not dev_mode,
        base_to_conan_build_type={
            base.BUILD_TYPE_DEBUG: "Debug",
            base.BUILD_TYPE_RELEASE: "Release",
            base.BUILD_TYPE_PROFILING: "Release",
        }
    )

    toolchain_settings_provider = ToolchainSettingsProviderDefault(wks_fs, logger)

    wks = Workspace(
        name=wks_name,
        wks_fs=wks_fs,
        logger=logger,
        system_config_provider=system_config_provider,
        toolchain_settings_provider=toolchain_settings_provider,
        build_script_emitter=BuildScriptEmitterFastbuild()
    )
    return wks
