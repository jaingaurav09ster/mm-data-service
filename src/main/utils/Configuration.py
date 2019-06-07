import json
import argparse


def load_json_config(config_path):
    """
    Function to load config from a json file.

    :param config_path: path to the config file. Can be relative or absolute.
    :return: Dictionary containing the JSON parsed config file. If file is not found, will raise a FileNotFoundError. If
    the JSON is not specified correctly, it will raise a JSONParse Error.
    """
    with open(config_path, 'rt') as f:
        # return yaml.safe_load(f.read())
        return json.load(f)


def argparse_cmd_line(cmd_line_args):
    """
    Function to parse arguments from the command line in the format of script_run --arg1=val1 --arg2=val2.

    :param cmd_line_args: list containing the name of command line arguments to parse, e.g ['arg1', 'arg2']
    :return: the parsed argument object. Values can be retrieved for example as 'parsed_obj.arg1'
    """
    # argparse and get the argument inputs
    parser = argparse.ArgumentParser(description='Process the command line args.')
    for arg_name, description in cmd_line_args.items():
        parser.add_argument('--{}'.format(arg_name), help=description)
    return parser.parse_args()
