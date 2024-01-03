import fs

from . import base
from .workspace_def import TargetKind
from .linker_base import LinkerArgFormatter, LinkerSettings, LinkerWarningState, LinkerWarningSettings


class LinkerArgFormatterLink(LinkerArgFormatter):
    def format_input_output_declaration(
            self, output_dir_path: str, output_base_name: str, target_kind: TargetKind
    ) -> list[str]:
        output_pdb_path = fs.path.join(output_dir_path, f"{output_base_name}-lib.pdb")
        args = ["\"%1\"", "/out:\"%2\"", f"/pdb:\"{output_pdb_path}\""]
        if target_kind == TargetKind.DYNAMIC_LIB:
            args += ["/DLL"]
        return args

    def format_lib_arg(self, lib: str) -> str:
        return lib

    def format_lib_dir_arg(self, lib_dir: str) -> str:
        return f"/libpath:\"{lib_dir}\""

    @staticmethod
    def _format_warning_state(warn: str, state: LinkerWarningState) -> list[str]:
        match state:
            case LinkerWarningState.ENABLE:
                return []
            case LinkerWarningState.DISABLE:
                return [f"/IGNORE:{warn}"]
            case LinkerWarningState.TREAT_AS_ERROR:
                return [f"/WX:{warn}"]
            case _:
                raise NotImplementedError()

    @classmethod
    def _format_warning_states(cls, states: dict[str, LinkerWarningState]) -> list[str]:
        l = []
        for warn, state in states.items():
            l += cls._format_warning_state(warn, state)
        return l

    @classmethod
    def _format_warning_settings(cls, settings: LinkerWarningSettings) -> list[str]:
        l = []
        l += ["/WX"] if settings.treat_as_errors else ["/WX:NO"]
        l += ["/MACHINE:X64"]
        l += cls._format_warning_states(settings.warning_states)
        return l

    def format_settings_args(self, settings: LinkerSettings) -> list[str]:
        l = []
        l += ["/NOLOGO"]
        l += self._format_warning_settings(settings.warning_settings)
        l += ["/DEBUG:FULL"] if settings.enable_debug_info else ["/DEBUG:NONE"]
        l += ["/GUARD:CF"] if settings.enable_security_checks else ["/GUARD:NO"]
        l += ["/OPT:REF,ICF,LBR"] if settings.enable_optimizations else ["/OPT:NOREF,NOICF,NOLBR"]
        return l


class LinkerArgFormatterLLDLink(LinkerArgFormatterLink):
    pass
