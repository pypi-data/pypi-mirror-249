import json
import sys
from pathlib import Path
from typing import Optional

import typer
import yaml
from pydantic import RootModel, TypeAdapter

from .environments import DEFAULT_TEMPLATE, EnvironmentBuilder, TemplateType
from .schemas import JobAppYaml, TemplateConfig

cli = typer.Typer()


@cli.command()
def parse(
    json_indent: Optional[int] = typer.Option(None, "-i", help="Indentation for JSON output"),
    check: bool = typer.Option(False, "-c", "--check", help="Do not output JSON, just check if valid"),
    resume_yaml: typer.FileText = typer.Argument(sys.stdin, help="Yaml resume input"),
    output_file: typer.FileTextWrite = typer.Argument(sys.stdout, help="Write output to file"),
):
    try:
        data = yaml.safe_load(resume_yaml)
        jobapp = JobAppYaml(**data)
    except Exception as e:
        if check:
            typer.echo("ERROR", err=True)
        else:
            typer.echo(f"Error parsing resume yaml: {e}", err=True)
        raise typer.Exit(code=1)
    if check:
        typer.echo("OK", err=True)
    else:
        typer.echo(RootModel[JobAppYaml](jobapp).model_dump_json(indent=json_indent), file=output_file)


@cli.command()
def template(
    # template_file: Optional[Path] = typer.Option(..., "-f"),
    template_type: TemplateType = typer.Option(TemplateType.md, "-t", "--template-type"),
    template_config: Optional[Path] = typer.Option(
        None, "-c", "--template-config", help="Template configuration file (JSON)"
    ),
    resume_yaml: typer.FileText = typer.Argument(sys.stdin, help="Yaml resume input"),
    output_file: typer.FileTextWrite = typer.Argument(sys.stdout, help="Write output to file"),
):
    tmpl_config: TemplateConfig = TemplateConfig(replace_strings={})
    template_file = DEFAULT_TEMPLATE[template_type]

    if template_config:
        json_text = template_config.read_text()
        json_data = json.loads(json_text)
        tmpl_config = TemplateConfig(**json_data)

    env = EnvironmentBuilder().build(template_type, tmpl_config.replace_strings)
    template = env.get_template(template_file)

    data = yaml.safe_load(resume_yaml)
    jobapp = JobAppYaml(**data)

    rendered_output = template.render(resume=jobapp.resume)
    typer.echo(rendered_output, file=output_file)


@cli.command()
def schema(
    json_indent: Optional[int] = typer.Option(None, "-i", help="Indentation for JSON output"),
):
    typer.echo(json.dumps(TypeAdapter(JobAppYaml).json_schema(), indent=json_indent))
