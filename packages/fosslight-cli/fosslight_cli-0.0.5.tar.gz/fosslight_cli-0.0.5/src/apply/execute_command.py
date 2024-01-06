import os


def execute_command(data: dict):
    command = data["command"]
    parameters = data.get("parameters", {})

    parameter_part = ' '.join([f"--{key} '{value}'" for key, value in parameters.items() if value])
    os.system(f"fosslight-cli {command} {parameter_part}")
