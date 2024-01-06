import click

from src.commands.base import cli
from src.services.project import ProjectService
from src.services.self_check import SelfCheckService
from src.utils.output import set_output_result


@cli.group()
def create():
    pass


@create.command("project")
@click.option('--prjName', 'prjName', required=True, help="Name of the Project")
@click.option('--osType', 'osType', required=True, help="OS type of the Project")
@click.option('--distributionType', 'distributionType', required=True, help="")
@click.option('--networkServerType', 'networkServerType', required=True, help="")
@click.option('--priority', 'priority', required=True, help="")
@click.option('--osTypeEtc', 'osTypeEtc', help="")
@click.option('--prjVersion', 'prjVersion', help="")
@click.option('--publicYn', 'publicYn', help="")
@click.option('--comment', 'comment', help="")
@click.option('--userComment', 'userComment', help="")
@click.option('--watcherEmailList', 'watcherEmailList', help="")
@click.option('--modelListToUpdate', 'modelListToUpdate', help="")
@click.option('--modelReportFile', 'modelReportFile', help="")
def create_project(
    prjName,
    osType,
    distributionType,
    networkServerType,
    priority,
    osTypeEtc,
    prjVersion,
    publicYn,
    comment,
    userComment,
    watcherEmailList,
    modelListToUpdate,
    modelReportFile,
):
    prjId = ProjectService().create(
        prjName=prjName,
        osType=osType,
        distributionType=distributionType,
        networkServerType=networkServerType,
        priority=priority,
        osTypeEtc=osTypeEtc,
        prjVersion=prjVersion,
        publicYn=publicYn,
        comment=comment,
        userComment=userComment,
        watcherEmailList=watcherEmailList,
        modelListToUpdate=modelListToUpdate,
        modelReportFile=modelReportFile,
    )
    set_output_result(prjId)


@create.command("selfCheck")
@click.option('--prjName', 'prjName', required=True, help="Name of the Project")
@click.option('--prjVersion', 'prjVersion', help="Version of the Project")
def create_self_check(prjName, prjVersion):
    prjId = SelfCheckService().create(prjName=prjName, prjVersion=prjVersion)
    set_output_result(prjId)
