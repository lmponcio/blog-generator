import logging
import json
import os
import markdown
import shutil
import datetime

########## defining functions for internal use
def _get_first_file_ending_in(ending, path):
    """Returns the first file ending in a specif way found in the given path"""
    log.debug("file ending in %s will be searched at %s", ending, path)
    # my_markup_path = ""
    if os.path.isdir(path):
        # log.debug("folder has been opened: %s", self.paths.bak_input)
        # nonlocal my_markup_path
        for dirname, subdirs, files in os.walk(path):
            # log.debug(
            #     "walking through files in input folder %s",
            #     self.paths.bak_input,
            # )
            # nonlocal my_markup_path
            for filename in files:
                # nonlocal my_markup_path
                if filename[-len(ending) :] == ending:
                    log.debug("file found: filename %s, dir %s", filename, dirname)
                    # nonlocal my_markup_path
                    return filename


def _clean_str_for_url(this_str):
    clean_str = ""
    lower = this_str.lower()
    for ch in lower:
        if ch.isalnum() or ch == "-" or ch == "_":
            clean_str += ch
        elif ch == "/" or ch == " ":
            clean_str += "-"
    return clean_str


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
        self._import_replace_keywords()
        self._import_post_info()

    ### methods for internal use
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
        html_lines = _markdown_file_to_html_list(markdown_path)
        html_string = "".join(html_lines)
        self.content = html_string

    ### methods
    def fill_template(self, markdown_path, template_path):
        self._import_post_content(markdown_path)
        # call this 5 times for post info (from post_info.json file)
        _replace_in_file(
            self._replace_keywords["html_title"], self.html_title, template_path
        )
        _replace_in_file(
            self._replace_keywords["post_title"], self.post_title, template_path
        )
        _replace_in_file(self._replace_keywords["date"], self.date, template_path)
        _replace_in_file(self._replace_keywords["img_src"], self.img_src, template_path)
        _replace_in_file(self._replace_keywords["img_url"], self.img_url, template_path)
        # call 1 more time for post content (from markdown file in input dir)
        _replace_in_file(self._replace_keywords["content"], self.content, template_path)


class PathsManager:
    def __init__(self):
        self.bak_input = None
        self.bak_markdowns = None
        self.bak_template = None
        self.blog_home = None
        self.blog_posts = None

        # import the paths after creating the path manager
        self._import_paths()

    def _import_paths(self):
        log.debug("importing paths from config.json")
        config_dict = _get_config_dict()
        self.bak_input = config_dict["paths"]["bak_input"]
        self.bak_markdowns = config_dict["paths"]["bak_markdowns"]
        self.bak_template = config_dict["paths"]["bak_template"]
        self.blog_home = config_dict["paths"]["blog_home"]
        self.blog_posts = config_dict["paths"]["blog_posts"]


class BlogUpdater:
    def __init__(self):
        self.paths = PathsManager()
        self.new_post = Post()

    def add_post(self):
        # add a new page
        # copying the template
        my_timestamp = datetime.datetime.now().strftime("%Y-%m-%d_")
        this_timestamp = my_timestamp
        this_title = _clean_str_for_url(self.new_post.post_title)
        log.debug(
            "attempting to join %s, %s, %s and %s",
            self.paths.blog_posts,
            this_timestamp,
            this_title,
            ".html",
        )
        post_path = os.path.join(
            self.paths.blog_posts, this_timestamp + this_title + ".html"
        )
        shutil.copy(self.paths.bak_template, post_path)

        # crating markup backup
        my_markup_filename = _get_first_file_ending_in(".md", self.paths.bak_input)
        input_markup = os.path.join(self.paths.bak_input, my_markup_filename)
        bak_markup = os.path.join(
            self.paths.bak_markdowns, this_timestamp + this_title + ".md"
        )
        log.debug(
            "input markup file %s will be saved as backup at %s",
            input_markup,
            bak_markup,
        )
        shutil.copy(input_markup, bak_markup)

        # filling template
        self.new_post.fill_template(bak_markup, post_path)
        # modify main blog page
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

    log.debug("creating new post")
    bu.add_post()

    # bu.new_post.fill_template(
    #     "/home/lmponcio/ProjectFiles/StaticGithub/blog-generator/blog-templates/tests/my_markdown.md",
    #     "/home/lmponcio/ProjectFiles/StaticGithub/blog-generator/blog-templates/tests/base.html",
    # )

    # log.debug("filling template")
    # bu.new_post.fill_template("hola")
