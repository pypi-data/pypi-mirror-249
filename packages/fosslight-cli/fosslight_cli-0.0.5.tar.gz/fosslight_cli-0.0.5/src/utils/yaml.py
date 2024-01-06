import os
import re

import yaml


def read_yaml(file_path):
    path_matcher = re.compile(r'\$\{([^}^{]+)\}')

    def path_constructor(loader, node):
        ''' Extract the matched value, expand env variable, and replace the match '''
        value = node.value
        match = path_matcher.match(value)
        env_var = match.group()[2:-1]
        return os.environ.get(env_var, '') + value[match.end():]

    class EnvVarLoader(yaml.SafeLoader):
        pass

    EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
    EnvVarLoader.add_constructor('!path', path_constructor)

    with open(file_path) as f:
        data = yaml.load(f, Loader=EnvVarLoader)
    return data
