from enum import Enum, auto
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any

from . import base


class LanguageStandard(Enum):
    C89 = auto()
    C99 = auto()
    C11 = auto()
    C17 = auto()
    C23 = auto()
    C_LATEST = auto()
    CPP03 = auto()
    CPP11 = auto()
    CPP14 = auto()
    CPP17 = auto()
    CPP20 = auto()
    CPP23 = auto()
    CPP_LATEST = auto()


class UnsupportedSettingError(NotImplementedError):
    pass


class UnsupportedLanguageError(UnsupportedSettingError):
    pass


class LanguageConformance(Enum):
    MIN = auto()
    MAX = auto()


class CompilerWarningState(Enum):
    ENABLE = auto()
    DISABLE = auto()
    REPORT_ONCE = auto()
    TREAT_AS_ERROR = auto()


class CompilerWarningLevel(Enum):
    W0 = auto()
    W1 = auto()
    W2 = auto()
    W3 = auto()
    W4 = auto()
    All = auto()


@dataclass
class CompilerWarningSettings:
    level: CompilerWarningLevel = CompilerWarningLevel.W3
    treat_as_errors: bool = True
    version: str = ""
    warning_states: dict[str, CompilerWarningState] = field(default_factory=dict)


class CompilerFloatBehavior(Enum):
    STRICT = auto()
    PRECISE = auto()
    FAST = auto()


class CompilerOptimizationMode(Enum):
    NONE = auto()
    MINIMIZE_SIZE = auto()
    MAXIMIZE_SPEED = auto()


@dataclass
class CompilerSettings:
    lang_std: LanguageStandard = LanguageStandard.CPP17
    lang_conformance: LanguageConformance = LanguageConformance.MAX
    warning_settings: CompilerWarningSettings = field(default_factory=CompilerWarningSettings)
    enable_rtti: bool = False
    enable_exceptions: bool = False
    float_behavior: CompilerFloatBehavior = CompilerFloatBehavior.PRECISE
    use_debug_runtime: bool = False
    enable_debug_info: bool = False
    optimization_mode: CompilerOptimizationMode = CompilerOptimizationMode.NONE
    enable_security_checks: bool = False


class CompilerArgFormatter(ABC):
    @abstractmethod
    def format_beginning_args(self) -> list[str]:
        pass

    @abstractmethod
    def format_object_compilation_args(self) -> list[str]:
        pass

    @abstractmethod
    def format_debug_info_args(self, output_dir_path: str, output_base_name: str) -> list[str]:
        pass

    @abstractmethod
    def format_pch_creation_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        pass

    @abstractmethod
    def format_pch_usage_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        pass

    @abstractmethod
    def format_definition_compiler_arg(self, name: str, value: Any) -> str:
        pass

    @abstractmethod
    def format_include_dir_arg(self, include_dir: str) -> str:
        pass

    @abstractmethod
    def format_system_include_dir_arg(self, include_dir: str) -> str:
        pass

    @abstractmethod
    def format_settings_args(self, settings: CompilerSettings) -> list[str]:
        pass


def _get_default_compiler_settings(build_type: str) -> CompilerSettings:
    settings = CompilerSettings()
    settings.lang_std = LanguageStandard.CPP17
    settings.lang_conformance = LanguageConformance.MAX

    warn_settings = CompilerWarningSettings()
    warn_settings.level = CompilerWarningLevel.All
    warn_settings.version = "19.33"
    warn_settings.treat_as_errors = True

    # Info: function not inlined
    warn_settings.warning_states["4710"] = CompilerWarningState.DISABLE
    # Info: the compiler performed inlining on the given function, although it was not marked
    # for inlining.
    warn_settings.warning_states["4711"] = CompilerWarningState.DISABLE
    # Compiler will insert Spectre mitigation for memory load if /Qspectre switch specified
    warn_settings.warning_states["5045"] = CompilerWarningState.DISABLE
    # 'struct': '4' bytes padding added after data member 'struct::member'
    warn_settings.warning_states["4820"] = CompilerWarningState.DISABLE

    warn_settings.warning_states["undef"] = CompilerWarningState.DISABLE
    warn_settings.warning_states["reserved-macro-identifier"] = CompilerWarningState.DISABLE
    warn_settings.warning_states["c++98-compat-pedantic"] = CompilerWarningState.DISABLE
    warn_settings.warning_states["newline-eof"] = CompilerWarningState.DISABLE

    settings.warning_settings = warn_settings

    settings.enable_rtti = False
    settings.enable_exceptions = True
    settings.float_behavior = CompilerFloatBehavior.FAST

    if build_type == base.BUILD_TYPE_DEBUG:
        settings.use_debug_runtime = True
        settings.enable_debug_info = True
        settings.optimization_mode = CompilerOptimizationMode.NONE
        settings.enable_security_checks = True
        return settings

    if build_type == base.BUILD_TYPE_RELEASE:
        settings.use_debug_runtime = False
        settings.enable_debug_info = False
        settings.optimization_mode = CompilerOptimizationMode.MAXIMIZE_SPEED
        settings.enable_security_checks = False
        return settings

    if build_type == base.BUILD_TYPE_PROFILING:
        settings = settings
        settings.use_debug_runtime = False
        settings.enable_debug_info = True
        settings.optimization_mode = CompilerOptimizationMode.MAXIMIZE_SPEED
        settings.enable_security_checks = False
        return settings

    raise NotImplementedError()
