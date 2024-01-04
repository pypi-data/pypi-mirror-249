import glob
import os
import subprocess

from unittest import TestCase, skipIf

import click
from click.testing import CliRunner
from pkJson.cli import cli


# noinspection PyTypeChecker
class seVersionTestCase(TestCase):
    """Test case class for seVersioning package."""
    def setUp(self) -> None:
        self.package = "codeTesting"

    def test_001_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        self.assertEqual(result.exit_code, 0)

    def test_002_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, "--version")
        self.assertEqual(result.exit_code, 0)

    def test_003_encode(self):
        runner = CliRunner()
        result = runner.invoke(cli, "encode")
        self.assertEqual(result.exit_code, 0)
        click.echo(result)
        # self.assertTrue("INFO" in result.output)

    def test_004_decode(self):
        runner = CliRunner()
        result = runner.invoke(cli, "decode")
        self.assertEqual(result.exit_code, 0)
        click.echo(result)
        # self.assertTrue("INFO" in result.output)

    def test_005_settings(self):
        runner = CliRunner()
        result = runner.invoke(cli, "settings")
        self.assertEqual(result.exit_code, 0)
        click.echo(result)
        # self.assertTrue("INFO" in result.output)

    # def test_004_1_newversion_full(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--newversion=23.3.0"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue("23.3.0" in result.output)
    #
    # def test_004_2_newversion_rc(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--newversion=23.3.0.rc1"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue("23.3.0.rc1" in result.output)
    #
    # def test_004_3_newversion_major(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--newversion=23"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue("23." in result.output)
    #
    # def test_004_4_newversion_minor(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--newversion=23.3"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue("23.3.0" in result.output)
    #
    # def test_005_1_rc1(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--rc"])
    #     self.assertEqual(result.exit_code, 0)
    #     # self.assertTrue("23.3.0.rc1" in result.output)
    #
    # def test_005_2_rc2(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--rc"])
    #     self.assertEqual(result.exit_code, 0)
    #     # self.assertTrue("23.3.0.rc2" in result.output)
    #
    # def test_006_patch(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--patch"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue("23.3.1" in result.output)
    #
    # def test_007_major(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--major"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue("24" in result.output)
    #
    # def test_008_minor(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--minor"])
    #     self.assertEqual(result.exit_code, 0)
    #
    # def test_009_post_none(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--post"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue(".post0" in result.output)
    #
    # def test_010_post_1(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--post"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue(".post1" in result.output)
    #
    # def test_011_dev_none(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--dev"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue(".dev0" in result.output)
    #
    # def test_012_dev_1(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--dev"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue(".dev1" in result.output)
    #
    # def test_013_release(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--release"])
    #     self.assertEqual(result.exit_code, 0)
    #
    # def test_014_no_params(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package])
    #     self.assertEqual(result.exit_code, 0)
    #
    # def test_015_inc_build(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--build"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertTrue("build[" in result.output)
    #
    # def test_016_inc_build(self):
    #     result = inc_build(self.package)
    #     # self.assertEqual(result.exit_code, 70)
    #     self.assertTrue("build[" in result)
    #
    # # ---------------------------------------------------------------------------------------------
    #
    # def test_300_create_error_SE_01300(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--create", "--dev"])
    #     self.assertEqual(result.exit_code, 1300)
    #
    # def test_301_newversion_error_SE_01301_1(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--newversion", "--dev"])
    #     self.assertEqual(result.exit_code, 1301)
    #
    # def test_301_newversion_error_SE_01301_2(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--newversion=23.3.0", "--dev"])
    #     self.assertEqual(result.exit_code, 1301)
    #
    # def test_302_dev_error_SE_01302(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--dev", "--patch"])
    #     self.assertEqual(result.exit_code, 1302)
    #
    # def test_303_rc_error_SE_01303(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--rc", "--patch"])
    #     self.assertEqual(result.exit_code, 1303)
    #
    # def test_304_patch_error_SE_01304(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--patch", "--post"])
    #     self.assertEqual(result.exit_code, 1304)
    #
    # def test_305_major_error_SE_01305(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--major", "--minor"])
    #     self.assertEqual(result.exit_code, 1305)
    #
    # def test_306_minor_error_SE_01306(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--minor", "--post"])
    #     self.assertEqual(result.exit_code, 1306)
    #
    # def test_307_build_error_SE_01307(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--build", "--post"])
    #     self.assertEqual(result.exit_code, 1307)
    #
    # def test_308_post_error_SE_01308(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--post", "--clean"])
    #     self.assertEqual(result.exit_code, 1308)
    #
    # def test_309_release_error_SE_01309(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--release", "--clean"])
    #     self.assertEqual(result.exit_code, 1309)
    #
    # # ---------------------------------------------------------------------------------------------
    # cleanTesting = False
    #
    # @skipIf(cleanTesting, "")
    # def test_310_clean(self):
    #     """ Cleanup testing folder: """
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--clean"])
    #     self.assertEqual(result.exit_code, 0)
    #
    # @skipIf(cleanTesting, "")
    # def test_310_clean_error_SE_01310(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package, "--clean"])
    #     self.assertEqual(result.exit_code, 1310)
    #
    # @skipIf(cleanTesting, "")
    # def test_311_clean_error_SE_01311(self):
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [self.package])
    #     self.assertEqual(result.exit_code, 1311)
    #
    # # ---------------------------------------------------------------------------------------------
    #
    # def test_900_SE_01100(self):
    #     """
    #     SE-01100: Could not package in ./app or ./
    #     """
    #     runner = CliRunner()
    #     result = runner.invoke(cli, [f'{self.package}_fail'])
    #     self.assertEqual(result.exit_code, 1100)
    #
    # # ---------------------------------------------------------------------------------------------
    #
    # @skipIf(cleanTesting, "")
    # def test_999_cleanup(self):
    #     """Remove `self.package` folder created during testing"""
    #     APP_DIR = os.getcwd()
    #     print("")
    #     print(f'       ROOT: {APP_DIR}')
    #     print(f'Test Folder: {APP_DIR}/{self.package.lower()}')
    #     for file in glob.glob(f'{APP_DIR}/{self.package.lower()}'):
    #         print(f'   Deleting: {file}')
    #         subprocess.run(["rm", "-rf", file])
