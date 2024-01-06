from src.services.project import ProjectService
from src.utils.apply import has_key
from src.utils.display import display_text


def create_project(data: dict):
    service = ProjectService()

    # check schema
    required = [
        "parameters",
        "parameters.prjName",
        "parameters.osType",

        "update.models.modelListToUpdate",
        "update.modelFile.modelReport",
        "update.watchers.emailList",

        "scan.dir",
    ]
    for field in required:
        keys = field.split(".")
        if len(keys) == 1:
            assert has_key(data, keys), f"SchemaError: createProject.{field} required"
        else:
            if has_key(data, keys[:-1]):
                assert has_key(data, keys), f"SchemaError: createProject.{field} required"

    # create
    prjId = service.create(**data["parameters"])
    display_text(f"Project created ({prjId})")

    # update
    if update := data["update"]:
        if models := update.get("models"):
            service.update_models(prjId=prjId, modelListToUpdate=models["modelListToUpdate"])
        if model_file := update.get("modelFile"):
            service.update_model_file(prjId=prjId, modelReport=model_file["modelReport"])
        if watchers := update.get("watchers"):
            service.update_watchers(prjId=prjId, emailList=watchers["emailList"])
        display_text(f"Project updated")

    # scan
    if scan := data.get("scan"):
        service.scan(prjId=prjId, dir=scan["dir"])
    return prjId
