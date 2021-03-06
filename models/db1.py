# -*- coding: utf-8 -*-
from gluon.tools import Crud
crud = Crud(db)


db.define_table('category',Field('name'),Field("description", "text"))


db.define_table('blog_post',
           Field('category','reference category'), 
           Field("body_text", "text",requires=IS_NOT_EMPTY()),
           Field('image', 'upload'),
           Field("title", requires=IS_NOT_EMPTY()),
           Field("description", "text"),
           auth.signature)



db.define_table('blog_comment',
                Field('blog_post', "text",'reference blog_post'),
                Field('body',"text", requires = IS_NOT_EMPTY()),
                auth.signature)
