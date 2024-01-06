from requests import Response

from src.client import get_api_client
from src.dto.scan_result import ScanResult
from src.enums import CodeType
from src.scanner import FosslightScanner
from src.utils.codes import get_code_value
from src.utils.file import read_file
from src.utils.response import check_response


class ProjectService:

    def create(
        self,
        prjName,
        osType,
        distributionType,
        networkServerType,
        priority,
        osTypeEtc=None,
        prjVersion=None,
        publicYn=None,
        comment=None,
        userComment=None,
        watcherEmailList=None,
        modelListToUpdate=None,
        modelReportFile=None,
    ) -> str:
        response = get_api_client().create_project(
            prjName=prjName,
            osType=get_code_value(osType, CodeType.OS_TYPE),
            distributionType=get_code_value(distributionType, CodeType.DISTRIBUTION_TYPE),
            networkServerType=networkServerType,
            priority=get_code_value(priority, CodeType.PRIORITY),
            osTypeEtc=osTypeEtc,
            prjVersion=prjVersion,
            publicYn=publicYn,
            comment=comment,
            userComment=userComment,
            watcherEmailList=watcherEmailList,
            modelListToUpdate=modelListToUpdate,
            modelReportFile=modelReportFile,
        )
        check_response(response)
        return response.json()['prjId']

    def compare_bom(self, prjId, compareId) -> dict:
        response = get_api_client().compare_project_bom(prjId=prjId, compareId=compareId)
        check_response(response)
        return response.json()

    def export_bom(self, prjId, mergeSaveFlag) -> Response:
        response = get_api_client().export_project_bom(prjId=prjId, mergeSaveFlag=mergeSaveFlag)
        check_response(response)
        return response

    def export_bom_json(self, prjId) -> dict:
        response = get_api_client().export_project_bom_json(prjId)
        check_response(response)
        return response.json()

    def get(
        self,
        createDate=None,
        creator=None,
        division=None,
        modelName=None,
        prjIdList=None,
        status=None,
        updateDate=None,
    ) -> dict:
        client = get_api_client()
        response = client.get_project_list(
            createDate=createDate,
            creator=creator,
            division=division,
            modelName=modelName,
            prjIdList=prjIdList,
            status=status,
            updateDate=updateDate,
        )
        check_response(response)
        return response.json()

    def get_models(self, prjIdList) -> dict:
        client = get_api_client()
        response = client.get_project_models(prjIdList=prjIdList)
        check_response(response)
        return response.json()

    def update_watchers(self, prjId, emailList):
        response = get_api_client().update_project_watchers(prjId=prjId, emailList=emailList)
        check_response(response)

    def update_models(self, prjId, modelListToUpdate):
        response = get_api_client().update_project_models(prjId=prjId, modelListToUpdate=modelListToUpdate)
        check_response(response)

    def update_model_file(self, prjId, modelReport):
        response = get_api_client().update_project_model_file(prjId=prjId, modelReport=read_file(modelReport))
        check_response(response)

    def update_bin(
        self,
        prjId,
        ossReport=None,
        binaryTxt=None,
        comment=None,
        resetFlag=None,
    ):
        response = get_api_client().update_project_bin(
            prjId=prjId,
            ossReport=read_file(ossReport) if ossReport else None,
            binaryTxt=read_file(binaryTxt) if binaryTxt else None,
            comment=comment,
            resetFlag=resetFlag,
        )
        check_response(response)

    def update_src(
        self,
        prjId,
        ossReport=None,
        comment=None,
        resetFlag=None,
    ):
        response = get_api_client().update_project_src(
            prjId=prjId,
            ossReport=read_file(ossReport) if ossReport else None,
            comment=comment,
            resetFlag=resetFlag,
        )
        check_response(response)

    def update_package(self, prjId, packageFile, verifyFlag=None):
        response = get_api_client().update_project_package(
            prjId=prjId,
            packageFile=read_file(packageFile) if packageFile else None,
            verifyFlag=verifyFlag,
        )
        check_response(response)

    # scan and upload bin, src files
    def scan(self, prjId, dir):
        result: ScanResult = FosslightScanner.scan_all(dir)
        report_file_path = result.report_file_path
        binary_file_path = result.binary_file_path

        if report_file_path or binary_file_path:
            self.update_bin(
                prjId=prjId,
                ossReport=report_file_path,
                binaryTxt=binary_file_path,
            )
        if report_file_path:
            self.update_src(
                prjId=prjId,
                ossReport=report_file_path,
            )

    def export_notice(self, prjId):
        # get notice html file
        response = get_api_client().export_project_notice(prjId=prjId)
        check_response(response)
        return response
