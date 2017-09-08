"""Script for cloning the Wikibooks project „Mathe für Nicht-Freaks“ into a git
repository using the MediaWiki extension of git (see
https://github.com/Git-Mediawiki/Git-Mediawiki/wiki/User-manual for a manual
of this extension)."""

from functools import reduce
import os
import shutil
import shlex

import requests

from config import TARGET_DIR, URL, API_URL, PROJECT_NAME

def query_path(obj, path):
    """Returning the path `path` of the JSON object `obj`. Examples:

    >>>a = {"a": [1, 2, 3], "b": [{"foo": "bar"}]}
    >>>query_path(a, ["a"])
    [1,2,3]
    >>>query_path(a, ["a", 2])
    3
    >>>query_path(a, ["b", 0, "foo"])
    "bar"
    >>>query_path(a, ["b", 0, "foo"]) == a["b"][0]["foo"]
    True
    """
    return reduce(lambda x, y: x[y], path, obj)

def merge_obj(obj1, obj2):
    """Merges the objects `obj1` and `obj2` depending of there types."""
    if obj1 is None:
        return obj2
    elif isinstance(obj1, list):
        return obj1 + obj2
    elif isinstance(obj1, dict):
        result = obj1.clone()

        result.update(obj2)

        return result
    else:
        assert False

def query(params, path_to_result):
    """Performs a query using the MediaWiki API."""
    params["action"] = "query"
    params["format"] = "json"
    path_to_result = ["query"] + path_to_result
    result = None

    while True:
        api_result = requests.get(API_URL, params=params).json()
        result = merge_obj(result, query_path(api_result, path_to_result))

        if "continue" in api_result:
            params.update(api_result["continue"])
        else:
            return result

def quote_title(title):
    """Quote an article name of a MediaWiki page."""
    return title.replace(" ", "_")

def run_script():
    """Runs the script."""
    try:
        shutil.rmtree(TARGET_DIR)
    except FileNotFoundError:
        pass

    sites = query({"list": "allpages", "aplimit": 500,
                   "apprefix": PROJECT_NAME}, ["allpages"])
    sites_param = " ".join((quote_title(x["title"]) for x in sites))

    git_cmd = "git clone -c remote.origin.shallow=true " \
              "-c remote.origin.pages={} " \
              "mediawiki::{} {}".format(shlex.quote(sites_param),
                                        shlex.quote(URL), TARGET_DIR)

    os.system(git_cmd)

if __name__ == "__main__":
    run_script()
