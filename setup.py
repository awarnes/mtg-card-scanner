import pathlib
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from db.db_manage import set_up_db, apply_patches

with open('README.md', 'r') as f:
    long_description = f.read()


class PostDevelopCommand(develop):
    """Post-installation command for development mode."""
    def run(self):
        develop.run(self)
        set_up_db()
        apply_patches()

class PostInstallCommand(install):
    """Post-installation command for installation mode."""
    def run(self):
        install.run(self)
        set_up_db()
        apply_patches()

setup(
    name="mtg-card-scanner",
    version="0.0.1",
    author="awarnes",
    description="Desktop application for managing MTG card collections.",
    long_description=long_description,
    url="https://github.com/awarnes/mtg-card-scanner",
    install_requires=pathlib.Path("requirements.txt").open().readlines(),
    # https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand
    }
)

