mwuppet is a Mediawiki Userscripts deploy tool. Use it to easily deploy your userscript bundles (JS/CSS/HTML) onto the wiki. Because copy pasting code into an edit box and hitting 'Save Page' sucks.

Installation:
-------------

<pre>(pip install | easy_install) python-mwuppet</pre>

How to Use:
-----------

<pre>
mwuppet push filename(s)
</pre>

filename(s): MediaWiki userscript that you want to deploy onto the wiki.

<pre>
mwuppet pull filename(s)
</pre>

filename(s): MediaWiki userscript that you want to update fron the wiki.


File Format:
-------------
The mediawiki_scriptname should be in the following format:

<pre>
Page:User:Wiki_username:path
</pre>

Example: page:User:Yuvipanda/wizard/wizard.js

Now according to the above example, the userscript wizard.js will be deployed to/updated from http://en.wikipedia.org/wiki/User:Yuvipanda/wizard/wizard.js

Note:
-----
1) Old user of mwuppet, make sure that you delete ~/.mwuppet and try the script.
