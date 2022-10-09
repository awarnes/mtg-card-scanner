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
    install_requires=[
        "fuzzywuzzy==0.18.0"
        "numpy==1.23.2"
        "opencv-python==4.6.0.66"
        "packaging==21.3"
        "Pillow==9.2.0"
        "pyparsing==3.0.9"
        "PySide6==6.3.1"
        "PySide6-Addons==6.3.1"
        "PySide6-Essentials==6.3.1"
        "pytesseract==0.3.10"
        "shiboken6==6.3.1"
    ],
    # https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    }
)

