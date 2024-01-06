from src.client import get_api_client
from src.enums import CodeType


# get the code value used for API calls
def get_code_value(name: str, code_type: CodeType) -> str:
    # TODO: caching
    client = get_api_client()
    response = client.get_code(codeType=code_type)
    code_list = response.json()['content']
    # To make it case-insensitive using upper()
    mapping = {x["cdDtlNm"].upper(): x["cdDtlNo"] for x in code_list}

    # name is already code value
    if name in mapping.values():
        return name

    # convert name to code value
    value = mapping.get(name.upper())
    if value is not None:
        return value
    raise ValueError(f"{CodeType.get_display_name(code_type)} - '{name}' is not a valid code.\n- available code inputs: {', '.join(mapping.keys())}")
