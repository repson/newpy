# fileconf.py
# Copyright (C) 2020 Stefan Gal (stefan.mail.sk@gmail.com) and contributors
#
# This module is part of NewPy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from configparser import ConfigParser, Error, ParsingError
from colorama import init, Fore, Style
from shutil import copyfile
import os
import re

from errors import MissingConfigFileError, MissingSectionError, MissingOptionError
# from builder import Builder


class MissingFileSectionError(ParsingError):
    """
    Raised when a key-value pair is found before any section header.
    """
    def __init__(self, filename, line):
        Error.__init__(
            self, 'File contains no section headers.\nfile: %r,\n%r' %
            (filename, line))
        self.source = filename
        self.line = line
        self.args = (filename, line)


class ConfigBuildCheck:
    """For checking and building the config.ini file"""
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_PATH = os.path.join(ROOT_DIR, 'config.ini')
    CONFIG_TEMPLATE_FILE_PATH = os.path.join(ROOT_DIR, 'templ_config.ini')

    def __init__(self):
        init()
        self.template_config = ConfigParser()
        self.template_config.read(self.CONFIG_TEMPLATE_FILE_PATH)
        self.config = ConfigParser()
        self.config.read(self.CONFIG_FILE_PATH)

    def new_config_file(self):
        """Generate new config.ini file."""
        try:
            copyfile(self.CONFIG_TEMPLATE_FILE_PATH, self.CONFIG_FILE_PATH)
            print(f"\n{Fore.GREEN} + CREATED: {self.CONFIG_FILE_PATH}")
        except Exception as e:
            print(
                f"\n{Fore.RED} + FAILED TO CREATE: {self.CONFIG_FILE_PATH}\n")
            raise e
        finally:
            print(Style.RESET_ALL)

    def check_sections_ok(self) -> bool:
        """Check sections available compared to the template in the config file."""
        missing_section, missing_line_nr = [], []
        for section in self.template_config.sections():
            if section not in self.config.sections():
                with open(self.CONFIG_TEMPLATE_FILE_PATH, 'r') as file:
                    for line_nr, line in enumerate(file, 1):
                        if section in line:
                            missing_section.append(section)
                            missing_line_nr.append(line_nr)
        if missing_section:
            raise MissingFileSectionError(
                self.CONFIG_FILE_PATH,
                f'{Fore.RED} + Missing section: {missing_section} on lines {missing_line_nr}'
            )
        return True

    def check_options_ok(self) -> bool:
        """Check options available compared to the template in the config file."""
        structure, missing_option = [], []
        file_ok = True
        for section in self.config.sections():
            for option in self.config.options(section):
                structure.append((section, option))
        for section in self.template_config.sections():
            for option in self.template_config.options(section):
                if (section, option) not in structure:
                    file_ok = False
                    missing_option.append(str(section + "->" + option))
        if not file_ok:
            raise Error(
                f"{Fore.RED} + Missing or corrupt option: {missing_option}")
        return file_ok


class ConfigRead:
    """
    Read in the config.ini data.
    """

    _CONFIG_FILE = "config/config.ini"

    def __init__(self):
        self.config = ConfigParser()
        if not len(self.config.read(self._CONFIG_FILE)):
            raise MissingConfigFileError(self._CONFIG_FILE)

    # def config_file_test(self):
    #     # 'newpy/config.ini' is available?
    #     if os.path.exists(self._CONFIG_FILE):
    #         print("Configuration file 'config.ini' available\n".rjust(15))
    #         return True
    #     else:
    #         raise MissingConfigFileError(self._CONFIG_FILE)
    #         # raise MissingConfigFileError("Config.ini file is missing or filename is incorrect! Check for config/config.ini")

    def project_in_config_check(self):

        self.PATH = self.config["PROJECT"]["projectpath"]
        self.FILE = self.config["PROJECT"]["projectname"]
        self.PROJECT_PATH = os.path.join(self.PATH, self.FILE)
        print(self.PROJECT_PATH)
        if os.path.exists(self.PROJECT_PATH):
            return True
        # builder = Builder(self.PROJECT_PATH, self.config)
        # builder.folder_structure()

    def pypi_in_config_check(self):
        author = self.config['PYPI']['Author']
        author_email = self.config['PYPI']['AuthorEmail']
        _pattern_email = "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}"
        email_format = re.search(_pattern_email, author_email)
        description = self.config['PYPI']['Description']
        version = self.config['PYPI']['Version']
        release = self.config['PYPI']['Release']
        return all([author, email_format, description, version, release])

    @property
    def get_project_name(self):
        return self.FILE if self.FILE else None

    @property
    def get_project_path(self):
        return self.PATH if self.PATH else None

    @property
    def get_project_folder(self):
        return os.path.join(self.get_project_path, self.get_project_name)


if __name__ == "__main__":
    # cbc = ConfigBuildCheck()
    # run.new_config_fi0jnuih76tle()
    # cbc.check_sections_ok()
    # cbc.check_options_ok()
    cr = ConfigRead()
    cr.project_in_config_check()