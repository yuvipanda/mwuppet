#!/usr/bin/env python
import os
import argparse
from mwapi import MWApi
from yaml import load
import time
import re

MODE_REGEX = re.compile(r'page:\s?(\S*)', re.I)

api = MWApi('http://en.wikipedia.org')

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

def parse_line(line):
    match = MODE_REGEX.search(line)
    if match:
        return match.group(1)
    else:
        return False

def save_page(page, text, summary):
    if not api.is_authenticated:
        config = get_user_config()
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
    parser.add_argument("--files", nargs="*")
    parser.add_argument("--message", default="/* Updated with mwuppet */")

    args = parser.parse_args()

    for fname in args.files:
        f = open(fname)
        firstline = f.readline()
        page = parse_line(firstline)
        if(page):
            save_page(page, f.read(), args.message)

