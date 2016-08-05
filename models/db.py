db = DAL("sqlite://storage.sqlite")

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)


db.define_table('image',
		Field('Title', requires = IS_NOT_EMPTY()),
        Field('Short_Description','text'),
        Field('Ingredients','text',requires = IS_NOT_EMPTY()),
		Field('Procedure','text',requires = IS_NOT_EMPTY()),
		Field('File', 'upload'),
  		Field('Created_by', db.auth_user, default=auth.user_id, writable=False, readable=False),
        Field('likes', 'integer', default='0', readable=False, writable=False))

db.define_table('post',
		Field('Image_id', 'reference image'),
		Field('Author', readable=False, writable=False),
		Field('EMail', readable=False, writable=False),
		Field('Comment'))

db.post.Image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.post.Author.requires = IS_NOT_EMPTY()
db.post.EMail.requires = IS_EMAIL()
db.post.Comment.requires = IS_NOT_EMPTY()

db.post.Image_id.writable = db.post.Image_id.readable = False
custom_auth_table = db[auth.settings.table_user_name]
custom_auth_table.password.requires = [IS_STRONG(), CRYPT()]
