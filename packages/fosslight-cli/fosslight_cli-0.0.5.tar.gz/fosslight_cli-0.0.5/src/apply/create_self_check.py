from src.services.self_check import SelfCheckService

from src.utils.apply import has_key
from src.utils.display import display_text


def create_self_check(data: dict):
    service = SelfCheckService()

    # check schema
    required = [
        "parameters",
        "parameters.prjName",
        "parameters.prjVersion",
        "update.watchers.emailList",
        "scan.dir",
    ]
    for field in required:
        keys = field.split(".")
        if len(keys) == 1:
            assert has_key(data, keys), f"SchemaError: createSelfCheck.{field} required"
        else:
            if has_key(data, keys[:-1]):
                assert has_key(data, keys), f"SchemaError: createSelfCheck.{field} required"

    # create
    selfCheckId = service.create(**data["parameters"])
    display_text(f"SelfCheck created ({selfCheckId})")

    # update
    if update := data.get("update"):
        if watchers := update.get("watchers"):
            service.update_watchers(selfCheckId=selfCheckId, emailList=watchers["emailList"])
        display_text(f"SelfCheck updated")

    # scan
    if scan := data.get("scan"):
        service.scan(selfCheckId=selfCheckId, dir=scan["dir"])
    return selfCheckId
