# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#Non Trivial - dicide for yourself what you do with the forms

import logging


def index():
    """
    This is the main page of the wiki.  
    You will find the title of the requested page in request.args(0).
    If this is None, then just serve the latest revision of something titled "Main page" or something 
    like that. 
    """
    # p = db().select(db.pagetable.ALL)

    title = request.args(0) or 'main page'
    # You have to serve to the user the most recent revision of the 
    # page with title equal to title.
    
    # Let's uppernice the title.  The last 'title()' below
    # is actually a Python function, if you are wondering.
    display_title = title.title()

    
    # Here, I am faking it.  
    # Produce the content from real database data. 
    content = represent_wiki("I like <<Slugs>>s")
    
    return dict(display_title=display_title, content=content)

@auth.requires_login()
def add():
    #get first
    p = db.revision(1)
    #find most recent revision and set it previous_text
    #previous_text = p.body

    form = SQLFORM.factory(
        Field('title'),
        Field('body', 'text'), #default=previous_text),
        Field('page_reference'), #'integer', requires=IS_INT_IN_RANGE(0, 1000), default=831),
        Field('author'), #use author login
        Field('date_posted', 'datetime')
        )
    if form.process().accepted:
        #insert into table
        #where did it go? forms.vars.id
        id = db.revision.insert(title = form.vars.title,
                                body = form.vars.body,
                                #page_reference = previous_text,
                                author = form.vars.author,
                                date_posted = form.vars.date_posted,
                                )
        #write to any table
        # db.pagetable.insert(item_id = id,
        #                     title = "this is a log",
        #                     special = "no"
        #                     )
        session.flash = T("inserted")
        redirect(URL('default', 'index'))
    return dict(form=form)

@auth.requires_login()
def edit():

    def validate_edit_form(form):
        if form.vars.body != '':
            form.errors.body = T('Insert something more')
        elif form.vars.body != '1':
            form.errors.body = T('Insert some letters')

    p = db.revision(request.args(0)) or redirect(URL('default', 'index'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized')
        redirect(URL('default', 'index'))
    form = SQLFORM(db.revision, record=p)
    if form.process(onvalidate=validate_edit_form).accepted: #edit_plus_validation(p)
        session.flash = T('Updated')
        redirect(URL('default', 'index', args=[p.id]))
    return dict(form=form)

#alternative

# def edit_plus_validation(previous_rec):
#     def validate_edit_form(form):
#         if form.vars.body != '':
#             form.errors.body = T('Insert something more')
#         elif form.vars.body != '1':
#             form.errors.body = T('Insert some letters')
#         if previous_rec.area_code is not None form.vars.body ! = p.body:
#             form.errors.body = T('Insert something more')
#     return validate_edit_form



def test():
    """This controller is here for testing purposes only.
    Feel free to leave it in, but don't make it part of your wiki.
    """
    title = "This is the wiki's test page"
    form = None
    content = None
    
    # Let's uppernice the title.  The last 'title()' below
    # is actually a Python function, if you are wondering.
    display_title = title.title()
    
    # Gets the body s of the page.
    r = db.testpage(1)
    s = r.body if r is not None else ''
    # Are we editing?
    editing = request.vars.edit == 'true'
    # This is how you can use logging, very useful.
    logger.info("This is a request for page %r, with editing %r" %
                 (title, editing))
    if editing:
        # We are editing.  Gets the body s of the page.
        # Creates a form to edit the content s, with s as default.
        form = SQLFORM.factory(Field('body', 'text',
                                     label='Content',
                                     default=s
                                     ))
        # You can easily add extra buttons to forms.
        form.add_button('Cancel', URL('default', 'test'))
        # Processes the form.
        if form.process().accepted:
            # Writes the new content.
            if r is None:
                # First time: we need to insert it.
                db.testpage.insert(id=1, body=form.vars.body)
            else:
                # We update it.
                r.update_record(body=form.vars.body)
            # We redirect here, so we get this page with GET rather than POST,
            # and we go out of edit mode.
            redirect(URL('default', 'test'))
        content = form
    else:
        # We are just displaying the page
        content = s
    return dict(display_title=display_title, content=content, editing=editing)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
