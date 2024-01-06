import click
from src.config import ConfigManager

from src.client import get_api_client
from src.commands.base import cli
from src.services.project import ProjectService
from src.utils.display import display_text
from src.utils.json import pretty_print_dict
from src.utils.response import check_response


@cli.group()
def get():
    pass


@get.group("project")
def get_project():
    pass


@get.group("selfCheck")
def get_self_check():
    pass


@get.group("license")
def get_license():
    pass


@get.group("oss")
def get_oss():
    pass


@get.group("partner")
def get_partner():
    pass


# config
@get.command("config")
def get_config():
    config_info = ConfigManager.read_config()
    display_text(f"- Server: {config_info.server_url}")
    display_text(f"- Token: {config_info.token}")


# project
@get_project.command("list")
@click.option("--createDate", "createDate")
@click.option("--creator", "creator")
@click.option("--division", "division")
@click.option("--modelName", "modelName")
@click.option("--prjIdList", "prjIdList")
@click.option("--status", "status")
@click.option("--updateDate", "updateDate")
def get_project_list(
    createDate,
    creator,
    division,
    modelName,
    prjIdList,
    status,
    updateDate,
):
    data = ProjectService().get(
        createDate=createDate,
        creator=creator,
        division=division,
        modelName=modelName,
        prjIdList=prjIdList,
        status=status,
        updateDate=updateDate,
    )
    pretty_print_dict(data)


@get_project.command("models")
@click.option("--prjIdList", "prjIdList")
def get_project_models(prjIdList):
    data = ProjectService().get_models(prjIdList)
    pretty_print_dict(data)


@get_self_check.command("detail")
@click.option("--id", "id", help="selfCheck id")
def get_self_check_detail(id):
    client = get_api_client()
    response = client.get_self_check_detail(id=id)
    check_response(response)
    pretty_print_dict(response.json())


# license
@get_license.command("list")
@click.option("--licenseName", "licenseName", required=True, help="license name")
def get_license_list(licenseName):
    client = get_api_client()
    response = client.get_license_list(licenseName=licenseName)
    if response.status_code == 404:
        display_text("Not found")
        return
    check_response(response)
    pretty_print_dict(response.json())


# oss
@get_oss.command("list")
@click.option("--ossName", "ossName", required=True, help="oss name")
@click.option("--ossVersion", "ossVersion", help="oss version")
@click.option("--downloadLocation", "downloadLocation", help="download location")
def get_oss_list(ossName, ossVersion, downloadLocation):
    client = get_api_client()
    response = client.get_oss(
        ossName=ossName,
        ossVersion=ossVersion,
        downloadLocation=downloadLocation,
    )
    check_response(response)
    pretty_print_dict(response.json())


# partner
@get_partner.command("list")
@click.option("--createDate", "createDate")
@click.option("--creator", "creator")
@click.option("--division", "division")
@click.option("--partnerIdList", "partnerIdList")
@click.option("--status", "status")
@click.option("--updateDate", "updateDate")
def get_partner_list(
    createDate,
    creator,
    division,
    partnerIdList,
    status,
    updateDate,
):
    client = get_api_client()
    response = client.get_partner_list(
        createDate=createDate,
        creator=creator,
        division=division,
        partnerIdList=partnerIdList,
        status=status,
        updateDate=updateDate,
    )
    check_response(response)
    pretty_print_dict(response.json())


# code
@get.command("code")
@click.option("--codeType", "codeType", required=True, help="code type")
@click.option("--detailValue", "detailValue", help="detail value")
def get_code(codeType, detailValue):
    client = get_api_client()
    response = client.get_code(codeType=codeType, detailValue=detailValue)
    check_response(response)
    pretty_print_dict(response.json())


# vulnerability
@get.command("maxVulnerability")
@click.option("--ossName", "ossName", required=True, help="oss name")
@click.option("--ossVersion", "ossVersion", help="oss version")
def get_max_vulnerability(ossName, ossVersion):
    client = get_api_client()
    response = client.get_max_vulnerability(ossName=ossName, ossVersion=ossVersion)
    check_response(response)
    pretty_print_dict(response.json())


@get.command("vulnerability")
@click.option("--cveId", "cveId", help="cve id")
@click.option("--ossName", "ossName", help="oss name")
@click.option("--ossVersion", "ossVersion", help="oss version")
def get_vulnerability(cveId, ossName, ossVersion):
    client = get_api_client()
    response = client.get_vulnerability(
        cveId=cveId,
        ossName=ossName,
        ossVersion=ossVersion,
    )
    check_response(response)
    pretty_print_dict(response.json())
