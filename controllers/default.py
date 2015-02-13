# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#Non Trivial - diciqde for yourself what you do with the forms

import logging

def index():
    # title = request.args(0) or 'SlugWiki'
    # #sorts title
    # title = title.lower()
    # #sets title to var display_title
    # title_name = title.title()
    # def GetData(form):
    #    return form.vars.pagetable()


    #set all titles and set it var pajes
    pajes = db().select(db.pagetable.ALL)
    #instantiate form
    form = SQLFORM(db.pagetable)
    #if the form is submitted
    if form.process().accepted:
        #set the title to var
        record = form.vars.title  
        # if the first selection of the query doesn't -> lets add it      
        if db(db.pagetable.title == record).select().first() is None:
            #flash them an add notice
            session.flash = T('Page added')
            #redirct them to an add page
            redirect(URL('default', 'home', args=[record],vars=dict(edit='true')))
        else:
            #otherwise flash them an not found, and send to make it
            session.flash = T('Page found')
            redirect(URL('default', 'home', args=[record]))





        # title = request.args(0)
        # title_name = title.title()
        #if db(db.pagetable.title == title).select().first() is None:
        #send you to default/new/{{title}} to add it
            #redirect(URL('default', 'new', args=[title]))
        #else:
            #redirect(URL('default', 'home', args=[title]))
            # rev.update_record(body=form.vars.body)
            # redirect(URL('default', 'home', args=[title]))
    # title = request.args(0)
    #title = title.lower()
    # display = title.title()

    return dict(pajes=pajes, form=form)

def home():

    #sets the first page topic
    title = request.args(0) or 'SlugWiki'
    #sorts title
    title = title.lower()
    #sets title to var title_name
    title_name = title.title()
    #if the this is the first instance of title send 
    if db(db.pagetable.title == title).select().first() is None:
        #send you to default/new/{{title}} to add it
        redirect(URL('default', 'new', args=[title]))
    #lets set page_id as the id of that first selection
    page_id = db(db.pagetable.title == title).select().first().id
    #old revision is set to var rev which selects first item of the list reversed order of time created
    rev = db(db.revision.pagetable_id == page_id).select(orderby=~db.revision.date_created).first()
    # s is set to the body of that revision
    # rev.body = "default"
    s = rev.body
    #if user wants to edit ?edit=y will attach to URL
    editing = request.vars.edit == 'y'
    #if we are editing
    if editing:
        #lets create a form with custom paras body, type text, labeled and set to previous rev
        form = SQLFORM.factory(Field('body', 'text', label='Content', default=s))
        #create a cancel button that directs us back to index
        form.add_button('Cancel', URL('default', 'index', args=[all]))
        #hist button
        form.add_button('History', URL('default', 'history', args=[title]))
        #if form is accepted
        if form.process().accepted:
            db.revision.insert(author = auth.user_id, body=form.vars.body, pagetable_id = page_id)
            #update revision with new body
            rev.update_record(body=form.vars.body)
            #direct them back to 
            redirect(URL('default', 'home', args=[title]))
        #set content to the form we declared
        content = form
    else:
        #otherwise set the content to the previous body
        content = s
    #create button edit that directs us to home/{{title}}
    button = A('edit', _class='btn', _href=URL('default', 'home', args=[title], vars=dict(edit='y')))
    #return the dictionary
    return dict(title_name=title_name,
                button = button,
                content = content,
                editing = editing)


    #page = db(db.pagetable.title == title).select().first()
    
    # You have to serve to the user the most recent revision of the 
    # page with title equal to title.
    
    # Let's uppernice the title.  The last 'title()' below
    # is actually a Python function, if you are wondering.
    

    
    # Here, I am faking it.  
    # Produce the content from real database data. 
   # content = represent_wiki("I like <<Slugs>>s and <<pussies>>.")
    
    #return dict(display_title=display_title, content=content, pages=pages)


    #lecture notes to quickly JOT



def new():
    #set var title to the last thing in the URL
    title = request.args(0)
    #set var to pass with msg asking to create
    content = "Create page for %s?" % (title)
    #create anchor button labeled:Create page, that directs you to /default/create/{{title}}
    create_button = A('Create page', _class='btn', _href=URL('default', 'create', args=[title]))
    #create anchor button labeled:Cancel, that directs you back to /default/index
    cancel_button = A('Cancel', _class='btn', _href=URL('default', 'index'))
    #function returns a dictionary of variables: msg, btns and title
    return dict(content = content,
        create_button = create_button,
        cancel_button = cancel_button,
        title = title
        )

def create():
    #set title as last var on the URL
    title = request.args(0)
    #set up SQLfactory form to produce a form with body - format to text, with placeholder of 'Content'
    form = SQLFORM.factory(Field('body', 'text', 
                                  label='Content'))
    #add a button labeled Cancel that directs you to default/index
    form.add_button('Cancel', URL('default', 'index'))
    #if
    if form.process().accepted:
        #add the title to the database pagetable
        db.pagetable.insert(title=title)
        #set up a var that represents the title, specifically the most recent entry to db
        page_id = db(db.pagetable.title == title).select().first().id
        #add author id, body content and page id to revisions database
        db.revision.insert(author = auth.user_id, body=form.vars.body, pagetable_id = page_id)
        #get redirected back to default/index/{{title}}
        redirect(URL('default', 'index', args=[title]))
    #return a dictionary or form and title
    return dict(form = form, title = title)

def history():
    #title set to last > URL
    title = request.args(0)
    page_id = db(db.pagetable.title == title).select().first().id
    rev = db(db.revision.pagetable_id == page_id).select(orderby=~db.revision.date_created)
    revising = request.vars.rev == 'y'
    if revising:
        rev_id = request.args(1)
        rev = db(db.revision.id == rev_id).select().first()
        db.revision.insert(author = auth.user_id, body=rev.body, pagetable_id = page_id)
        redirect(URL('default', 'home', args=[title]))
    return dict(title =title, rev=rev)


# @auth.requires_login()
# def add():
#     #get first
#     #p = db.revision(0)
#     #find most recent revision and set it previous_text
#     #previous_text = p.body
#     #previous_title = p.title

#     form = SQLFORM.factory(
#         Field('title'),
#         # Field('body', 'text'), #default=previous_text),
#         # Field('page_reference'), #'integer', requires=IS_INT_IN_RANGE(0, 1000), default=831),
#         # Field('author'), #use author login
#         # Field('date_posted', 'datetime')
#         )
#     if form.process().accepted:
#         #insert into table
#         #where did it go? forms.vars.id
#         id = db.pagetable.insert(title = form.vars.title,
#                                 # body = form.vars.body,
#                                 # #page_reference = previous_text,
#                                 # author = form.vars.author,
#                                 # date_posted = form.vars.date_posted,
#                                 )
#         #write to any table
#         # db.pagetable.insert(item_id = id,
#         #                     title = "this is a log",
#         #                     special = "no"
#         #                     )
#         session.flash = T("inserted")
#         redirect(URL('default', 'edit'))
#     return dict(form=form)

# @auth.requires_login()
# def edit():
#     # p = db.returnevision(0)
#     # previous_title = p.title

#     form = SQLFORM.factory(
#         Field('title'), #default=previous_title),
#         Field('body', 'text'), #default=previous_text),
#         Field('page_reference'), #'integer', requires=IS_INT_IN_RANGE(0, 1000), default=831),
#         Field('author'), #use author login
#         Field('date_posted', 'datetime')
#         )
#     if form.process().accepted:
#         #insert into table
#         #where did it go? forms.vars.id
#         id = db.revision.insert(title = form.vars.title,
#                                 body = form.vars.body,
#                                 #page_reference = previous_text,
#                                 author = form.vars.author,
#                                 date_posted = form.vars.date_posted,
#                                 )
#     def validate_edit_form(form):
#         if form.vars.body != '':
#             form.errors.body = T('Insert something more')
#         elif form.vars.body != '1':
#             form.errors.body = T('Insert some letters')

    #p = db.revision(request.args(0)) or redirect(URL('default', 'index'))
    # if p.user_id != auth.user_id:
    #     session.flash = T('Not authorized')
    #     redirect(URL('default', 'index'))
    # form = SQLFORM(db.revision, record=p)
    # if form.process(onvalidate=validate_edit_form).accepted: #edit_plus_validation(p)
    #     session.flash = T('Updated')
    #     redirect(URL('default', 'index', args=[p.id]))
    # return dict(form=form)

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
    
    
    # Let's uppernice the title.  The last 'title()' below
    # is actually a Python function, if you are wondering.
    title_name = title.title()
    
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
    return dict(title_name=title_name, content=content, editing=editing)


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
