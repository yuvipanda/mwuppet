#!/usr/bin/env python
import os
import argparse
from mwapi import MWApi
from json import loads, dumps
import re
import getpass
from StringIO import StringIO
from PIL import Image
import requests

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

def get_page(page, firstline, fname):
    if not api.is_authenticated:
        ensure_logged_in()
    result = api.get(action="parse", page=page, prop="wikitext")
    wikitext = result["parse"]["wikitext"]["*"]
    f = open(fname, "w")
    f.write(firstline)
    f.write(wikitext.encode("UTF-8"))
    f.close()
    print "File " + fname + " updated."


def save_page(page, text, summary):
    if not api.is_authenticated:
        ensure_logged_in()

    result = api.post(action="edit", title=page, text=text, summary=summary, token=tokens['edittoken'])
    print result
    if 'captcha' in result['edit']:
        captcha_url = result['edit']['captcha']['url']
        url = "https://en.wikipedia.org" + captcha_url
        response = requests.get(url)
        i = Image.open(StringIO(response.content))
        i.show()
        captcha_id = result['edit']['captcha']['id']
        captcha_word = raw_input("Enter Captcha Word: ")
        print api.post(action="edit", title=page, text=text, summary=summary, token=tokens['edittoken'],captchaid=captcha_id,captchaword=captcha_word)

def process(text):
    global username
    pattern="{{USERNAME}}"
    return re.sub(pattern,username,text)

def main():
    parser = argparse.ArgumentParser(description="Sync code files with a Mediawiki installation")
    subparsers = parser.add_subparsers(dest="action")
    
    parser_push = subparsers.add_parser("push", help="push <filenames>")
    parser_push.add_argument("files", nargs="*")
    parser_push.add_argument("--message", default="/* Updated with mwuppet */")

    parser_pull = subparsers.add_parser("pull", help="pull <filenames>")
    parser_pull.add_argument("files", nargs="*")

    args = parser.parse_args()
    ensure_logged_in()
    
    for fname in args.files:
        f = open(fname)
        firstline = process(f.readline())
        page = parse_line(firstline)

        if (page):
            if args.action == "push":
                save_page(page, process(f.read()), args.message)
            elif args.action == "pull":
                get_page(page, firstline, fname)

if __name__ == "__main__":
    main()
