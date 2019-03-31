# -*- coding: utf-8 -*-
#__Author__= allisnone #2019-02-16
#https://docs.python.org/3/library/sqlite3.html
#https://www.sqlite.org/index.html
#https://www.jianshu.com/p/25fde93c2fb9

#https://www.jianshu.com/p/0d234e14b5d3
#https://www.jianshu.com/p/8d085e2f2657
#https://www.jianshu.com/p/9771b0a3e589
from sqlalchemy import *#Column, String, create_engine,relationship
from sqlalchemy.orm import sessionmaker,relationship,aliased
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    addresses = relationship("Address", back_populates='user',cascade="all, delete, delete-orphan")
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                            self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

#User.addresses = relationship("Address", order_by=Address.id, back_populates="user")
"""
class User(Base):
    __tablename__ = 'user'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # 一对多:
    books = relationship('Book')

class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # “多”的一方的book表是通过外键关联到user表的:
    user_id = Column(String(20), ForeignKey('user.id'))
"""

sqlite_file = 'test2.db'    
engine = create_engine('sqlite:///' + sqlite_file + '?check_same_thread=False', echo=False)
#engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')

#根据基类创建数据库表
Base.metadata.create_all(engine)

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print(ed_user)
print(ed_user.name)
print(ed_user.password)
print(ed_user.id)

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# DBSession对象可视为当前数据库连接
# 创建session对象:
session = DBSession()

#new_user = User(id='5', name='Bob')
# 添加到session:
session.add(ed_user)


our_user = session.query(User).filter_by(name='ed').first()

print('our_user=',our_user)
print('ed_user is our_user: ',ed_user is our_user )

session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])

ed_user.password = 'f8s7ccs'
session.dirty
session.new 
# 提交即保存到数据库:
session.commit()

user = session.query(User).filter(User.id=='2').one()
print('type:', type(user))
print('name:', user.name)
# 关闭session:

#数据库查询
#基于类-table查询
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)
#基于列查询
for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)
    
#
for row in session.query(User, User.name).all():
    print(row.User, row.name)
    
for row in session.query(User.name.label('name_label')).all():
    print(row.name_label)

user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.name).all():
    print(row.user_alias)
    
for u in session.query(User).order_by(User.id)[1:3]:
    print(u)
    
for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
    print(name)
    
for name, in session.query(User.name).filter(User.fullname=='Ed Jones'):
    print(name)
    
for user in session.query(User).filter(User.name=='ed').filter(User.fullname=='Ed Jones'):
    print(user)
    
#query.filter(User.name != 'ed')
#query.filter(User.name.like('%ed%'))
#query.filter(User.name.in_(['ed', 'wendy', 'jack']))
# works with query objects too:
#query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%'))))
#not in
#query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
#is None
#query.filter(User.name == None)
#query.filter(User.name.is_(None))

"""
#add:
# use and_()
from sqlalchemy import and_
query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))

# or send multiple expressions to .filter()
query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

# or chain multiple filter()/filter_by() calls
query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')

or:
from sqlalchemy import or_
query.filter(or_(User.name == 'ed', User.name == 'wendy'))

match:
query.filter(User.name.match('wendy'))
"""

#
query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
print(query.all())
print(query.first())
#print(query.one())

user = session.query(User).filter(User.id == 2).one()
print(user)

count = session.query(User).filter(User.name.like('%ed')).count()
print('count=',count)

from sqlalchemy import func

count_func = session.query(func.count(User.name), User.name).group_by(User.name).all()
print('count_func=',count_func)

scalar_count = session.query(func.count('*')).select_from(User).scalar()
print('scalar_count=',scalar_count)

scalar_count = session.query(func.count('*')).scalar()
print('scalar_count_main=',scalar_count)


"""relationship"""
#必须双向关联，区别于Django
User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

#使用关联对象
jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
print(jack.addresses)

jack.addresses = [ Address(email_address='jack@google.com'),Address(email_address='j25@yahoo.com')]
print('jack.addresses[1]=',jack.addresses[1])
print('jack.addresses[1].user=',jack.addresses[1].user)

session.add(jack)
session.commit()

jack = session.query(User).filter_by(name='jack')
print('jack_filter=',jack)
print('jack_filter=',type(jack))
jack = jack.all()

print('jack=',jack)
print('jack.addresses=',jack[0].addresses)

#join 查询

for u, a in session.query(User, Address).\
                    filter(User.id==Address.user_id).\
                    filter(Address.email_address=='jack@google.com').\
                    all():
    print(u)
    print(a)
    
j = session.query(User).join(Address).filter(Address.email_address=='jack@google.com').all()
print('join=',j)

#query.join(Address, User.id==Address.user_id)    # explicit condition
#query.join(User.addresses)                       # specify relationship from left to right
#query.join(Address, User.addresses)              # same, with explicit target
#query.join('addresses')  

adalias1 = aliased(Address)
adalias2 = aliased(Address)
for username, email1, email2 in \
    session.query(User.name, adalias1.email_address, adalias2.email_address).\
    join(adalias1, User.addresses).\
    join(adalias2, User.addresses).\
    filter(adalias1.email_address=='jack@google.com').\
    filter(adalias2.email_address=='j25@yahoo.com'):
    print(username, email1, email2)

#子查询
stmt = session.query(Address.user_id, func.count('*').\
label('address_count')).\
group_by(Address.user_id).subquery()

for u, count in session.query(User, stmt.c.address_count).\
    outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
    print(u, count)
    
stmt = session.query(Address).\
filter(Address.email_address != 'j25@yahoo.com').\
subquery()
adalias = aliased(Address, stmt)
for user, address in session.query(User, adalias).\
    join(adalias, User.addresses):
    print(user)
    print(address)

session.commit()
session.close()


"""many to many"""


from sqlalchemy import Table, Text

post_keywords = Table('post_keywords', Base.metadata,
                      Column('post_id', ForeignKey('posts.id'), primary_key=True),
                      Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
                      )
class BlogPost(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    
    # many to many BlogPost<->Keyword
    keywords = relationship('Keyword',
                            secondary=post_keywords,
                            back_populates='posts')
    
    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body
    
    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


class Keyword(Base):
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost',
                         secondary=post_keywords,
                         back_populates='keywords')
    
    def __init__(self, keyword):
        self.keyword = keyword


Base.metadata.create_all(engine)