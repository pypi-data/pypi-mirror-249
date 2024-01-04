import json
import os
import operator as op
import pathlib
import sys
from zipfile import ZipFile

from cryptography.fernet import Fernet
from pathlib import Path
from loguru import logger

from pkJson._settings import settings

logger.configure(**{"handlers": [{"sink": sys.stdout, "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>"}]})


def getCWD_Root() -> Path:
    """
    Returns the project root directory for the current project we're in.

    :return: path to the root of the project
    :rtype: string
    """
    return Path(os.getcwd())


def getPackage_Root() -> Path:
    return os.path.dirname(os.path.abspath(__file__))


def getProject_Root() -> Path:
    # return Path(__file__).parent.parent
    return Path(os.getcwd())


class pkJson:
    def __init__(self):
        self.ferKey = None
        self.ferKeyFile = Path(getProject_Root()) / ".pkJsonrc"
        self.pkJsonFile = Path(getProject_Root()) / "pkJson.json"
        self.getKey()

    def getKey(self):
        self.ferKey = settings.FN_KEY.encode()

        # if os.path.exists(self.ferKeyFile):
        #     with open(self.ferKeyFile, 'rb') as f:
        #         self.ferKey = f.read()
        # else:
        #     self.ferKey = Fernet.generate_key()
        #
        #     with open(self.ferKeyFile, 'wb') as f:
        #         f.write(self.ferKey)

    def encryptPath(self, filepath):
        fernet = Fernet(self.ferKey)
        filepath = self.isString(filepath)  # if str convert to byte
        encrypted = fernet.encrypt(filepath)

        return encrypted.decode()

    def decryptPath(self, filepath):
        fernet = Fernet(self.ferKey)
        filepath = self.isString(filepath)  # if str convert to byte
        decrypted = fernet.decrypt(filepath)

        return decrypted

    def encryptFile(self, filename):
        fernet = Fernet(self.ferKey)

        with open(filename, 'rb') as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        return encrypted.decode()

    def decryptContent(self, content):
        fernet = Fernet(self.ferKey)
        content = self.isString(content)  # if str convert to byte
        decrypted = fernet.decrypt(content)

        return decrypted

    def createFileFolder(self, fullpath, content, jsonProject=".jsonProject"):
        fullpath = self.decryptPath(fullpath).decode()
        filename = os.path.basename(fullpath)
        filepath = os.path.dirname(fullpath)

        oFilePath = Path(getProject_Root()) / jsonProject / filepath
        oFileFull = Path(getProject_Root()) / jsonProject / filepath / filename
        oFileCreating = Path(jsonProject) / filepath / filename

        logger.info(f'Creating: {oFileCreating}')

        if not os.path.exists(oFilePath):
            os.makedirs(oFilePath)

        try:
            # logger.error(oFileFull)
            with open(f'{oFileFull}', 'wb') as f:
                f.write(self.decryptContent(content))
        except Exception:
            logger.error(f'Error creating file: {jsonProject}')

    def encryptProject(self, projectDir):
        self.getKey()

        desktop = pathlib.Path(projectDir)
        # desktop = pathlib.Path(getProject_Root()) / projectDir

        # logger.warning(f'{desktop}')

        desktop.rglob("*")

        project = {self.encryptPath("ferKey"): self.ferKey.decode()}
        for o in list(desktop.rglob("*")):
            if not self.ifExists(str(o)) and not o.is_dir():
                fullPath = str(o)
                logger.info(f'Adding: {fullPath}')
                key = self.encryptPath(fullPath)
                value = self.encryptFile(fullPath)
                project[key] = value
        # projectDir = 'jsonProject'

        with open(f'{self.pkJsonFile}', 'wb') as encrypted_file:
            encrypted_file.write(json.dumps(project, indent=2).encode())

        # with ZipFile('pkJson.zip', 'w') as oZip:
        #     oZip.write(self.pkJsonFile)

    def decryptProject(self, projectJson):
        oJson = {}
        if os.path.exists(projectJson):
            with open(projectJson) as f:
                oJson = json.load(f)
        else:
            logger.error(f'{projectJson} not found...')

        cnt = 0
        for k, v in oJson.items():
            if cnt == 0:
                self.ferKey = v
            else:
                self.createFileFolder(k, v)
            cnt += 1

    @staticmethod
    def ifExists(string):
        res = False
        # test_list = ['venv', '.git', '__pycache__', '.idea', 'seCodeCoverage', 'jsonProject', '.pytest_cache', 'egg-info', '.pkJsonrc', '.DS_Store', '.coverage', '.zip', 'pkJson.json', 'tar.gz', 'any.whl']
        test_list = settings.EXCLUDE_FILES
        for i in test_list:
            if op.contains(string, i):
                res = op.contains(string, i)
                break

        return res

    @staticmethod
    def isString(obj):
        if isinstance(obj, str):
            obj = obj.encode()
        return obj


if __name__ == '__main__':
    oJsonProject = pkJson()

    # rootDir = '.'
    # oJsonProject.encryptProject(rootDir)

    oJsonProject.decryptProject("jsonProject.json")
