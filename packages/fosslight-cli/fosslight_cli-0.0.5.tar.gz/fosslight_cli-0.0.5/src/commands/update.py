import click
from src.config import ConfigManager

from src.client import get_api_client
from src.commands.base import cli
from src.enums.reset_flag import ResetFlag
from src.services.project import ProjectService
from src.services.self_check import SelfCheckService
from src.utils.display import display_text
from src.utils.response import check_response


@cli.group()
def update():
    pass


@update.group("project")
def update_project():
    pass


@update.group("selfCheck")
def update_self_check():
    pass


@update.group("partner")
def update_partner():
    pass


@update.command('config')
@click.option('--server', '-s', help="Server url")
@click.option('--token', '-t', help="Account token")
def update_config(server, token):
    config_info = ConfigManager.read_config()
    if server:
        config_info.server_url = server
    if token:
        config_info.token = token
    ConfigManager.save_config(server_url=config_info.server_url, token=config_info.token)
    display_text("Success: Update config")


@update_project.command('watchers')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--emailList', 'emailList', required=True, help="watcher emailList")
def update_project_watchers(prjId, emailList):
    ProjectService().update_watchers(prjId, emailList)
    display_text("success")


@update_project.command('models')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--modelListToUpdate', 'modelListToUpdate', required=True)
def update_project_models(prjId, modelListToUpdate):
    ProjectService().update_models(prjId, modelListToUpdate)
    display_text("Success: Update project model")


@update_project.command('modelFile')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--modelReport', 'modelReport', required=True)
def update_project_model_file(prjId, modelReport):
    ProjectService().update_model_file(prjId, modelReport)
    display_text("Success: Update project model file")


@update_project.command('scan')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--dir', 'dir', required=True, help="project directory path")
def update_project_scan(prjId, dir):
    ProjectService().scan(prjId, dir)
    display_text("Success: scan project")


@update_project.command('bin')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--ossReport', 'ossReport')
@click.option('--binaryTxt', 'binaryTxt')
@click.option('--comment', 'comment')
@click.option('--resetFlag', 'resetFlag', type=click.Choice(ResetFlag.choices))
def update_project_bin(
    prjId,
    ossReport,
    binaryTxt,
    comment,
    resetFlag,
):
    ProjectService().update_bin(prjId, ossReport, binaryTxt, comment, resetFlag)
    display_text("Success: Upload project bin")


@update_project.command('src')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--ossReport', 'ossReport')
@click.option('--comment', 'comment')
@click.option('--resetFlag', 'resetFlag', type=click.Choice(ResetFlag.choices))
def update_project_src(
    prjId,
    ossReport,
    comment,
    resetFlag,
):
    ProjectService().update_src(prjId, ossReport, comment, resetFlag)
    display_text("Success: Upload project src")


@update_project.command('package')
@click.option('--prjId', 'prjId', required=True, help="project id")
@click.option('--packageFile', 'packageFile', required=True)
@click.option('--verifyFlag', 'verifyFlag')
def update_project_package(prjId, packageFile, verifyFlag):
    ProjectService().update_package(prjId, packageFile, verifyFlag)
    display_text("Success: Upload project package")


@update_self_check.command('report')
@click.option('--selfCheckId', 'selfCheckId', required=True, help="selfCheck id")
@click.option('--ossReport', 'ossReport')
@click.option('--resetFlag', 'resetFlag', type=click.Choice(ResetFlag.choices))
def update_self_check_report(selfCheckId, ossReport, resetFlag):
    SelfCheckService().update_report(selfCheckId, ossReport, resetFlag)
    display_text("Success: Upload self-check report")


@update_self_check.command('watchers')
@click.option('--selfCheckId', 'selfCheckId', required=True, help="selfCheck id")
@click.option('--emailList', 'emailList', required=True)
def update_self_check_watchers(selfCheckId, emailList):
    SelfCheckService().update_watchers(selfCheckId, emailList)
    display_text("Success: Update self-check watchers")


@update_partner.command('watchers')
@click.option('--partnerId', 'partnerId', required=True, help="partner id")
@click.option('--emailList', 'emailList', required=True)
def update_partner_watchers(partnerId, emailList):
    client = get_api_client()
    response = client.update_partner_watchers(
        partnersId=partnerId,
        emailList=emailList,
    )
    check_response(response)
    display_text("Success: Update partners watchers")
