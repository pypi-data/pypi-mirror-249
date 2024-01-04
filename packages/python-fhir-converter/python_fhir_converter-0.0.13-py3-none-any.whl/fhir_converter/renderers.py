from __future__ import annotations

from collections.abc import Callable, Generator, Mapping
from functools import partial
from json import dump as json_dump
from os import walk as os_walk
from pathlib import Path
from typing import IO, Any, Optional, Union

from frozendict import frozendict
from liquid import Environment
from liquid.loaders import BaseLoader
from pyjson5 import loads as json5_loads

from fhir_converter import filters, hl7, loaders, tags, utils

DataInput = Union[str, IO]
DataOutput = IO


class CcdaRenderer:
    """Consolidated CDA document renderer. Supports rendering the documents to FHIR

    Filters:
        The module provides builtin filters to support the default templates provided
        within the module. Custom filters may be added for user defined templates.
        Consumers must provide the rendering environment with the custom filters registered.
        The builtin filters will be added unless a filter with the same name has already
        been registered.

    Tags:
        The module provides builtin tags to support the default templates provided
        within the module. Custom tags may be added for user defined templates.
        Consumers must provide the rendering environment with the custom tag(s) registered.
        The builtin tag(s) will be added unless a tag with the same name has already
        been registered.

    Args:
        env (Environment, optional): Optional rendering environment. A rendering environment
            will be constructed with builtin defaults when env is None. Defaults to None.
        template_globals (Mapping, optional): Optional mapping that will be added to the
            render context. Code mappings from ValueSet/ValueSet.json will be loaded
            from the module when template_globals is None. Defaults to None.
    """

    def __init__(
        self,
        env: Optional[Environment] = None,
        template_globals: Optional[Mapping[str, Any]] = None,
    ) -> None:
        if not env:
            env = get_environment()
        filters.register(env, filters.all)
        tags.register(env, tags.all)

        self.env = env
        self.template_globals = self._make_globals(template_globals)

    def _make_globals(self, globals: Optional[Mapping[str, Any]]) -> Mapping[str, Any]:
        template_globals = dict(globals or {})
        if not "code_mapping" in template_globals:
            value_set = json5_loads(
                loaders.read_text(self.env, filename="ValueSet/ValueSet.json")
            )
            template_globals["code_mapping"] = frozendict(value_set.get("Mapping", {}))
        return frozendict(template_globals)

    def render_fhir(
        self,
        template_name: str,
        xml_in: DataInput,
        fhir_out: DataOutput,
        encoding: str = "utf-8",
        **kwargs,
    ) -> None:
        """Renders the XML to FHIR writing the generated output to the supplied file like object.
        Keyword arguments will be forwarded to the json serializer

        Args:
            template_name (str): The rendering template
            xml_in (DataInput): The XML input. Either a string or file like object
            fhir_out (DataOutput): The file like object to write the rendered output
            encoding (str, optional): The encoding to use when parsing the XML input. Defaults to "utf-8".
        """
        json_dump(
            obj=self.render_to_fhir(template_name, xml_in, encoding),
            fp=fhir_out,
            **kwargs,
        )

    def render_to_fhir(
        self, template_name: str, xml_input: DataInput, encoding: str = "utf-8"
    ) -> dict:
        """Renders the XML to FHIR

        Args:
            template_name (str): The rendering template
            xml_in (DataInput): The XML input. Either a string or file like object
            encoding (str, optional): The encoding to use when parsing the XML input. Defaults to "utf-8".

        Returns:
            dict: The rendered FHIR bundle
        """
        template = self.env.get_template(template_name, globals=self.template_globals)
        return hl7.parse_fhir(
            json_input=template.render({"msg": utils.parse_xml(xml_input, encoding)}),
            encoding=encoding,
        )


def get_environment(
    auto_reload: bool = False,
    cache_size: int = 250,
    loader: Optional[BaseLoader] = None,
    defaults_loader: Optional[BaseLoader] = None,
    **kwargs,
) -> Environment:
    """Factory for creating rendering environments with builtin configurations. Keyword arguments
    will be forwarded to the rendering environment

    Args:
        auto_reload (bool, optional): If `True`, loaders that have an `uptodate` callable will
            reload template source data automatically. Defaults to False.
        cache_size (int, optional): The capacity of the template cache in number of templates.
            cache_size is None or less than 1 disables caching. Defaults to 250.
        loader (Optional[BaseLoader], optional): The loader to use when loading the
            reandering temples. Templates will be loaded from the default loader when
            loader is None. Defaults to None.
        defaults_loader (Optional[BaseLoader], optional): The default loader to use when a template
            can not be resolved by the loader. Defaults will be loaded from the module when
            defaults_loader is None. Defaults to None.

    Returns:
        Environment: the rendering environment
    """
    if not defaults_loader:
        defaults_loader = loaders.get_resource_loader(
            search_package="fhir_converter.templates.ccda"
        )
    if not loader:
        loader, defaults_loader = defaults_loader, None
    return Environment(
        loader=loaders.TemplateSystemLoader(
            loader=loader,
            auto_reload=auto_reload,
            cache_size=cache_size,
            defaults_loader=defaults_loader,
        ),
        auto_reload=auto_reload,
        cache_size=cache_size,
        **kwargs,
    )


def render_files_to_dir(
    render: Callable[[DataInput, DataOutput, str], None],
    from_dir: Path,
    to_dir: Path,
    extension: str = ".json",
    encoding: str = "utf-8",
    filter_func: Optional[Callable[[Path], bool]] = None,
    **kwargs,
) -> None:
    render_files(
        from_dir,
        render=partial(
            render_to_dir, render, to_dir=to_dir, extension=extension, encoding=encoding
        ),
        filter_func=filter_func,
        **kwargs,
    )


def render_to_dir(
    render: Callable[[DataInput, DataOutput, str], None],
    from_file: Path,
    to_dir: Path,
    extension: str = ".json",
    encoding: str = "utf-8",
    **kwargs,
) -> None:
    with open(from_file, "r", encoding=encoding) as data_in:
        out_path = to_dir.joinpath(from_file.with_suffix(extension).name)
        with open(out_path, "w", encoding=encoding) as data_out:
            render(data_in, data_out, encoding, **kwargs)


def render_files(
    from_dir: Path,
    render: Callable[[Path], None],
    filter_func: Optional[Callable[[Path], bool]] = None,
    **kwargs,
) -> None:
    def walk_dir() -> Generator[Path, Any, None]:
        for root, _, filenames in os_walk(from_dir):
            for file_path in filter(filter_func, map(Path, filenames)):
                yield Path(root).joinpath(file_path)

    for from_file in walk_dir():
        render(from_file, **kwargs)
