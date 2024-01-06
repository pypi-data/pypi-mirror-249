import click

from src.commands.base import cli
from src.services.project import ProjectService
from src.utils.json import pretty_print_dict


@cli.group()
def compare():
    pass


@compare.group("project")
def compare_project():
    pass


# project
@compare_project.command(name="bom")
@click.option('--prjId', 'prjId', required=True)
@click.option('--compareId', 'compareId', required=True)
def compare_project_bom(prjId, compareId):
    data = ProjectService().compare_bom(prjId, compareId)
    pretty_print_dict(data)
