# coding: utf8
from datetime import datetime
import re
import unittest


# Format for wiki links.
RE_LINKS = re.compile('(<<)(.*?)(>>)')

db.define_table('pagetable', # Name 'page' is reserved unfortunately.
    # Complete!
    Field('title')
    )
#need to cross these tables revision of title
db.define_table('revision',
    # Complete!
   # Field('title', db.pagetable), #reference
    Field('pagetable_id', db.pagetable),
    #Field('page_reference', 'reference db.pagetable'),
    Field('body', 'text', default="content"),
     # This is the main content of a revision.
    #Field('user_id', db.auth_user), #use this instead of author?
    Field('author', db.auth_user),
    Field('date_created', 'datetime', default=request.now),
    )

db.define_table('testpage',
    # This table is used for testing only.  Don't use it in your code,
    # but feel free to look at how I use it. 
    Field('body', 'text'),
    )

#db.revision.date_posted.default = datetime.utcnow()
#db.revision.name.default = get_first_name()
# db.revision.body.default = "Content"

db.revision.body.represent = IS_NOT_EMPTY()
#db.revision.body.represent = represent_content
# db.pagetable.title.requires = IS_NOT_IN_DB(db, 'pagetable.title')

def create_wiki_links(s):
    """This function replaces occurrences of '<<polar bear>>' in the 
    wikitext s with links to default/page/polar%20bear, so the name of the 
    page will be urlencoded and passed as argument 1."""
    def makelink(match):
        # The tile is what the user puts in
        title = match.group(2).strip()
        # The page, instead, is a normalized lowercase version.
        page = title.lower()
        return '[[%s %s]]' % (title, URL('default', 'index', args=[page]))
    return re.sub(RE_LINKS, makelink, s)

def represent_wiki(s):
    """Representation function for wiki pages.  This takes a string s
    containing markup language, and renders it in HTML, also transforming
    the <<page>> links to links to /default/index/page"""
    return MARKMIN(create_wiki_links(s))

def represent_content(v, r):
    """In case you need it: this is similar to represent_wiki, 
    but can be used in db.table.field.represent = represent_content"""
    return represent_wiki(v)

# We associate the wiki representation with the body of a revision.