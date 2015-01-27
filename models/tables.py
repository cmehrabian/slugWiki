# coding: utf8
from datetime import datetime
import re
import unittest

# Format for wiki links.
RE_LINKS = re.compile('(<<)(.*?)(>>)')

db.define_table('pagetable' # Name 'page' is reserved unfortunately.
    # Complete!
    )


db.define_table('revision',
    # Complete!
    Field('body', 'text'), # This is the main content of a revision.
    )

def create_wiki_links(s):
    """This function replaces occurrences of '<<polar bear>>' in the 
    wikitext s with links to default/page/polar%20bear, so the name of the 
    page will be urlencoded and passed as argument 1."""
    def makelink(match):
        title = match.group(2).strip()
        return '[[%s %s]]' % (title, URL('default', 'index', args=[title]))
    return re.sub(RE_LINKS, makelink, s)

def represent_wiki(s):
    """Representation function for wiki pages."""
    return MARKMIN(create_wiki_links(s))

def represent_content(v, r):
    """In case you need it."""
    return represent_wiki(v, None)

# We associate the wiki representation with the body of a revision.
db.revision.body.represent = represent_content
