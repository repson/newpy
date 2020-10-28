# cli-builder.py
# Copyright (C) 2020 Stefan Gal (stefan.mail.sk@gmail.com) and contributors
#
# This module is part of NewPy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
# pylint: disable=no-name-in-module

import os
import click
import logging
from .license import NewLicense
# from setup_manger import PrepareSetup

logging.Handler(level=logging.DEBUG)
logging.getLogger(__name__)


class Builder:
    license_set = ('afl3', 'agpl3', 'apache', 'bsd2', 'bsd3', 'cc0', 'cc_by',
                   'cc_by_nc', 'cc_by_nc_nd', 'cc_by_nc_sa', 'cc_by_nd',
                   'cc_by_sa', 'cddl', 'epl', 'gpl2', 'gpl3', 'isc', 'lgpl',
                   'mit', 'mpl', 'wtfpl', 'zlib')

    def __init__(self, project_name, lic_type):
        self.lic_type = lic_type
        self.curr_working_dir = os.getcwd()
        self.project_name = project_name
        self.project_path = os.path.join(self.curr_working_dir,
                                         self.project_name)

        self.folder_structure()

    def folder_structure(self):
        """Building folders: PROJECT, test and docs folders"""

        # if os.path.exists(self.project_path):
        print("\n")
        os.mkdir(path=os.path.join(self.curr_working_dir, self.project_name))
        self._build_test_folder()
        self._build_docs_folder()
        self._build_readme_md()
        # self.build_setup_py()
        # self.build_requirements_txt()
        # self.build_gitignore()

    def _build_test_folder(self):
        test_path = os.path.join(self.project_path, "tests")
        try:
            os.mkdir(path=test_path)
            print("Test path: ", test_path)
        except Exception as e:
            logging.error('Issue creating tests folder ', e)

    def _build_docs_folder(self):
        docs_path = os.path.join(self.project_path, "docs")
        try:
            os.mkdir(path=docs_path)
            print("Docs path: ", docs_path)
        except Exception as e:
            logging.error('Issue creating docs folder ', e)

    def _build_readme_md(self):
        try:
            with open(os.path.join(self.project_path, "README.md"),
                      "w") as file:
                return file
        except Exception as e:
            logging.error('Issue creating README.md file ', e)

    def build_license(self, lic_type):
        lic = NewLicense()
        try:
            if lic_type in self.license_set:
                lic.download(self.project_path, lic_type)
                print("LICENSE type: ", lic_type)
            else:
                lic.download(self.project_path, 'mit')
                print("LICENSE type incorrect. Using as default: ", lic_type)
        except Exception as e:
            logging.error('Issue to create LICENSE file ', e)

    # def build_setup_py(self):
    #     ps = PrepareSetup()
    #     ps.fill_setup_template(self.PROJECT_PATH)

    # def build_requirements_txt(self):
    #     with open(os.path.join(self.PROJECT_PATH, "requirements.txt"), "w") as file:
    #         pass

    # def build_gitignore(self):
    #     with open(os.path.join(self.PROJECT_PATH, ".gitignore"), "w") as file:
    #         pass


# @click.command()
# @click.option('--proj_name',
#               default='project',
#               help='This will be the folder name & project name.')
# def startnew(proj_name):
#     Builder(proj_name)

# if __name__ == "__main__":

#     startnew()