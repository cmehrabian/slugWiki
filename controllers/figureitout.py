#How to INSERT a revision in the page

r = db.revision(1)
s = r.body if r is not None else ''

#default author + timeage

page_tite = request.args(0)
page = db(db.pagetable.title == page_title).select().first()
 
new_resivion_id = db.revision.insert(body=form.vars.body, page_id=page_id)



#trying to initilize string s to content of body, but revision one may not exisit
 
r = db.revision(1)
s = r.body if r is not None else ''
 

 if r is None:
# First time: we need to insert it.
id = revision.

db.revision.insert(id=1, body=form.vars.body)
#better way to 
id

How do you set r to the id of a title? I believe we edit r = db.revision(1) in default.py but I don't know how
 
i tried following a tip from Q142 and edit so that I have:

page_id = db(db.pagetable.title == title).select().first()
r = db(db.revision.page_id == page_id).select(orderby=~db.revision.date_posted).first()
 
if r is None:
# First time: we need to insert it.
db.revision.insert(id=page_id, body=form.vars.body)
 
all it did for me was show/edit the body of all of the titles. I mean, I could go to like /default/index/cats and edit something, but that same body would show up if i were to do /default/index/dogs. Does anyone know whats going on?