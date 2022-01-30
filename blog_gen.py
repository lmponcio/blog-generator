import logging
import json
import os
import markdown


def config_logging():
    # create logger
    log = logging.getLogger("simple_example")
    log.setLevel(logging.DEBUG)

    # create console handler and set level to error
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create file handler and set level to debug
    fh = logging.FileHandler("blog_gen.log", "w")
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    )

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    log.addHandler(ch)
    log.addHandler(fh)


def markdown_file_to_html_list(input_path):
    """translates the markdown file by returning a list of lines of code in html"""
    temp_file_name = "temp_file.html"
    temp_file_dir = os.path.dirname(os.path.realpath(__file__))
    temp_file_path = os.path.join(temp_file_dir, temp_file_name)
    html = markdown.markdownFromFile(
        input=input_path,
        output=temp_file_path,
    )
    f = open(temp_file_path, "r")
    lines = f.readlines()
    print(lines)
    os.remove(temp_file_path)
    return lines


class JsonImporter:
    def __init__(self):
        # the json file should be in the same folder
        folder_path = os.path.dirname(os.path.realpath(__file__))
        basename = "config.json"
        self.json_file_path = os.path.join(folder_path, basename)

    def get_json(self):
        return json.load(open(self.json_file_path, "r"))


if __name__ == "__main__":
    # configuring logging
    config_logging()

    # importing config.json
    importer = JsonImporter()
    my_conf = importer.get_json()

    # pending:
    ## create a object that (1)opens the html template (2)inserts html lines previously converted into the right place and
    ## (3)saves the html new file
