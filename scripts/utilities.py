"""

Lorenz Data Assimilation

Simple of the Lorenz equations and the application of data assimilation methods.py

Scripted by dave.casson@usask.ca

"""

import configparser
import logging
import ast

def read_settings(settings_filename='settings.ini'):

    settings_reader = configparser.ConfigParser(allow_no_value=True)
    settings_reader.read(settings_filename)

    # Log the contents of the configuration file
    logging.info(f'The run configuration settings have been read from {settings_filename}')

    # Read all the configuration file elements into a dictionary
    settings_interim_dict = {sect: dict(settings_reader.items(sect)) for sect in settings_reader.sections()}
    # Remove the top level dict items, leaving only the key and value pairs
    settings = dict(ele for sub in settings_interim_dict.values() for ele in sub.items())

    #Convert numbers to floats
    for key, value in settings.items():
        try:
            settings[key] = int(value)
        except ValueError:
            try:
                settings[key] = float(value)
            except ValueError:
                settings[key] = str(value)

    return settings