import sys

import click
from loguru import logger
from pkJson._utils import pkJson, getCWD_Root, getPackage_Root, getProject_Root
from pkJson import __version__

logger.configure(**{"handlers": [{"sink": sys.stdout, "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>"}]})


oPk = pkJson()


# def getCWD_Root() -> Path:
#     """
#     Returns the project root directory for the current project we're in.
#
#     :return: path to the root of the project
#     :rtype: string
#     """
#     return Path(os.getcwd())
#
#
# def getPackage_Root() -> Path:
#     return os.path.dirname(os.path.abspath(__file__))
#
#
# def getProject_Root() -> Path:
#     return Path(__file__).parent.parent


def _version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'{__version__}')
    ctx.exit()


@click.group()
@click.option('-v', '--version', is_flag=True, callback=_version, expose_value=False, is_eager=True)
def cli():
    pass


@cli.command()
def settings():
    """Check configuration settings"""
    logger.info("pkJson: Config Settings")
    logger.info(f'{"":->160}')
    logger.info(f'CDW......: {getCWD_Root()}')
    logger.info(f'Package..: {getPackage_Root()}')
    logger.info(f'Project..: {getProject_Root()}')
    logger.info(f'Key File.: {oPk.ferKeyFile} --> {oPk.ferKey}')
    logger.info(f'Json File: {oPk.pkJsonFile}')


@cli.command()
@click.argument('path', default='.')
def encode(path):
    """Encode project into Json file"""

    oPk.encryptProject(path)


@cli.command()
@click.argument('filename', default='pkJson.json')
def decode(filename):
    """Encode project into Json file"""

    oPk.decryptProject(filename)
