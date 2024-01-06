from typing import Optional, List

import requests

from src.config import ConfigManager
from src.enums import CodeType


class ApiClient:

    def __init__(self, server_url):
        self.server_url = server_url
        self.session = requests.Session()

    def set_token(self, token):
        self.session.headers.update({'Authorization': token})

    def post(self, path, *args, **kwargs):
        return self.session.post(self.server_url + path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return self.session.put(self.server_url + path, *args, **kwargs)

    def get(self, path, *args, **kwargs):
        return self.session.get(self.server_url + path, *args, **kwargs)

    def create_project(
        self,
        prjName: str,
        osType: str,
        distributionType: str,
        networkServerType: str,
        priority: str,
        osTypeEtc: Optional[str] = None,
        prjVersion: Optional[str] = None,
        publicYn: Optional[str] = None,
        comment: Optional[str] = None,
        userComment: Optional[str] = None,
        watcherEmailList: Optional[List[str]] = None,
        modelListToUpdate: Optional[List[str]] = None,
        modelReportFile: Optional[str] = None,
    ):
        data = {
            "prjName": prjName,
            "osType": osType,
            "distributionType": distributionType,
            "networkServerType": networkServerType,
            "priority": priority,
            "osTypeEtc": osTypeEtc,
            "prjVersion": prjVersion,
            "publicYn": publicYn,
            "comment": comment,
            "userComment": userComment,
            "watcherEmailList": watcherEmailList,
            "modelListToUpdate": modelListToUpdate,
            "modelReportFile": modelReportFile,
        }
        return self.post('/api/v2/projects', data=data)

    def update_project_watchers(self, prjId, emailList: List[str]):
        params = {"emailList": emailList}
        return self.post(f'/api/v2/projects/{prjId}/watchers', params=params)

    def update_project_models(self, prjId, modelListToUpdate: str):
        # modelListToUpdate: "Name1|AV/Car/Security > AV|20201010,Name2|AV/Car/Security > AV|20201010"
        params = {"modelListToUpdate": modelListToUpdate}
        return self.put(f'/api/v2/projects/{prjId}/models', params=params)

    def update_project_model_file(self, prjId, modelReport: bytes):
        files = {
            "modelReport": modelReport,
        }
        return self.put(f'/api/v2/projects/{prjId}/models/upload', files=files)

    def update_project_bin(
        self,
        prjId: int,
        ossReport: Optional[bytes] = None,
        binaryTxt: Optional[bytes] = None,
        comment: Optional[str]=None,
        resetFlag: Optional[str] = None,
    ):
        files = {
            "ossReport": ossReport,
            "binaryTxt": binaryTxt,
        }
        data = {
            "resetFlag": resetFlag,
            "comment": comment,
        }
        return self.put(f'/api/v2/projects/{prjId}/bin', data=data, files=files)

    def update_project_src(self, prjId: int, ossReport: Optional[bytes] = None, comment: Optional[str] = None, resetFlag: Optional[str] = None):
        files = {"ossReport": ossReport}
        data = {
            "resetFlag": resetFlag,
            "comment": comment,
        }
        return self.post(f'/api/v2/projects/{prjId}/src', data=data, files=files)

    def update_project_package(self, prjId: int, packageFile: bytes, verifyFlag: Optional[str] = None):
        data = {"verifyFlag": verifyFlag}
        files = {"packageFile": packageFile}
        return self.post(f'/api/v2/projects/{prjId}/packages', files=files, data=data)

    def get_project_list(
        self,
        createDate: Optional[str] = None,
        creator: Optional[str] = None,
        division: Optional[str] = None,
        modelName: Optional[str] = None,
        prjIdList: Optional[str] = None,
        status: Optional[str] = None,
        updateDate: Optional[str] = None,
    ):
        params = {
            "createDate": createDate,
            "creator": creator,
            "division": division,
            "modelName": modelName,
            "prjIdList": prjIdList,
            "status": status,
            "updateDate": updateDate,
        }
        return self.get('/api/v2/projects', params=params)

    def get_project_models(self, prjIdList: str):
        # prjIdList = "10,11"
        params = {"prjIdList": prjIdList}
        return self.get('/api/v2/projects/models', params=params)

    def compare_project_bom(self, prjId: int, compareId: int):
        return self.get(f'/api/v2/projects/{prjId}/bom/compare-with/{compareId}')

    def export_project_bom(self, prjId: int, mergeSaveFlag: Optional[str] = None):
        params = {"mergeSaveFlag": mergeSaveFlag}
        return self.get(f'/api/v2/projects/{prjId}/bom/export', params=params)

    def export_project_bom_json(self, prjId: int):
        return self.get(f'/api/v2/projects/{prjId}/bom/json')

    def export_project_notice(self, prjId: str):
        return self.get(f'/api/v2/projects/{prjId}/notice')

    def get_license_list(self, licenseName: str):
        data = {"licenseName": licenseName}
        return self.get('/api/v2/licenses', params=data)

    def get_oss(self, ossName: str, ossVersion: Optional[str] = None, downloadLocation: Optional[str] = None):
        params = {
            "ossName": ossName,
            "ossVersion": ossVersion,
            "downloadLocation": downloadLocation,
        }
        return self.get('/api/v2/oss', params=params)

    def get_partner_list(
        self,
        createDate: Optional[str] = None,
        creator: Optional[str] = None,
        division: Optional[str] = None,
        partnerIdList: Optional[str] = None,
        status: Optional[str] = None,
        updateDate: Optional[str] = None,
    ):
        params = {
            "createDate": createDate,
            "creator": creator,
            "division": division,
            "partnerIdList": partnerIdList,
            "status": status,
            "updateDate": updateDate,
        }
        return self.get('/api/v2/partners', params=params)

    def update_partner_watchers(self, partnerId: int, emailList: List[str]):
        data = {"emailList": emailList}
        return self.put(f"/api/v2/partners/{partnerId}/watchers", data=data)

    def get_max_vulnerability(self, ossName: str, ossVersion: Optional[str] = None):
        params = {
            "ossName": ossName,
            "ossVersion": ossVersion
        }
        return self.get('/api/v2/max-vulnerabilities', params=params)

    def get_vulnerability(self, cveId: Optional[str] = None, ossName: Optional[str] = None, ossVersion: Optional[str] = None):
        params = {
            "cveId": cveId,
            "ossName": ossName,
            "ossVersion": ossVersion
        }
        return self.get('/api/v2/vulnerabilities', params=params)

    def get_self_check_detail(self, id: str):
        return self.get(f'/api/v2/selfchecks/{id}')

    def create_self_check(self, prjName: str, prjVersion: Optional[str] = None):
        data = {"prjName": prjName, "prjVersion": prjVersion}
        return self.post('/api/v2/selfchecks', data=data)

    def update_self_check_report(self, selfCheckId: int, ossReport: bytes=None, resetFlag: str=None):
        files = {}
        if ossReport:
            files['ossReport'] = ossReport
        data = {
            "resetFlag": resetFlag
        }
        return self.put(f'/api/v2/selfchecks/{selfCheckId}/report', files=files, data=data)

    def update_self_check_watchers(self, selfCheckId: int, emailList: List[str]):
        return self.put(f'/api/v2/selfchecks/{selfCheckId}/watchers', data={"emailList": emailList})

    def export_self_check(self, selfCheckId: int):
        return self.get(f'/api/v2/selfchecks/{selfCheckId}/export')

    def get_code(self, codeType: CodeType, detailValue: str = None):
        params = {"codeType": codeType, "detailValue": detailValue}
        return self.get('/api/v2/codes', params=params)


def get_api_client():
    config = ConfigManager.read_config()
    if not config.server_url or not config.token:
        raise Exception('Please set server_url and token')
    client = ApiClient(config.server_url)
    client.set_token(config.token)
    return client
