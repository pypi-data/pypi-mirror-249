from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto

from . import base
from .workspace_def import TargetKind


class LinkerWarningState(Enum):
    ENABLE = auto()
    DISABLE = auto()
    TREAT_AS_ERROR = auto()


@dataclass
class LinkerWarningSettings:
    treat_as_errors: bool = True
    warning_states: dict[str, LinkerWarningState] = field(default_factory=dict)


@dataclass
class LinkerSettings:
    warning_settings: LinkerWarningSettings = field(default_factory=LinkerWarningSettings)
    enable_debug_info: bool = False
    enable_security_checks: bool = False
    enable_optimizations: bool = False


class LinkerArgFormatter(ABC):
    @abstractmethod
    def format_input_output_declaration(
            self, output_dir_path: str, output_base_name: str, target_kind: TargetKind
    ) -> list[str]:
        pass

    @abstractmethod
    def format_lib_arg(self, lib: str) -> str:
        pass

    @abstractmethod
    def format_lib_dir_arg(self, lib_dir: str) -> str:
        pass

    @abstractmethod
    def format_settings_args(self, settings: LinkerSettings) -> list[str]:
        pass


def _get_default_linker_settings(build_type: str) -> LinkerSettings:
    settings = LinkerSettings()
    settings.warning_settings.treat_as_errors = True
    settings.warning_settings.warning_states["4099"] = LinkerWarningState.DISABLE

    if build_type == base.BUILD_TYPE_DEBUG:
        settings.enable_debug_info = True
        settings.enable_security_checks = True
        settings.enable_optimizations = False
        return settings

    if build_type == base.BUILD_TYPE_RELEASE:
        settings.enable_debug_info = False
        settings.enable_security_checks = False
        settings.enable_optimizations = True
        return settings

    if build_type == base.BUILD_TYPE_PROFILING:
        settings.enable_debug_info = True
        settings.enable_security_checks = False
        settings.enable_optimizations = True
        return settings

    raise NotImplementedError()


