from functools import partial
import click.testing
import pytest
import zeit.deploynotify.cli


@pytest.fixture(scope='session')
def cli():
    runner = click.testing.CliRunner()
    return partial(runner.invoke, zeit.deploynotify.cli.cli)


def test_cli_imports_all_modules(cli):
    assert cli(['--help']).exit_code == 0
