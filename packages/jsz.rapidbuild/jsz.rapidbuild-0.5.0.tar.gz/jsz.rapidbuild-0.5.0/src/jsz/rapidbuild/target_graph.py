from dataclasses import dataclass, field
from typing import Any
import fs

from .workspace_def import (
    WorkspaceDefinition, TargetKind
)
from .graph import (
    DirectedGraph
)
from . import base
from .base import (
    extend_unique,
    append_unique
)


class TargetNotFoundError(RuntimeError):
    pass


class TargetDependencyError(RuntimeError):
    pass


@dataclass
class TargetInterface:
    name: str
    kind: TargetKind
    include_dirs: list[str] = field(default_factory=list)
    definitions: dict[str, Any] = field(default_factory=dict)
    link_libs: list[str] = field(default_factory=list)
    link_libs_external: list[str] = field(default_factory=list)
    link_libs_external_dirs: list[str] = field(default_factory=list)
    load_time_libs: list[str] = field(default_factory=list)
    load_time_libs_external: list[str] = field(default_factory=list)


@dataclass
class TargetImplementation:
    name: str
    kind: TargetKind
    source_dir: str = ""
    include_dirs: list[str] = field(default_factory=list)
    definitions: dict[str, Any] = field(default_factory=dict)
    link_libs: list[str] = field(default_factory=list)
    link_libs_external: list[str] = field(default_factory=list)
    link_libs_external_dirs: list[str] = field(default_factory=list)
    load_time_libs: list[str] = field(default_factory=list)
    load_time_libs_external: list[str] = field(default_factory=list)


class TargetGraph:
    def __init__(self, wks_def: WorkspaceDefinition = WorkspaceDefinition()):
        self.wks_def = wks_def
        self.graph = self._build()

        self.targets_interfaces = {}
        self.targets_impls = {}

    def _build(self):

        targets = self.wks_def.targets

        targets_ids = {tgt.name: idx for idx, tgt in enumerate(targets)}

        edges = []
        for target in targets:
            for dep_name in target.private_props.dependencies:
                if dep_name not in targets_ids.keys():
                    raise TargetNotFoundError(f"Target '{dep_name}' privately referenced by '{target.name}' was not defined.")
                edges.append((targets_ids[target.name], targets_ids[dep_name]))

            for dep_name in target.public_props.dependencies:
                if dep_name not in targets_ids.keys():
                    raise TargetNotFoundError(f"Target '{dep_name}' publicly referenced by '{target.name}' was not defined.")
                edges.append((targets_ids[target.name], targets_ids[dep_name]))

        return DirectedGraph(vertices=list(targets_ids.values()), edges=edges)

    def is_valid(self):
        return not self.graph.is_cyclic()

    @staticmethod
    def _add_definitions(iface, impl, dep_defs, *, is_public_dep):
        for name, value in dep_defs.items():
            # TODO: resolve conflicts (A=3, A=4)
            if is_public_dep:
                if name not in iface.definitions:
                    iface.definitions[name] = value
            if name not in impl.definitions:
                impl.definitions[name] = value

    @staticmethod
    def _process_dependency(iface, impl, dep_iface, dep_simple_name, *, is_public_dep):
        if dep_iface.kind == TargetKind.EXECUTABLE:
            raise TargetDependencyError("Cannot declare dep on an exe.")

        TargetGraph._add_definitions(iface, impl, dep_iface.definitions, is_public_dep=is_public_dep)

        if is_public_dep:
            extend_unique(iface.include_dirs, dep_iface.include_dirs)
        extend_unique(impl.include_dirs, dep_iface.include_dirs)

        extend_unique(iface.link_libs, dep_iface.link_libs)
        extend_unique(impl.link_libs, dep_iface.link_libs)

        extend_unique(iface.link_libs_external, dep_iface.link_libs_external)
        extend_unique(impl.link_libs_external, dep_iface.link_libs_external)

        extend_unique(iface.link_libs_external_dirs, dep_iface.link_libs_external_dirs)
        extend_unique(impl.link_libs_external_dirs, dep_iface.link_libs_external_dirs)

        if dep_iface.kind == TargetKind.DYNAMIC_LIB:
            append_unique(iface.load_time_libs, dep_simple_name)
            append_unique(impl.load_time_libs, dep_simple_name)

        extend_unique(iface.load_time_libs, dep_iface.load_time_libs)
        extend_unique(impl.load_time_libs, dep_iface.load_time_libs)

        extend_unique(iface.load_time_libs_external, dep_iface.load_time_libs_external)
        extend_unique(impl.load_time_libs_external, dep_iface.load_time_libs_external)

    @staticmethod
    def _process_ext_dependency(iface, impl, dep_iface, *, is_public_dep):

        TargetGraph._add_definitions(iface, impl, dep_iface.definitions, is_public_dep=is_public_dep)

        if is_public_dep:
            extend_unique(iface.include_dirs, dep_iface.include_dirs)
        extend_unique(impl.include_dirs, dep_iface.include_dirs)

        extend_unique(iface.link_libs_external, dep_iface.link_libs)
        extend_unique(impl.link_libs_external, dep_iface.link_libs)

        extend_unique(iface.link_libs_external_dirs, dep_iface.link_libs_dirs)
        extend_unique(impl.link_libs_external_dirs, dep_iface.link_libs_dirs)

        extend_unique(iface.load_time_libs_external, dep_iface.load_time_libs)
        extend_unique(impl.load_time_libs_external, dep_iface.load_time_libs)

    def calc_target_iface_impl(self, target_name: str, source_dir_abs_path: str, toolchain_name: str, build_type: str,
                               third_party_manifest):
        assert self.is_valid()

        target_def = self.wks_def.find_target_def(target_name)
        if target_def is None:
            raise TargetNotFoundError()

        if target_def.name in self.targets_impls:
            return self.targets_impls[target_def.name], self.targets_interfaces.get(target_def.name, None)

        target_key = base.build_target_key(target_def.name, toolchain_name, build_type)

        iface = TargetInterface(name=target_key, kind=target_def.kind)
        impl = TargetImplementation(name=target_key, kind=target_def.kind, source_dir="")

        target_public_include_dir_name = "include"
        target_private_include_dir_name = "src"
        target_source_dir_name = "src"

        target_public_include_path = fs.path.join(source_dir_abs_path, target_def.name, target_public_include_dir_name)
        target_private_include_path = fs.path.join(source_dir_abs_path, target_def.name, target_private_include_dir_name)
        target_source_dir_path = fs.path.join(source_dir_abs_path, target_def.name, target_source_dir_name)

        iface.include_dirs.append(target_public_include_path)
        impl.include_dirs.append(target_public_include_path)
        impl.include_dirs.append(target_private_include_path)

        impl.source_dir = target_source_dir_path

        iface.link_libs.append(target_def.name)

        #
        # process preprocessor definitions
        #

        # Own public definitions -> interface definitions + impl definitions
        self._add_definitions(iface, impl, target_def.public_props.definitions, is_public_dep=True)
        self._add_definitions(iface, impl, target_def.private_props.definitions, is_public_dep=False)

        #
        # process dependencies
        #

        for dep_name in target_def.public_props.dependencies:
            dep_iface, _ = self.calc_target_iface_impl(dep_name, source_dir_abs_path, toolchain_name, build_type, third_party_manifest)

            self._process_dependency(iface, impl, dep_iface, dep_name, is_public_dep=True)

        for dep_name in target_def.private_props.dependencies:
            dep_iface, _ = self.calc_target_iface_impl(dep_name, source_dir_abs_path, toolchain_name, build_type, third_party_manifest)

            self._process_dependency(iface, impl, dep_iface, dep_name, is_public_dep=False)

        #
        # process external dependencies
        #

        for ext_name in target_def.public_props.externals:
            dep_iface = third_party_manifest[base.build_target_key(ext_name, base.TOOLCHAIN_DEFAULT, build_type)]

            self._process_ext_dependency(iface, impl, dep_iface, is_public_dep=True)

        for ext_name in target_def.private_props.externals:
            dep_iface = third_party_manifest[base.build_target_key(ext_name, base.TOOLCHAIN_DEFAULT, build_type)]

            self._process_ext_dependency(iface, impl, dep_iface, is_public_dep=False)

        # save result
        target_key = base.build_target_key(target_def.name, toolchain_name, build_type)

        # Executables don't need an interface
        if target_def.kind != TargetKind.EXECUTABLE:
            self.targets_interfaces[target_key] = iface
        self.targets_impls[target_key] = impl

        return iface, impl


def create_targets_interfaces_and_implementations(
        source_dir_abs_path: str, toolchains: list[str], build_types: list[str], third_party_manifest,
        workspace_def: WorkspaceDefinition
):
    assert (len(source_dir_abs_path) != 0)
    assert (len(build_types) != 0)
    assert (len(toolchains) != 0)

    target_graph = TargetGraph(wks_def=workspace_def)
    if not target_graph.is_valid():
        raise TargetDependencyError()

    for toolchain_name in toolchains:
        for build_type in build_types:
            for target_def in workspace_def.targets:
                target_graph.calc_target_iface_impl(target_def.name, source_dir_abs_path, toolchain_name,
                                                    build_type, third_party_manifest)

    return target_graph.targets_interfaces, target_graph.targets_impls
