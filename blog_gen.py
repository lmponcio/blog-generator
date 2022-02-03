import logging
import json
import os
import markdown

########## defining functions for internal use


def _get_config_dict():
    folder_path = os.path.dirname(os.path.realpath(__file__))
    basename = "config.json"
    json_file_path = os.path.join(folder_path, basename)
    return json.load(open(json_file_path, "r"))


def _get_post_info_dict():
    folder_path = os.path.dirname(os.path.realpath(__file__))
    basename = "post_info.json"
    json_file_path = os.path.join(folder_path, basename)
    return json.load(open(json_file_path, "r"))


def _markdown_file_to_html_list(input_path):
    """translates the markdown file by returning a list of lines of code in html"""
    temp_file_dir = os.path.dirname(os.path.realpath(__file__))
    temp_file_path = os.path.join(temp_file_dir, "temp_file.html")
    html = markdown.markdownFromFile(
        input=input_path,
        output=temp_file_path,
    )
    f = open(temp_file_path, "r")
    lines = f.readlines()
    print(lines)
    os.remove(temp_file_path)
    return lines


def _replace_in_file(replace_keyword, new_text, path):
    with open(path, "r") as file:
        data = file.read()
        print(data)
        data = data.replace(replace_keyword, new_text)

    with open(path, "w") as file:
        file.write(data)
        print()


########## defining classes


class Post:
    def __init__(self):
        self.html_title = None
        self.post_title = None
        self.date = None
        self.img_src = None
        self.img_url = None
        self.content = None
        self._replace_keywords = None

    def _import_replace_keywords(self):
        config_dict = _get_config_dict()
        self._replace_keywords = config_dict["replace_keywords"]

    def _import_post_info(self):
        post_info_dict = _get_post_info_dict()
        self.html_title = post_info_dict["html_title"]
        self.post_title = post_info_dict["post_title"]
        self.date = post_info_dict["date"]
        self.img_src = post_info_dict["img_src"]
        self.img_url = post_info_dict["img_url"]

    def _import_post_content(self, markdown_path):
        # the post content has to be converted to a string(it comes as a big list of lines)
        pass

    def fill_template(self, markdown_path, template_path):
        self._import_replace_keywords()
        self._import_post_info()
        self._import_post_content(self, markdown_path)
        # call this 5 times for post info
        _replace_in_file(replace_keyword, new_text, path)
        _replace_in_file(replace_keyword, new_text, path)
        _replace_in_file(replace_keyword, new_text, path)
        _replace_in_file(replace_keyword, new_text, path)
        _replace_in_file(replace_keyword, new_text, path)
        # call 1 more time for post content
        _replace_in_file(replace_keyword, new_text, path)


class PathsManager:
    def __init__(self):
        self.bak_input = None
        self.bak_markdowns = None
        self.bak_templates = None
        self.blog_home = None
        self.blog_posts = None

    def import_paths(self):
        config_dict = _get_config_dict()
        self.bak_input = config_dict["paths"]["bak_input"]
        self.bak_markdowns = config_dict["paths"]["bak_markdowns"]
        self.bak_templates = config_dict["paths"]["bak_templates"]
        self.blog_home = config_dict["paths"]["blog_home"]
        self.blog_posts = config_dict["paths"]["blog_posts"]


class BlogUpdater:
    def __init__(self):
        self.paths = PathsManager()
        self.new_post = Post()

    def add_post(self):
        # first it has to add a blog

        # after that it has to update the main blog page
        pass


if __name__ == "__main__":
    # configuring logging
    # create logger
    log = logging.getLogger("blog_gen")
    log.setLevel(logging.DEBUG)

    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # file handler
    fh = logging.FileHandler("blog_gen.log", "w")
    fh.setLevel(logging.DEBUG)

    # formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    )

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    log.addHandler(ch)
    log.addHandler(fh)

    # log configuration ends here
    #############################

    log.debug("creating blog updater object")
    bu = BlogUpdater()

    log.debug("importing paths from config file")
    bu.paths.import_paths()

    log.debug("filling template")
    bu.new_post.fill_template("hola")
