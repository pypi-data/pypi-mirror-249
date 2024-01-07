import os
import yaml


def load_yaml(file_path, environment="QA"):
    with open(file_path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)[environment]

def overwrite_config_with_env_vars(configurations_to_be_overwritten):
    """
    Overwrites configurations with environment variables if they exist.
    Parses the configurations recursively.

    :param configurations_to_be_overwritten: configurations dictionary
    :return: modified configurations dictionary
    """

    for key, value in configurations_to_be_overwritten.items():
        if type(value) == dict:
            value = overwrite_config_with_env_vars(value)
        else:
            if os.environ.get(key, None):
                configurations_to_be_overwritten[key] = os.environ.get(key, value)
    return configurations_to_be_overwritten




class Config():
    def __init__(self, INFRA='SKYPILOT', ENVIRONMENT='QA', **kwargs):
        """
        Configurations set in config.yaml will be overwritten by environment variables.
        INFRA and ENVIRONMENT will be overwritten by environment variables if they exist.

        INFRA: SKYPILOT # LOCAL,SKYPILOT
        ENVIRONMENT: 'QA'  # QA, PROD
        """

        self.INFRA = os.environ.get('INFRA', INFRA)
        self.ENVIRONMENT = os.environ.get('ENVIRONMENT', ENVIRONMENT)

        self.SRC_DIR_ABS_PATH = os.path.dirname(os.path.realpath(__file__))
        try:
            self.config = load_yaml(os.path.join(self.SRC_DIR_ABS_PATH, 'config_endpoint.yaml'), ENVIRONMENT)
            self.config = overwrite_config_with_env_vars(self.config)
            self.WORKER_CAPACITY = self.config['WORKER_CAPACITY']
            self.WORKER_NAME_PREFIX = self.config['WORKER_NAME_PREFIX']
            self.SKYPILOT_JOB_FILE = self.config['SKYPILOT_JOB_FILE']
            self.SKYPILOT_SERVIC_ACC_KEYFILE = self.config['SKYPILOT_SERVIC_ACC_KEYFILE']
            self.HOST = self.config['HOST']
            self.PORT = self.config['PORT']

        except FileNotFoundError:
            for key, value in kwargs.items():
                self.__setattr__(key, value)


