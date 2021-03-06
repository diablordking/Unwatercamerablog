# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)


# -------------------------------------------------------------------------


crud = Crud(globals(),db)


def index():
    posts = db(db.blog_post).select(orderby=~db.blog_post.created_on)
    return locals()

def user():
    from handlers.user import User
    user = User()
    return dict(auth=user.auth, form=user.auth())


@cache.action()

def single():
    response.title ="Cameras"
    return response.render()

def  about():
    posts = db(db.blog_post).select()
    response.title ="About"
    return locals()

def UnderwaterLenses():
    posts = db(db.blog_post).select()
    response.title ="Underwater Lenses"
    return locals()


def MacroTutorials():
    posts = db(db.blog_post).select()
    response.title ="Macro Tutorials"
    return locals()

def WideAngleTutorials():
    posts = db(db.blog_post).select()
    response.title ="Wide Angle Tutorials"
    return locals()

def UnderwaterCameras():
    posts = db(db.blog_post).select()
    response.title ="Underwater Cameras"
    return locals()



def contact(): 
    response.title ="Contact"
    return response.render()


def report(): 
    response.title ="report"
    return response.render()


def download():
    flnm = request.args(0)
    import os
    response.stream(os.path.join(request.folder, 'uploads', flnm))

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def edit():
    "edit an existing wiki page"
    post =db.blog_post(request.args(0,cast=int)) or redirect(URL('default','index'))
    form = crud.update("blog_post", post.id, next=URL("view", args=post.id), 
                      message="post updated")
    return dict(post=post, form=form)

def show():
    post =db.blog_post(request.args(0,cast=int))
    db.blog_comment.blog_post.default = post.id
    db.blog_comment.blog_post.readable=False
    db.blog_comment.blog_post.writable=False
    form = SQLFORM(db.blog_comment).process()
    comments = db(db.blog_comment.blog_post ==post.id).select()
    return locals()


def list_all():
    posts = db.Post.select(orderby=~db.Post.created_on)
    return locals()


@auth.requires_login()
def create():
    form = SQLFORM(db.blog_post).process()
    if form.accepted:
        session.flash = "Posted!"
        redirect(URL('index'))
    return locals()


@auth.requires_membership('patron')
def manage():
    grid =SQLFORM.grid(db.blog_post)
    return locals()

@auth.requires_login()
def postedit():
    myrecord =db(db.blog_post.created_by==auth.user.id)
    grid =SQLFORM.grid(myrecord)
    return locals()
