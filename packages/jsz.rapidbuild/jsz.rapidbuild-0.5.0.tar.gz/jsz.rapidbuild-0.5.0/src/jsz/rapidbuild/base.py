from abc import ABC, abstractmethod
import sys
import subprocess
import os.path
from enum import Enum, auto
from typing import Any
from dataclasses import dataclass, field

from .compiler_base import (
    CompilerSettings
)

from .linker_base import (
    LinkerSettings
)


def append_unique(list_: list[Any], item: any):
    if item not in list_:
        list_.append(item)


def extend_unique(list_a: list[Any], list_b: list[Any]):
    for item in list_b:
        if item not in list_a:
            list_a.append(item)


def build_target_key(target_name: str, toolchain_name: str, build_type: str):
    return "{}_{}_{}".format(target_name, toolchain_name, build_type)


BUILD_TYPE_MATCH_ALL = "*"
BUILD_TYPE_DEBUG = "debug"
BUILD_TYPE_RELEASE = "release"
BUILD_TYPE_PROFILING = "profiling"

TOOLCHAIN_DEFAULT = "default"
TOOLCHAIN_VS16_MSVC = "vs16_msvc"
TOOLCHAIN_VS16_LLVM13 = "vs16_llvm13"
TOOLCHAIN_VS17_MSVC = "vs17_msvc"
TOOLCHAIN_VS17_LLVM13 = "vs17_llvm13"

OS_WINDOWS = "windows"


class Logger(ABC):
    @abstractmethod
    def log_info(self, *args):
        pass

    @abstractmethod
    def log_error(self, *args):
        pass


class LoggerDefault(Logger):
    def log_info(self, *args):
        print(*args, file=sys.stdout)

    def log_error(self, *args):
        print(*args, file=sys.stderr)


class ProcessRunner(ABC):
    @abstractmethod
    def run(self, args, *, env, check):
        pass


class ProcessRunnerDefault(ProcessRunner):
    def run(self, args, *, env, check):
        subprocess.run(args, env=env, check=check)


class ThirdPartyInvalidFormat(RuntimeError):
    pass


@dataclass
class ThirdPartyTargetInterface:
    include_dirs: list[str] = field(default_factory=list)
    definitions: dict[str, Any] = field(default_factory=list)
    link_libs: list[str] = field(default_factory=list)
    link_libs_dirs: list[str] = field(default_factory=list)
    load_time_libs: list[str] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict):
        if not isinstance(d, dict):
            raise ThirdPartyInvalidFormat()

        if not set(d.keys()).issubset({"include_dirs", "definitions", "link_libs", "link_libs_dirs", "load_time_libs"}):
            raise ThirdPartyInvalidFormat()

        include_dirs = d.get("include_dirs", [])
        if not isinstance(include_dirs, list):
            raise ThirdPartyInvalidFormat()

        definitions = d.get("definitions", {})
        if not isinstance(definitions, dict):
            raise ThirdPartyInvalidFormat()

        link_libs = d.get("link_libs", [])
        if not isinstance(link_libs, list):
            raise ThirdPartyInvalidFormat()

        link_libs_dirs = d.get("link_libs_dirs", [])
        if not isinstance(link_libs_dirs, list):
            raise ThirdPartyInvalidFormat()

        load_time_libs = d.get("load_time_libs", [])
        if not isinstance(load_time_libs, list):
            raise ThirdPartyInvalidFormat()

        return ThirdPartyTargetInterface(include_dirs=include_dirs, definitions=definitions, link_libs=link_libs,
                                         link_libs_dirs=link_libs_dirs, load_time_libs=load_time_libs)


class SystemConfigManifestProvider(ABC):
    @abstractmethod
    def run(self, working_dir_abs_path, build_types):
        pass

    @abstractmethod
    def get_toolchains_manifest(self):
        pass

    @abstractmethod
    def get_third_party_manifest(self):
        pass


class ToolchainSettings(ABC):
    @abstractmethod
    def get_build_types(self) -> set[str]:
        pass

    @abstractmethod
    def get_compiler_settings(self, build_type: str) -> CompilerSettings:
        pass

    @abstractmethod
    def get_compiler_definitions(self, build_type: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_linker_settings(self, build_type: str) -> LinkerSettings:
        pass


class ToolchainSettingsProvider(ABC):
    @abstractmethod
    def get_toolchain_settings(self, toolchain_name) -> ToolchainSettings:
        pass

    @abstractmethod
    def get_toolchains(self) -> set[str]:
        pass


class BuildScriptEmitter(ABC):
    @abstractmethod
    def filename(self):
        pass

    @abstractmethod
    def contents(self, wks_name, source_dir_abs_path, configure_dir_abs_path, build_dir_abs_path,
                 toolchains_manifest, toolchain_settings_provider, build_types, targets_names, targets_impls) -> str:
        pass
