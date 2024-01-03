from . import base
from .compiler_base import (CompilerArgFormatter, CompilerSettings, LanguageStandard, UnsupportedLanguageError,
    LanguageConformance, CompilerWarningLevel, CompilerWarningState, CompilerWarningSettings, CompilerFloatBehavior,
    CompilerOptimizationMode, UnsupportedSettingError
)


class CompilerArgFormatterClang(CompilerArgFormatter):
    def format_beginning_args(self) -> list[str]:
        return []

    def format_object_compilation_args(self) -> list[str]:
        return ["-c", "%1", "-o", "%2"]

    def format_debug_info_args(self, output_dir_path: str, output_base_name: str) -> list[str]:
        return []

    def format_pch_creation_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        return [
            "-x", "c++-header", f"\"{pch_header_path}\"",
            "-o", "\"%2\""  # PCH output file (compiled .pch)
        ]

    def format_pch_usage_args(self, pch_header_path: str, pch_output_path: str) -> list[str]:
        return [
            "-include-pch", f"\"{pch_output_path}\""
        ]

    def format_definition_compiler_arg(self, name: str, value: base.Any) -> str:
        if value is not None:
            return f"-D\"{name}={value}\""
        else:
            return f"-D\"{name}\""

    def format_include_dir_arg(self, include_dir: str) -> str:
        return f"-I\"{include_dir}\""

    def format_system_include_dir_arg(self, include_dir: str) -> str:
        return f"-isystem\"{include_dir}\""

    @staticmethod
    def _format_language_std(std: LanguageStandard) -> list[str]:
        match std:
            case LanguageStandard.C89:
                return ['-x', 'c', '-std=c89']
            case LanguageStandard.C99:
                return ['-x', 'c', '-std=c99']
            case LanguageStandard.C11:
                return ['-x', 'c', '-std=c11']
            case LanguageStandard.C17:
                return ['-x', 'c', '-std=c17']
            case LanguageStandard.C23:
                return ['-x', 'c', '-std=c23']
            case LanguageStandard.C_LATEST:
                return ['-x', 'c', '-std=c23']
            case LanguageStandard.CPP03:
                return ['-x', 'c++', '-std=c++98']
            case LanguageStandard.CPP11:
                return ['-x', 'c++', '-std=c++11']
            case LanguageStandard.CPP14:
                return ['-x', 'c++', '-std=c++14']
            case LanguageStandard.CPP17:
                return ['-x', 'c++', '-std=c++17']
            case LanguageStandard.CPP20:
                return ['-x', 'c++', '-std=c++20']
            case LanguageStandard.CPP23:
                return ['-x', 'c++', '-std=c++23']
            case LanguageStandard.CPP_LATEST:
                return ['-x', 'c++', '-std=c++2c']
            case _:
                raise UnsupportedLanguageError(f"Unhandled language standard '{std}'.")

    @staticmethod
    def _format_language_conformance(lang_conformance: LanguageConformance) -> list[str]:
        match lang_conformance:
            case LanguageConformance.MIN:
                return [
                    "--no-pedantic",
                    "-fms-extensions",
                    # "-fms-volatile" #TODO: Unknown argument
                ]
            case LanguageConformance.MAX:
                return [
                    "--pedantic",
                    "--pedantic-errors",
                    "-fno-ms-extensions",
                    # "-fno-ms-volatile" #TODO: Unknown argument
                ]
            case _:
                raise UnsupportedLanguageError(f"Unhandled language conformance option '{lang_conformance}'.")

    @staticmethod
    def _format_warning_level(warning_level: CompilerWarningLevel) -> list[str]:
        match warning_level:
            case CompilerWarningLevel.W0:
                return ["-w"]
            case CompilerWarningLevel.W1:
                return ["-Wall"]
            case CompilerWarningLevel.W2:
                return ["-Wall"]
            case CompilerWarningLevel.W3:
                return ["-Wall"]
            case CompilerWarningLevel.W4:
                return ["-Wall", "-Wextra"]
            case CompilerWarningLevel.All:
                return ["-Wall", "-Wextra", "-Weverything"]
            case _:
                raise UnsupportedSettingError()

    @staticmethod
    def _format_warning_version(ver: str) -> list[str]:
        return []

    @staticmethod
    def _format_warning_state(warn: str, state: CompilerWarningState) -> list[str]:
        match state:
            case CompilerWarningState.DISABLE:
                return [f"-Wno-{warn}"]
            case CompilerWarningState.ENABLE:
                return [f"-W{warn}"]
            case CompilerWarningState.REPORT_ONCE:
                return [f"-W{warn}"]
            case CompilerWarningState.TREAT_AS_ERROR:
                return [f"-Werror={warn}"]
            case _:
                raise UnsupportedSettingError()

    @classmethod
    def _is_known_warning(cls, warn):
        return any(c.isalpha() for c in warn)

    @classmethod
    def _format_warning_states(cls, states: dict[str, CompilerWarningState]) -> list[str]:
        l = []
        for warn, state in states.items():
            if cls._is_known_warning(warn):
                l += cls._format_warning_state(warn, state)
        return l

    @classmethod
    def _format_warning_settings(cls, warning_settings: CompilerWarningSettings) -> list[str]:
        l = []
        l += cls._format_warning_level(warning_settings.level)
        l += cls._format_warning_version(warning_settings.version)
        if warning_settings.treat_as_errors:
            l += ["-Werror"]
        l += cls._format_warning_states(warning_settings.warning_states)
        l += ["-Wno-system-headers"]
        return l

    @staticmethod
    def _format_float_behavior(beh: CompilerFloatBehavior) -> list[str]:
        match beh:
            case CompilerFloatBehavior.PRECISE:
                return ["-ffp-model=precise"]
            case CompilerFloatBehavior.STRICT:
                return ["-ffp-model=strict"]
            case CompilerFloatBehavior.FAST:
                return ["-ffp-model=fast"]
            case _:
                raise UnsupportedSettingError()

    @staticmethod
    def _format_optimization_mode(opt: CompilerOptimizationMode) -> list[str]:
        match opt:
            case CompilerOptimizationMode.NONE:
                return ["-O0"]
            case CompilerOptimizationMode.MINIMIZE_SIZE:
                return ["-O3", "-Osize"]
            case CompilerOptimizationMode.MAXIMIZE_SPEED:
                return ["-O3", "-Ofast"]

    @classmethod
    def _format_compiler_settings(cls, settings: CompilerSettings) -> list[str]:
        l = []
        # emit error for unknown arguments
        # l += '/options:strict',
        l += cls._format_language_std(settings.lang_std)
        l += cls._format_language_conformance(settings.lang_conformance)
        l += cls._format_warning_settings(settings.warning_settings)
        l += ["-frtti"] if settings.enable_rtti else ["-fno-rtti"]
        l += ["-fcxx-exceptions"] if settings.enable_exceptions else ["-fno-cxx-exceptions"]
        l += cls._format_float_behavior(settings.float_behavior)
        l += ["-fno-complete-member-pointers"]
        # #TODO: unknown argument
        # l += ["-fms-runtime-lib=dll_dbg"] if settings.use_debug_runtime else ["-fms-runtime-lib=dll"]
        if settings.enable_debug_info:
            l += ["-g"]
        l += cls._format_optimization_mode(settings.optimization_mode)
        l += ["-mavx"]
        # if settings.enable_security_checks:
        #     # enable buffer security checks
        #     l += ['/GS']
        #     l += ['/sdl']
        #     # enable control flow guards
        #     l += ['/guard:cf']
        #     # enable EH continuation metadata(must be also present in linker args)
        #     l += ['/guard:ehcont']
        #     # enable all runtime checks.RTCc rejects conformant code, so it is not supported by
        #     # the C++ Standard Library
        #     l += ['/RTCsu']
        # else:
        #     # disable buffer security checks
        #     l += ['/GS-']
        #     # + '/sdl- ' // it overrides / GS -
        #     # disable control flow guards
        #     l += ['/guard:cf-']
        #     # disable EH continuation metadata
        #     l += ['/guard:ehcont-']
        return l

    def format_settings_args(self, settings: CompilerSettings) -> list[str]:
        return self._format_compiler_settings(settings)


class CompilerArgFormatterGCC(CompilerArgFormatterClang):
    pass


