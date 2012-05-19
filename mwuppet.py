# page: User:Yuvipanda/test Booyeah
import os
import argparse
from mwapi import MWApi
from yaml import load
import time
import re

MODE_REGEX = re.compile(r'page:\s?(\S*)', re.I)

DEFAULT_HOST = "https://en.wikipedia.org"

def get_auth_config():
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

def get_config(path):
    conf_path = os.path.join(path, 'mwuppet.conf')
    return load(open(conf_path).read())

def save_page(page, text, summary):
    if not api.is_authenticated:
        config = get_auth_config()
        api.login(config["user"]["username"], config["user"]["password"])
        api.populateTokens()

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

    if not args.message:
        args.message = raw_input("Enter comit message: ")

    files = [os.path.join(args.path, name) for name in os.listdir(args.path) if name != "mwuppet.conf"]
    conf = get_config(args.path)

    api = MWApi(conf.get('host', DEFAULT_HOST))

    for fname in files:
        f = open(fname)
        page = conf['prefix'] + os.path.basename(fname)
        save_page(page, f.read(), args.message)
