import base64
import json
import os
import re
from pathlib import Path

from cryptography.fernet import Fernet
from pydantic_settings import BaseSettings


# Project Directory
ROOT = Path(os.getcwd())

settingDefault = '''# Configuration Settings - pkJson
# ----------------------------------------------------------------------------------------------------------------------
# NOTE: No need to use quotes around values but you can use single, double or no quotes.
#       The values are the items to the right of the equals sign, and comments are striped from line.
# ----------------------------------------------------------------------------------------------------------------------

[Settings]
fn_key                  = '{fn_key}'
exclude_files           = ['venv', '.git', '.idea', 'jsonProject', '__pycache__', '.pytest_cache',  'egg-info', '.pkJsonrc', '.DS_Store', '.coverage', 'pkJson.json', 'sePackages']
'''


class ConfigManager:
    """
    Class manages loading the configuration parameters from .env.settings and .env.secrets
    """

    def __init__(self, pramCheck=None):
        if pramCheck is None:
            pramCheck = dict()
        self.parameters = {}
        self.pramCheck = pramCheck
        self.error_list = {}
        self.error_occurred = False

        # -------------------------------------------------------------------------------------------------------------------------------------------
        # create default .env file if not exist, then load
        # -------------------------------------------------------------------------------------------------------------------------------------------
        filepath = f'{ROOT}/.pkJsonrc'
        if not os.path.exists(filepath):

            f = open(filepath, "w")
            oFN_KEY = base64.b64encode(Fernet.generate_key()).decode()
            f.write(settingDefault.format(fn_key=oFN_KEY))
            f.close()

        if os.path.exists(filepath):
            self.readFile(filepath)
        else:
            print(filepath)

    def readFile(self, filename):
        with open(filename, "r") as fEnv:
            lines = fEnv.readlines()
            count = 0
            search_pattern = re.compile(r'^[^#].+=[\"|\']*.*[\"|\']*$')

            for line in lines:
                count += 1
                if search_pattern.search(line):
                    # remove line comments
                    key_value_comment = line.strip().split("#", 1)

                    # split parameters/value
                    name, value = key_value_comment[0].strip().split("=", 1)

                    # remove single or double quotes from value
                    value = value.translate(str.maketrans('', '', '"\''))

                    # Remove all spaces on both sides of each object
                    name = name.strip()
                    value = value.strip()
                    self.parameters[name] = value

    def validateKeyList(self):

        if self.pramCheck:
            for parm in self.pramCheck:
                # The self.parameterList[parameters] element contains the keywords to determine whether a parameter is
                # required or optional.  If it is required, it should have the value "ERROR".  If it's optional,
                # it can be something like WARNING, INFO, or whatever else fits the purpose
                if not parm in self.parameters:
                    self.error_list[parm] = json.dumps({"settingsRequired": {"details": f'Setting \'{parm}\' does not exist in the config file and is required', "level": f'{self.pramCheck[parm]}'}})
                elif not self.parameters[parm]:
                    self.error_list[parm] = json.dumps({"settingsRequired": {"details": f'Setting \'{parm}\' is in the config file but is not set', "level": f'WARNING'}})

        self.error_occurred = self.checkConfigFileParameters()

    def checkConfigFileParameters(self):
        # This function checks the error_list array that is created in the init of this class
        # error_occurred = [e for e,v in self.error_list if re.search('ERROR',v)]
        error_occurred = False
        for (e, v) in self.error_list.items():
            if re.search('ERROR', v, re.IGNORECASE):
                error_occurred = True
        return error_occurred


settingsValidate = {"log_level": "ERROR", "log_appname": "ERROR", "log_inc_resp_body": "ERROR"}
oConfigManager = ConfigManager(settingsValidate)
oConfigManager.validateKeyList()


class Settings(BaseSettings):
    SETTING_ERRORS: dict = {}

    # Settings from .pkJsonrc
    try:
        FN_KEY: str = base64.b64decode(oConfigManager.parameters['fn_key']).decode()
        EXCLUDE_FILES: list = oConfigManager.parameters['exclude_files'].replace(" ", "").strip("[] ").split(',')

    except KeyError as ex:
        SETTING_ERRORS[ex.args[0]] = json.dumps({"settingsErrors": {"details": f'Setting {ex} does not exist in config.Settings. Needs to be removed if not required'}})

    @staticmethod
    def validateSettings():
        missing = {}
        for param in oConfigManager.parameters:
            try:
                eval(f'settings.{param.upper()}')

            except AttributeError:
                missing[param] = json.dumps({"settingsMissing": {"details": f'{param.upper()}: str = oConfigManager.parameters[\'{param}\']'}})

        return missing


settings = Settings()

settingsMissing = settings.validateSettings()
settingsErrors = settings.SETTING_ERRORS
settingsNotSet = oConfigManager.error_list

# for k, v in sorted(settings):
#     print(f'{k:>25}: {v}')
#
# if len(settingsMissing):
#     print("Need to add to pkJson._settings:")
#     for k, v in settingsMissing.items():
#         o = json.loads(v)
#         print(f'{o["settingsMissing"]["details"]}')
