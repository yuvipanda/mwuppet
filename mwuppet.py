# page: User:Yuvipanda/test Booyeah
import os
import argparse
from mwapi import MWApi
from yaml import load
import time
import re

MODE_REGEX = re.compile(r'page:\s?(\S*)', re.I)

DEFAULT_HOST = "https://en.wikipedia.org"

api = None
user_config = None

def get_user_config():
    config_path = os.path.expanduser("~/.mwuppet")
    if os.path.exists(config_path):
        config = load(open(config_path).read())
    else:
        config = {
            "user": {
                "username": raw_input("Enter your user name: "),
                "password": raw_input("Enter your password: ")
            }
        }
    return config

def get_project_config(path):
    conf_path = os.path.join(path, 'mwuppet.conf')
    return load(open(conf_path).read())

def save_page(page, text, summary):
    print api.post({
        "action": "edit",
        "title": page,
        "text": text,
        "summary": summary,
        "token": api.tokens["edittoken"]
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync code files with a Mediawiki installation")
    parser.add_argument("path")
    parser.add_argument("--message")

    args = parser.parse_args()

    user_config = get_user_config()

    if not args.message:
        args.message = raw_input("Enter comit message: ")

    files = [os.path.join(args.path, name) for name in os.listdir(args.path) if name != "mwuppet.conf"]
    project_config = get_project_config(args.path)

    api = MWApi(project_config.get('host', DEFAULT_HOST))
    api.login(user_config["user"]["username"], user_config["user"]["password"])
    api.populateTokens()

    project_config['prefix'] = 'User:' + user_config['user']['username'] + '/' + project_config['name'] + '/'

    for fname in files:
        f = open(fname)
        page = project_config['prefix'] + os.path.basename(fname)

        save_page(page, f.read(), args.message)
