#!/usr/bin/env python
import os
import argparse
from mwapi import MWApi
from json import loads, dumps
import re
import getpass

MODE_REGEX = re.compile(r'page:\s?(\S*)', re.I)

api = MWApi('https://en.wikipedia.org')
tokens = None
username = ""

def ensure_logged_in():
    global tokens
    global username
    cookies_path = os.path.expanduser("~/.mwuppet")
    if os.path.exists(cookies_path):
        data = loads(open(cookies_path).read())
        cookies = data['cookies']
        username = data['username']
        api.set_auth_cookie(cookies)
        tokens = api.get_tokens()
        # This way, we can be sure that we're actually logged in, and the token never really expires!
        if tokens['edittoken'] != '+\\':
            return

    # If it reaches here, that means we don't have a valid login
    username = raw_input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    api.login(username, password)
    
    cookies = api.get_auth_cookie()
    tokens = api.get_tokens()
    open(cookies_path, 'w').write(dumps({
        'tokens': tokens,
        'cookies': cookies,
        'username': username
    }))

def parse_line(line):
    match = MODE_REGEX.search(line)
    if match:
        return match.group(1)
    else:
        return False

def save_page(page, text, summary):
    print api.post(action="edit", title=page, text=text, summary=summary, token=tokens['edittoken'])

def process(text):
    global username
    pattern="{{USERNAME}}"
    return re.sub(pattern,username,text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync code files with a Mediawiki installation")
    parser.add_argument("files", nargs="*")
    parser.add_argument("--message", default="/* Updated with mwuppet */")

    args = parser.parse_args()
    ensure_logged_in()

    for fname in args.files:
        f = open(fname)
        firstline = process(f.readline())
        page = parse_line(firstline)
        
        if(page):
            save_page(page, process(f.read()), args.message)