import datetime

import click

from src.commands.base import cli
from src.services.project import ProjectService
from src.services.self_check import SelfCheckService
from src.utils.display import display_text
from src.utils.json import pretty_print_dict


@cli.group()
def export():
    pass


@export.group("project")
def export_project():
    pass


@export_project.command("bom")
@click.option("--prjId", "prjId", required=True, help="project id")
@click.option("--mergeSaveFlag", "mergeSaveFlag", help="mergeSaveFlag")
@click.option("--output", "-o", "output", help="output file path")
def export_project_bom(prjId, mergeSaveFlag, output):
    response = ProjectService().export_bom(prjId, mergeSaveFlag)
    path = output if output else f"bom_{int(datetime.datetime.now().timestamp())}.xlsx"
    if not path.endswith(".xlsx"):
        path += ".xlsx"
    with open(path, "wb") as f:
        f.write(response.content)
    display_text("Success: Export project bom")


@export_project.command("bomJson")
@click.option("--prjId", "prjId", required=True, help="project id")
def export_project_bom_json(prjId):
    data = ProjectService().export_bom_json(prjId)
    pretty_print_dict(data)


@export_project.command("notice")
@click.option("--prjId", "prjId", required=True, help="project id")
@click.option("--output", "-o", "output", help="output file path")
def export_project_notice(prjId, output):
    response = ProjectService().export_notice(prjId)
    path = output if output else f"notice_{int(datetime.datetime.now().timestamp())}.html"

    if not path.endswith(".html"):
        path += ".html"
    with open(path, "w") as f:
        f.write(response.text)
    display_text(f"Success: {path} created")


@export.command("selfCheck")
@click.option("--selfCheckId", "selfCheckId", required=True, help="selfCheck id")
def export_self_check(selfCheckId):
    response = SelfCheckService().export(selfCheckId)
    with open(f"bom_{int(datetime.datetime.now().timestamp())}.xlsx", "wb") as f:
        f.write(response.content)
    display_text("Success: Export self-check")
