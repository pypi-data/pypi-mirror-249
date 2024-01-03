from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum, auto

import fs
import fs.errors

import bentoudev.dataclass.yaml_loader as yaml_loader

from . import base
from .compiler_base import (
    CompilerSettings,
    CompilerArgFormatter,
    _get_default_compiler_settings,
)
from .compiler_msvc import (
    CompilerArgFormatterMSVC,
    CompilerArgFormatterClangCL,
)
from .compiler_llvm import (
    CompilerArgFormatterGCC,
    CompilerArgFormatterClang
)
from .librarian_msvc import (
    LibrarianArgFormatterMSVC
)
from .librarian_llvm import (
    LibrarianArgFormatterGCC,
    LibrarianArgFormatterLLVM
)
from .linker_base import (
    LinkerSettings,
    _get_default_linker_settings
)
from .linker_msvc import (
    LinkerArgFormatterLink,
    LinkerArgFormatterLLDLink,
)
from .linker_llvm import (
    LinkerArgFormatterLDLLD,
    LinkerArgFormatterLD
)


class ToolchainSettingsWindowsDefault(base.ToolchainSettings):
    def get_build_types(self) -> set[str]:
        return {base.BUILD_TYPE_DEBUG, base.BUILD_TYPE_PROFILING, base.BUILD_TYPE_RELEASE}

    def get_compiler_settings(self, build_type: str) -> CompilerSettings:
        return _get_default_compiler_settings(build_type)

    def get_compiler_definitions(self, build_type: str) -> dict[str, base.Any]:
        return {}

    def get_linker_settings(self, build_type: str) -> LinkerSettings:
        return _get_default_linker_settings(build_type)


class ToolchainSettingsProviderHardcoded(base.ToolchainSettingsProvider):
    def __init__(self):
        self.d = {
            base.TOOLCHAIN_VS16_MSVC: ToolchainSettingsWindowsDefault(),
            base.TOOLCHAIN_VS17_MSVC: ToolchainSettingsWindowsDefault(),
            base.TOOLCHAIN_VS16_LLVM13: ToolchainSettingsWindowsDefault(),
            base.TOOLCHAIN_VS17_LLVM13: ToolchainSettingsWindowsDefault(),
        }

    def get_toolchain_settings(self, toolchain_name) -> base.ToolchainSettings:
        try:
            return self.d[toolchain_name]
        except KeyError:
            raise NotImplementedError()

    def get_toolchains(self) -> set[str]:
        return set(self.d.keys())


@dataclass
class ToolchainBuildTypeSettings:
    compiler_settings: CompilerSettings = field(default_factory=CompilerSettings)
    compiler_defs: dict[str, base.Any] = field(default_factory=dict)
    linker_settings: LinkerSettings = field(default_factory=LinkerSettings)


@dataclass
class ToolchainSettingsData(base.ToolchainSettings):
    build_types: dict[str, ToolchainBuildTypeSettings] = field(default_factory=dict)

    def _get_build_type(self, build_type: str) -> ToolchainBuildTypeSettings:
        try:
            return self.build_types[build_type]
        except KeyError:
            raise NotImplementedError()

    def get_build_types(self) -> set[str]:
        return set(self.build_types.keys())

    def get_compiler_settings(self, build_type: str) -> CompilerSettings:
        return self._get_build_type(build_type).compiler_settings

    def get_compiler_definitions(self, build_type: str) -> dict[str, base.Any]:
        return self._get_build_type(build_type).compiler_defs

    def get_linker_settings(self, build_type: str) -> LinkerSettings:
        return self._get_build_type(build_type).linker_settings


class ToolchainSettingsDeserializer(ABC):
    @abstractmethod
    def deserialize(self) -> ToolchainSettingsData | None:
        pass


class ToolchainSettingsSettingsDeserializerFromFile(ToolchainSettingsDeserializer):
    def __init__(self, *, wks_fs, path, logger):
        self.fs = wks_fs
        self.file_path = path
        self.logger = logger

    def deserialize(self) -> ToolchainSettingsData | None:
        file_contents = ""
        try:
            with self.fs.open(self.file_path, 'r') as f:
                file_contents = f.read()
        except fs.errors.ResourceNotFound:
            self.logger.log_error(f"File '{self.file_path}' does not exist.")
            return None

        try:
            settings = yaml_loader.load_yaml_dataclass(
                ToolchainSettingsData, fs.path.basename(self.file_path), file_contents)
            if settings is None:
                self.logger.log_error(f"File '{self.file_path}' is not a valid yaml file.")
            return settings
        except yaml_loader.DataclassLoadError as err:
            self.logger.log_error(f"File '{self.file_path}':\n{str(err)}.")
            return None


class ToolchainSettingsDeseralizeError(RuntimeError):
    pass


class ToolchainSettingsProviderFromFile(base.ToolchainSettingsProvider):
    def __init__(self, wks_fs, path, logger):
        self.deserializer = ToolchainSettingsSettingsDeserializerFromFile(wks_fs=wks_fs, path=path, logger=logger)

        self.settings = self.deserializer.deserialize()
        if self.settings is None:
            raise ToolchainSettingsDeseralizeError()

        self.d = {
            base.TOOLCHAIN_VS16_MSVC: self.settings,
            base.TOOLCHAIN_VS17_MSVC: self.settings,
            base.TOOLCHAIN_VS16_LLVM13: self.settings,
            base.TOOLCHAIN_VS17_LLVM13: self.settings,
        }

    def get_toolchain_settings(self, toolchain_name) -> base.ToolchainSettings:
        try:
            return self.d[toolchain_name]
        except KeyError:
            raise NotImplementedError()

    def get_toolchains(self) -> set[str]:
        return set(self.d.keys())


class ToolchainSettingsProviderDefault(base.ToolchainSettingsProvider):
    TOOLCHAIN_SETTINGS_FILE = "toolchain_settings.yml"

    def __init__(self, wks_fs, logger):
        try:
            path = fs.path.join("src", self.TOOLCHAIN_SETTINGS_FILE)
            self.provider = ToolchainSettingsProviderFromFile(wks_fs, path, logger)
            logger.log_info(f"Using toolchain settings from '{path}'.")
        except ToolchainSettingsDeseralizeError:
            self.provider = ToolchainSettingsProviderHardcoded()
            logger.log_info("Using default hardcoded toolchain settings.")

    def get_toolchain_settings(self, toolchain_name) -> base.ToolchainSettings:
        return self.provider.get_toolchain_settings(toolchain_name)

    def get_toolchains(self) -> set[str]:
        return self.provider.get_toolchains()


# noinspection PyArgumentList
class CompilerFamily(Enum):
    MSVC = auto()
    CLANG = auto()
    CLANG_CL = auto()
    GCC = auto()


class CouldNotDetermineCompilerFamily(RuntimeError):
    pass


def guess_compiler_family_from_compiler_path(path: str) -> CompilerFamily:
    filename = Path(path).parts[-1]
    if filename == "cl" or filename == "cl.exe":
        return CompilerFamily.MSVC
    if filename == "clang" or filename == "clang.exe" or filename == "clang++" or filename == "clang++.exe":
        return CompilerFamily.CLANG
    if filename == "clang-cl" or filename == "clang-cl.exe":
        return CompilerFamily.CLANG_CL
    if filename == "gcc":
        return CompilerFamily.GCC
    raise CouldNotDetermineCompilerFamily(f"compiler path: {path}")


def create_compiler_arg_formatter(f: CompilerFamily) -> CompilerArgFormatter:
    return {
        CompilerFamily.MSVC: CompilerArgFormatterMSVC(),
        CompilerFamily.CLANG: CompilerArgFormatterClang(),
        CompilerFamily.CLANG_CL: CompilerArgFormatterClangCL(),
        CompilerFamily.GCC: CompilerArgFormatterGCC()
    }[f]


def get_compiler_system_definitions(f: CompilerFamily, build_type: str):
    defs = {
        base.BUILD_TYPE_MATCH_ALL: {
            "_MT": None,
            "_DLL": None,
        },
        base.BUILD_TYPE_DEBUG: {
            "_DEBUG": None,
        },
        base.BUILD_TYPE_RELEASE: {
        },
        base.BUILD_TYPE_PROFILING: {
        },
    }
    try:
        return defs[base.BUILD_TYPE_MATCH_ALL] | defs[build_type]
    except KeyError:
        raise NotImplementedError()


# noinspection PyArgumentList
class LibrarianFamily(Enum):
    MSVC = auto()
    LLVM = auto()
    GCC = auto()


class CouldNotDetermineLibrarianFamily(RuntimeError):
    pass


def guess_librarian_family_from_path(path: str) -> LibrarianFamily:
    filename = Path(path).parts[-1]
    if filename == "lib" or filename == "lib.exe":
        return LibrarianFamily.MSVC
    if filename == "llvm-ar" or filename == "llvm-ar.exe":
        return LibrarianFamily.LLVM
    if filename == "ar" or filename == "ar.exe":
        return LibrarianFamily.GCC
    raise CouldNotDetermineLibrarianFamily(f"librarian path: {path}")


def create_librarian_arg_formatter(f: LibrarianFamily):
    return {
        LibrarianFamily.MSVC: LibrarianArgFormatterMSVC(),
        LibrarianFamily.LLVM: LibrarianArgFormatterLLVM(),
        LibrarianFamily.GCC: LibrarianArgFormatterGCC(),
    }[f]


# noinspection PyArgumentList
class LinkerFamily(Enum):
    LINK = auto()
    LLD_LINK = auto()
    LD_LLD = auto()
    LD = auto()


class CouldNotDetermineLinkerFamily(RuntimeError):
    pass


def guess_linker_family_from_path(path: str) -> LinkerFamily:
    filename = Path(path).parts[-1]
    if filename == "link" or filename == "link.exe":
        return LinkerFamily.LINK
    if filename == "lld-link" or filename == "lld-link.exe":
        return LinkerFamily.LLD_LINK
    if filename == "ld.lld" or filename == "ld.lld.exe":
        return LinkerFamily.LD_LLD
    if filename == "ld" or filename == "ld.exe":
        return LinkerFamily.LD
    raise CouldNotDetermineLinkerFamily(f"linker path: {path}")


def create_linker_arg_formatter(f: LinkerFamily):
    return {
        LinkerFamily.LINK: LinkerArgFormatterLink(),
        LinkerFamily.LLD_LINK: LinkerArgFormatterLLDLink(),
        LinkerFamily.LD_LLD: LinkerArgFormatterLDLLD(),
        LinkerFamily.LD: LinkerArgFormatterLD()
    }[f]


def get_linker_system_libs(f: LinkerFamily, build_type: str):
    debug_libs = [
        # THE ORDER OF THESE IMPORT LIBS IS IMPORTANT
        # Switching msvcrtd.lib with vcruntimed.lib results in a duplicate symbol error with lld-link.

        # DLL import library for the Debug version of the UCRT (ucrtbased.dll).
        'ucrtd.lib',
        # Static library for the Debug version of the native CRT startup for use with DLL UCRT and vcruntime.
        'msvcrtd.lib',
        # DLL import library for the Debug vcruntime (vcruntime<version>d.dll).
        'vcruntimed.lib',
        # Multithreaded, dynamic link (import library for msvcp<version>d.dll)
        'msvcprtd.lib',
    ]
    release_libs = [
        # DLL import library for the UCRT (ucrtdll).
        'ucrt.lib',
        # Static library for the native CRT startup for use with DLL UCRT and vcruntime.
        'msvcrt.lib',
        # DLL import library for the vcruntime (vcruntime<version>.dll).
        'vcruntime.lib',
        # Multithreaded, dynamic link (import library for msvcp<version>.dll)
        'msvcprt.lib',
    ]
    libs = {
        base.BUILD_TYPE_MATCH_ALL: [
            'kernel32.lib',
            'user32.lib',
            'gdi32.lib',
            'shell32.lib',
            'winspool.lib',
            'ole32.lib',
            'oleaut32.lib',
            'uuid.lib',
            'comdlg32.lib',
            'advapi32.lib',
        ],
        base.BUILD_TYPE_DEBUG: debug_libs,
        base.BUILD_TYPE_RELEASE: release_libs,
        base.BUILD_TYPE_PROFILING: release_libs,
    }
    try:
        return libs[base.BUILD_TYPE_MATCH_ALL] + libs[build_type]
    except KeyError:
        raise NotImplementedError()



