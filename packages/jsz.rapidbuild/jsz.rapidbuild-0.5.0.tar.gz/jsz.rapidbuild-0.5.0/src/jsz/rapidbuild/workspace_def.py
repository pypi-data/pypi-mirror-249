from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class WorkspaceInvalidFormat(RuntimeError):
    pass


class TargetKind(Enum):
    STATIC_LIB = auto()
    DYNAMIC_LIB = auto()
    EXECUTABLE = auto()

    @staticmethod
    def from_string(s: str):
        return {
            "rapid_static_lib": TargetKind.STATIC_LIB,
            "rapid_dynamic_lib": TargetKind.DYNAMIC_LIB,
            "rapid_exe": TargetKind.EXECUTABLE,
        }[s]

    def to_string(self):
        return {
            TargetKind.STATIC_LIB: "rapid_static_lib",
            TargetKind.DYNAMIC_LIB: "rapid_dynamic_lib",
            TargetKind.EXECUTABLE: "rapid_exe",
        }[self]


@dataclass
class TargetScopedProperties:
    definitions: dict[str, Any] = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)
    externals: list[str] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict):
        if not isinstance(d, dict):
            raise WorkspaceInvalidFormat()

        if not set(d.keys()).issubset({"definitions", "dependencies", "externals"}):
            raise WorkspaceInvalidFormat()

        definitions = d.get("definitions", {})
        if not isinstance(definitions, dict):
            raise WorkspaceInvalidFormat()

        dependencies = d.get("dependencies", [])
        if not isinstance(dependencies, list):
            raise WorkspaceInvalidFormat()

        externals = d.get("externals", [])
        if not isinstance(externals, list):
            raise WorkspaceInvalidFormat()

        return TargetScopedProperties(definitions=definitions, dependencies=dependencies, externals=externals)


@dataclass
class TargetDefinition:
    name: str
    kind: TargetKind
    private_props: TargetScopedProperties = field(default_factory=TargetScopedProperties)
    public_props: TargetScopedProperties = field(default_factory=TargetScopedProperties)

    @staticmethod
    def from_dict(name: str, d: dict):
        if not isinstance(d, dict):
            raise WorkspaceInvalidFormat()

        if not set(d.keys()).issubset({"kind", "public", "private"}):
            raise WorkspaceInvalidFormat()

        if "kind" not in d.keys():
            raise WorkspaceInvalidFormat()

        try:
            kind = TargetKind.from_string(d["kind"])
        except KeyError:
            raise WorkspaceInvalidFormat()

        public_props = TargetScopedProperties.from_dict(d.get("public", {}))
        private_props = TargetScopedProperties.from_dict(d.get("private", {}))
        return TargetDefinition(name=name, kind=kind, private_props=private_props, public_props=public_props)


@dataclass
class WorkspaceDefinition:
    targets: list[TargetDefinition] = field(default_factory=list)

    def find_target_def(self, name):
        for t in self.targets:
            if t.name == name:
                return t
        return None

    @staticmethod
    def from_dict(d):
        if not isinstance(d, dict):
            raise WorkspaceInvalidFormat()

        if len(d) == 0:
            raise WorkspaceInvalidFormat()

        targets = [TargetDefinition.from_dict(name, v) for name, v in d.items()]
        return WorkspaceDefinition(targets=targets)


