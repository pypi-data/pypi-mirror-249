"""Base class for classes containing GEMD templates and objects."""

import os, warnings
from abc import ABC, abstractmethod
from typing import ClassVar, Type, Optional

from gemd import FileLink
from gemd.entity.attribute.base_attribute import BaseAttribute
from gemd.entity.util import make_instance

# from gemd.util.impl import set_uuids
from openmsimodel.entity.gemd.impl import assign_uuid

from openmsimodel.utilities.cached_isinstance_functions import (
    isinstance_template,
    isinstance_spec,
    isinstance_run,
)
from openmsimodel.utilities.typing import (
    Template,
    Spec,
    Run,
    SpecOrRun,
    SpecOrRunLiteral,
)
from openmsimodel.utilities.attributes import (
    AttrsDict,
    validate_state,
    update_attrs,
    remove_attrs,
    _validate_temp_keys,
    define_attribute,
    finalize_template,
)

from openmsimodel.utilities.logging import Logger
import openmsimodel.stores.gemd_template_store as store_tools

__all__ = ["Element"]


class Element(ABC):
    """
    Base class for materials, processes, and measurements.

    ``Element`` 's are thin wrappers for GEMD entities. One ``Element`` contains
    a template, spec, and run for the same kind of entity (``Material``,
    ``Process``, or ``Measurement``) and helps to create, update, link, and
    output these.

    Note that `name` is the GEMD name given to the spec and run. The template
    name is the name of the subclass.

    To subclass:

    1. Instantiate ``TEMPLATE`` as follows:
    ``TEMPLATE: ClassVar[Template] = Template(name=__name__)``,
    replacing ``Template`` with one of ``MaterialTemplate``,
    ``ProcessTemplate``, or ``MeasurementTemplate``.

    2. Instantiate ``_ATTRS`` as follows:
    ``_ATTRS``: ClassVar[AttrsDict] = _validate_temp_keys(TEMPLATE)

    3. Add conditions, parameters, and/or properties using
    ``define_attribute(_ATTRS, ...)`` from the ``qf_gemd.base.attributes``
    module.

    4. Call ``finalize_template(_ATTRS, TEMPLATE)``, found in the
    ``qf_gemd.base.attributes`` module, to add attributes to ``TEMPLATE``.

    5. Follow any additional subclass directions.
    """

    _TempType: ClassVar[Type[Template]]
    _SpecType: ClassVar[Type[Spec]]
    _RunType: ClassVar[Type[Run]]

    TEMPLATE: ClassVar[Template]

    _ATTRS: ClassVar[AttrsDict]

    # TODO: remove and put somewhere
    _TAG_SEP: ClassVar[str] = "::"

    def __init__(
        self,
        name: str,
        *,
        template: ClassVar[
            Template
        ] = None,  # TODO: triple check with abc's hastemplate
        notes: Optional[str] = None,
    ) -> None:
        super().__init__()

        self.name = name
        self.logger = Logger()
        self.TEMPLATE_WRAPPER = {}
        has_template = hasattr(self, "TEMPLATE")

        if not has_template and not template:
            # TODO: Change msg
            raise AttributeError(
                f"TEMPLATE is not defined. Assign to 'template' parameter an instance of either {Template.__dict__['__args__']},\n OR create a new subclass with a defined TEMPLATE attribute."
            )

        if template:
            if has_template:
                warnings.warn(
                    f"Found template '{self.TEMPLATE.name}', but '{template.name}' will be used instead.",
                    ResourceWarning,
                )
            self.TEMPLATE = template
            # if ("persistent_id" in self.TEMPLATE.uids.keys()) or (
            #     "auto" in self.TEMPLATE.uids.keys()
            # ):
            #     raise KeyError(
            #         f'the "auto" and "persistent_id" uid keys are reserved. Use another key. '
            #     )

            # TODO: Extend (or sync with external func that returns a dict for runs/specs

        # TODO: change from file when supporting file links
        # registering the object templates
        if store_tools.stores_config.activated:
            for i, store in enumerate(
                store_tools.stores_config.all_template_stores.values()
            ):
                self.TEMPLATE_WRAPPER[store.id] = store.register_new_template(
                    self.TEMPLATE,
                    from_file=False,
                    from_store=False,
                    from_memory=bool(template),
                    from_subclass=bool(has_template and not template),
                )
                if store_tools.stores_config.designated_store_id == store.id:
                    self.TEMPLATE = self.TEMPLATE_WRAPPER[
                        store_tools.stores_config.designated_store_id
                    ].template

        if (
            template
        ):  # FIXME: maybe dont need to check, just call all the time? even if redundant?
            self.prepare_attrs()

        # registering the attribute templates
        if store_tools.stores_config.activated:
            for i, store in enumerate(
                store_tools.stores_config.all_template_stores.values()
            ):
                for _attr_type in self._ATTRS.keys():
                    for _attr in self._ATTRS[_attr_type].values():
                        store_tools.stores_config.all_template_stores[
                            store.id
                        ].register_new_template(_attr["obj"])

        self._spec: Spec = self._SpecType(
            name=name, notes=notes, template=self.TEMPLATE
        )
        self._run: Run = make_instance(self._spec)
        assign_uuid(self._spec, "auto")
        assign_uuid(self._run, "auto")  # redundant?

    @property
    @abstractmethod
    def spec(self) -> Spec:
        """The underlying GEMD spec."""

    @property
    @abstractmethod
    def run(self) -> Run:
        """The underlying GEMD run."""

    ############################### ATTRIBUTES ###############################

    def prepare_attrs(self):
        self._ATTRS = _validate_temp_keys(self.TEMPLATE)
        if hasattr(self.TEMPLATE, "conditions"):
            for c in self.TEMPLATE.conditions:
                define_attribute(
                    self._ATTRS, template=c[0]
                )  # TODO: look into this weird format from GEMD (attr, bounds)
        if hasattr(self.TEMPLATE, "parameters"):
            for pa in self.TEMPLATE.parameters:
                define_attribute(self._ATTRS, template=pa[0])
        if hasattr(self.TEMPLATE, "properties"):
            for pr in self.TEMPLATE.properties:
                define_attribute(self._ATTRS, template=pr[0])
        # finalize_template(self._ATTRS, self.TEMPLATE)

    def _update_attributes(
        self,
        AttrType: Type[BaseAttribute],
        attributes: tuple[BaseAttribute],
        replace_all: bool = False,
        which: SpecOrRunLiteral = "spec",
    ) -> None:
        """Update attributes and link attribute templates."""

        update_attrs(
            self._ATTRS, self._spec, self._run, AttrType, attributes, replace_all, which
        )

    def _remove_attributes(
        self,
        AttrType: Type[BaseAttribute],
        attr_names: tuple[str, ...],
        which: SpecOrRunLiteral = "spec",
    ) -> None:
        """Remove attributes by name."""

        remove_attrs(self._ATTRS, self._spec, self._run, AttrType, attr_names, which)

    ############################### TAGS ###############################
    def update_tags(
        self,
        *tags: tuple[str, ...],
        replace_all: bool = False,
        which: SpecOrRunLiteral = "spec",
    ) -> None:
        """
        Change or add hierarchical tags.

        Each tag is represented by a ``tuple`` of hierarchical ``str`` s. For
        example, ``('Quantum Design', 'MPMS3')``, in that order, describes the
        make and model of a particular measurement instrument.

        When `replace_all` is ``False``, any existing tags that are exactly the
        same as a new tag will not be duplicated. However, a tag that is the
        "child" of an existing tag will not override the "parent" tag. For
        example, it is possible to have all of the following at once:
        ``('Quantum Design', 'DynaCool')``,
        ``('Quantum Design', 'DynaCool', '1')``,
        and ``('Quantum Design', 'DynaCool', '3')``.

        Internally, tag strings will be concatenated with ``'::'`` as
        recommended by the GEMD specification.

        tags: tuple[str]
            tuples representing tags to add. Each tuple should contain the
            components of a tag from most general to most specific.
        replace_all: bool, default False
            If ``True``, remove any existing tags before adding new ones.
        which: {'spec', 'run', 'both'}, default 'spec'
            Whether to update the spec, run, or both.
        """

        validate_state(which)

        if which in ["spec", "both"]:
            self._set_tags(self._spec, tags, replace_all)

        if which in ["run", "both"]:
            self._set_tags(self._run, tags, replace_all)

    def remove_tags(
        self, *tags: tuple[str, ...], which: SpecOrRunLiteral = "spec"
    ) -> None:
        """Remove tags.

        See `update_tags` for tag format details. Tags are removed by exact
        comparison of the underlying hierarchcal ``str`` s.

        tags: tuple[str]
        ``tuple`` s representing tags to remove.
        which: {'spec', 'run', 'both'}, default 'spec'
        Whether to remove from the spec, run, or both.
        """

        validate_state(which)

        if which in ["spec", "both"]:
            self._remove_tags(self._spec, tags)

        if which in ["run", "both"]:
            self._remove_tags(self._run, tags)

    # TODO: merge into one method?
    @classmethod
    def _set_tags(
        cls,
        spec_or_run: SpecOrRun,
        tags: tuple[tuple[str, ...], ...],
        replace_all: bool = False,
    ) -> None:
        """Set tags for the spec or run."""

        tag_strs = [cls._TAG_SEP.join(tag) for tag in tags]

        if not replace_all:
            existing_tags = [tag for tag in spec_or_run.tags if tag not in tag_strs]
        else:
            existing_tags = []

        spec_or_run.tags = existing_tags + tag_strs

    @classmethod
    def _remove_tags(
        cls, spec_or_run: SpecOrRun, tags: tuple[tuple[str, ...], ...]
    ) -> None:
        """Remove tags from the spec or run."""

        tag_strs = [cls._TAG_SEP.join(tag) for tag in tags]
        spec_or_run.tags = [tag for tag in spec_or_run.tags if tag not in tag_strs]

    @staticmethod
    def _build_tags_dict(tags: list[str], parent_dict: dict, tag_sep: str) -> None:
        """Build a spec or run hierarchical tags ``dict``."""

        for tag_str in tags:
            tag_tup = tag_str.split(tag_sep)
            parent = parent_dict
            for component in tag_tup:
                if component not in parent:
                    parent[component] = {}
                parent = parent[component]

    def get_tags_dict(self):
        """Get a ``dict`` representing the hierarchical tags."""

        tags_dict = {"spec": {}, "run": {}}

        self._build_tags_dict(self._spec.tags, tags_dict["spec"], self._TAG_SEP)
        self._build_tags_dict(self._run.tags, tags_dict["run"], self._TAG_SEP)

        return tags_dict

    ############################### FILE LINKS ###############################
    def update_filelinks(
        self,
        *filelinks: FileLink,
        replace_all: bool = False,
        which: SpecOrRunLiteral = "spec",
    ) -> None:
        """
        Change or add file links.

        filelinks: FileLink
        The file links to change or add.
        replace_all: bool, default False
        If ``True``, remove any existing file links before adding new ones.
        which: {'spec', 'run', 'both'}, default 'spec'
        Whether to update the spec, run, or both.
        """

        validate_state(which)

        supplied_links = {self._link_str(link): link for link in filelinks}

        if which in ["spec", "both"]:
            self._set_filelinks(self._spec, supplied_links, replace_all)

        if which in ["run", "both"]:
            self._set_filelinks(self._run, supplied_links, replace_all)

    @classmethod
    def _set_filelinks(
        cls,
        spec_or_run: SpecOrRun,
        supplied_links: dict[str, FileLink],
        replace_all: bool = False,
    ) -> None:
        """Set links for the spec or run."""

        existing_links = (
            {}
            if replace_all
            else {cls._link_str(link): link for link in spec_or_run.file_links}
        )

        spec_or_run.file_links = {**existing_links, **supplied_links}.values()

    def remove_filelinks(
        self, *filelinks: FileLink, which: SpecOrRunLiteral = "spec"
    ) -> None:
        """Remove file links.

        filelinks: tuple[str]
            The file links to remove by comparison of the underlying url and
            filename.
        which: {'spec', 'run', 'both'}, default 'spec'
            Whether to remove from the spec, run, or both.
        """

        validate_state(which)

        if which in ["spec", "both"]:
            self._remove_filelinks(self._spec, filelinks)

        if which in ["run", "both"]:
            self._remove_filelinks(self._run, filelinks)

    @classmethod
    def _remove_filelinks(
        cls, spec_or_run: SpecOrRun, filelinks: tuple[FileLink]
    ) -> None:
        """Remove tags from the spec or run."""

        filelink_strs = [cls._link_str(link) for link in filelinks]

        spec_or_run.file_links = [
            link
            for link in spec_or_run.file_links
            if cls._link_str(link) not in filelink_strs
        ]

    @staticmethod
    def _link_str(link: FileLink) -> str:
        """
        Return a str representation of a ``FileLink`` based on its ``filename`` and url``.
        """
        # TODO: add conversion to standard file path or https
        return f'{link.filename}{"/" if link.filename.endswith("/") else ","}{link.url}'

    def get_filelinks_dict(self):
        """
        Get string representations of the file links.

        filelinks_dict: FileLinksDict
            Strings representing the file links of the spec and run.
        """

        filelinks_dict = {}

        filelinks_dict["spec"] = tuple(
            self._link_str(link) for link in self._spec.file_links
        )
        filelinks_dict["run"] = tuple(
            self._link_str(link) for link in self._run.file_links
        )

        return filelinks_dict

    # TODO: add a 'update_spec' function to != the 1:1 / template:spec duality
    def return_all_gemd(self) -> list:
        if self.__class__.__name__ == "Ingredient":
            return [self.spec, self.run]
        else:
            return [self.TEMPLATE, self.spec, self.run]

    # @classmethod
    # def from_(cls, any):
    #     if isinstance_run(any):
    #         # element = cls(any.name, template=any.template)
    #         # element.spec = any.spec
    #         # element.run = any
    #     elif isinstance_spec(any):
    #         element = cls(any.name, template=any.template)
    #         element.spec = any
    #     elif isinstance_template(any):
    #         element = cls(any.name, template=any)
    #     return element

    # @abstractmethod
    # def to_form(self) -> str:
    #     """Return a ``str`` specifying how to create a web form for this node."""

    # def thin_dumps(self, encoder, destination):
    #     for obj in [self._spec, self._run]:
    #         encoder.thin_dumps(obj,indent=3) # trigger uids assignment
    #         fn = '_'.join([obj.__class__.__name__, obj.name,obj.uids['auto']])
    #         with open(os.path.join(destination, fn),'w') as fp:
    #             fp.write(encoder.thin_dumps(obj,indent=3))

    # def thin_dumps(self, encoder, destination):
    #     self.dump_loop(encoder.thin_dumps, destination)

    # def dumps(self, encoder, destination):
    #     self.dump_loop(encoder.dumps, destination)

    # def dump_loop(self, encoder_func, destination):
    #     for obj in [self._spec, self._run]:
    #         encoder_func(obj, indent=3)  # trigger uids assignment
    #         fn = "_".join([obj.__class__.__name__, obj.name, obj.uids["auto"]])
    #         with open(os.path.join(destination, fn), "w") as fp:
    #             fp.write(encoder_func(obj, indent=3))
