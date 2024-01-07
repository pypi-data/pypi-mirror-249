from enum import Enum
from typing import Dict, Mapping, Optional

from jinja2 import Environment, PackageLoader, select_autoescape

from .filters import make_tex_escape


class TemplateType(str, Enum):
    tex = "tex"
    md = "md"


DEFAULT_TEMPLATE: Mapping[TemplateType, str] = {
    TemplateType.tex: "resume.tex.j2",
    TemplateType.md: "resume.md.j2",
}


class EnvironmentBuilder:
    def __init__(self, pkg_name: str = "jobapppy"):
        self._loader: PackageLoader = PackageLoader(pkg_name)

    def _tex(self, replace_strings: Optional[Dict[str, str]] = None) -> Environment:
        env = Environment(
            loader=self._loader,
            autoescape=select_autoescape(),
            block_start_string="<%",
            block_end_string="%>",
            variable_start_string="<<",
            variable_end_string=">>",
            comment_start_string="<#",
            comment_end_string="#>",
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters["tex_escape"] = make_tex_escape(extra_strings=replace_strings)

        return env

    def _md(self, replace_strings: Optional[Dict[str, str]] = None) -> Environment:
        return Environment(
            loader=self._loader,
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

    def build(self, type_: TemplateType, *args, **kwargs):
        if type_ == TemplateType.tex:
            return self._tex(*args, **kwargs)
        elif type_ == TemplateType.md:
            return self._md(*args, **kwargs)
        raise ValueError(f"Unsupported template type: {type_}")
