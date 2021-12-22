import datetime
from sqlalchemy.orm import relationship
import time
from db import Base, Session, engine
import controller
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
import psycopg2

s = Session()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


user_post_association = Table('User_Post', Base.metadata, Column('User_userID', Integer, ForeignKey('User.userID'), primary_key=True),
                              Column('Post_postID', Integer, ForeignKey('Post.postID'), primary_key=True))

user_comments_association = Table('User_Comments', Base.metadata, Column('User_userID', Integer, ForeignKey('User.userID'), primary_key=True),
                              Column('Comments_commentID', Integer, ForeignKey('Comments.commentID'), primary_key=True))


class User(Base):
    __tablename__ = 'User'
    userID = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(Date)

    posts = relationship('Post')
    comments = relationship("Comments", secondary=user_comments_association)
    posts1 = relationship("Post", secondary=user_post_association)

    def __init__(self, userID, name, birth_date):
        self.userID = userID
        self.name = name
        self.birth_date = birth_date

    def __repr__(self):
        return "<User(name='{}', birth_date={})>".format(self.name, self.birth_date)


class Post(Base):
    __tablename__ = 'Post'
    postID = Column(Integer, primary_key=True)
    namepost = Column(String)
    topic = Column(String)
    userID = Column(Integer, ForeignKey('User.userID'))
    comments = relationship("Comments")

    def __init__(self, postID, namepost, topic, userID):
        self.postID = postID
        self.namepost = namepost
        self.topic = topic
        self.userID = userID

    def __repr__(self):
        return "<Post(namepost='{}', topic={})>".format(self.namepost, self.topic)


class Comments(Base):
    __tablename__ = 'Comments'
    commentID = Column(Integer, primary_key=True)
    date = Column(Date)
    text = Column(String)
    postID = Column(Integer, ForeignKey('Post.postID'))

    def __init__(self, commentID, date, text, postID):
        self.commentID = commentID
        self.date = date
        self.text = text
        self.postID = postID

    def __repr__(self):
        return "<Comment(date={}, text='{}')>".format(self.date, self.text)


tables = {
    1: 'User',
    2: 'Post',
    3: 'Comments',
    4: 'User_Comments',
    5: 'User_Post',
}


class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    @staticmethod
    def validTable(table):
        incorrect = True
        while incorrect:
            if str(table).isdigit():
                table = int(table)
                if table >= 1 and table <= 5:
                    incorrect = False
                else:
                    print('Incorrect input, try again.')
            else:
                print('Incorrect input, try again.')
        return table

    @staticmethod
    def showOneTable(table):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        table_name = '''"''' + tables[table] + '''"'''
        print(tables[table])
        show = 'select * from public.{}'.format(table_name)
        print("SQL query => ", show)
        print('')
        cursor.execute(show)
        records = cursor.fetchall()
        cursor.close()
        controller.closeConnect(connection)
        return records

    @staticmethod
    def insert_for_table1(userID: int, name: str, birth_date: datetime.datetime) -> None:
        user = User(userID=userID, name=name, birth_date=birth_date)
        s.add(user)
        s.commit()

    @staticmethod
    def insert_for_table2(postID: int, namepost: str, topic: str, userID: int) -> None:
        post = Post(postID=postID, namepost=namepost, topic=topic, userID=userID)
        s.add(post)
        s.commit()

    @staticmethod
    def insert_for_table3(commentID: int, date: datetime.datetime, text: str, postID: int) -> None:
        comment = Comments(commentID=commentID, date=date, text=text, postID=postID)
        s.add(comment)
        s.commit()

    @staticmethod
    def delete_for_table1(userID) -> None:
        sql_delete = s.query(User).filter_by(userID=userID).one()
        s.delete(sql_delete)
        s.commit()

    @staticmethod
    def delete_for_table2(postID) -> None:
        sql_delete = s.query(Post).filter_by(postID=postID).one()
        s.delete(sql_delete)
        s.commit()

    @staticmethod
    def delete_for_table3(commentID) -> None:
        sql_delete = s.query(Comments).filter_by(commentID=commentID).one()
        s.delete(sql_delete)
        s.commit()

    @staticmethod
    def update_for_table1(userID: int, name: str, birth_date: datetime.datetime) -> None:
        s.query(User).filter_by(userID=userID).update({User.name: name, User.birth_date: birth_date})
        s.commit()

    @staticmethod
    def update_for_table2(postID: int, namepost: str, topic: str) -> None:
        s.query(Post).filter_by(postID=postID).update({Post.namepost: namepost, Post.topic: topic})
        s.commit()

    @staticmethod
    def update_for_table3(commentID: int, date: datetime.datetime, text: str) -> None:
        s.query(Comments).filter_by(commentID=commentID).update({Comments.date: date, Comments.text: text})
        s.commit()

    @staticmethod
    def select1(user):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        select = """select "name", "namepost", "topic" from (select c."name", p."namepost", p."topic"
                         from "Post" p left join "User" c on c."userID" = p."userID"
                             where c."name" LIKE '{}' group by c."name", p."namepost", p."topic") as foo""".format(user)
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        records = cursor.fetchall()
        print('Time of request = {} ms'.format(end))
        cursor.close()
        controller.closeConnect(connection)
        return records

    @staticmethod
    def select2(post):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        select = """select "topic", "date", "text" from (select c."topic", p."date", p."text"
                         from "Comments" p left join "Post" c on c."postID" = p."postID"
                             where c."topic" LIKE '{}' group by c."topic", p."date", p."text") as foo""".format(post)
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        records = cursor.fetchall()
        print('Time of request = {} ms'.format(end))
        cursor.close()
        controller.closeConnect(connection)
        return records

    @staticmethod
    def select3(user):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        select = """select "name", "date", "text" from (select c."name", p."date", p."text"
                         from "Comments" p left join "User" c on c."userID" = p."postID"
                             where c."name" LIKE '{}' group by c."name", p."date", p."text") as foo""".format(user)
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        records = cursor.fetchall()
        print('Time of request = {} ms'.format(end))
        cursor.close()
        controller.closeConnect(connection)
        return records

    @staticmethod
    def random(table, num):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        incorrect = True
        while incorrect:
            if table == 1:
                insert = """INSERT INTO "User"("name", "birth date") select chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int), 
                         timestamp '2014-01-10 20:00:00' + random() * (timestamp '2014-01-20 20:00:00' -
                   timestamp '2014-01-10 10:00:00') from generate_series(1,{})""".format(num)
                incorrect = False
            elif table == 2:
                insert = """INSERT INTO "Post" ("namepost", "topic") select chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int), 
                         chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int)
                         from generate_series(1,{})""".format(num)
                incorrect = False
            elif table == 3:
                insert = """INSERT INTO "Comments"("text", "date") select chr(trunc(65 + random()*26)::int)||chr(trunc(65 + random()*26)::int), 
                         timestamp '2014-01-10 20:00:00' + random() * (timestamp '2014-01-20 20:00:00' -
                   timestamp '2014-01-10 10:00:00') from generate_series(1, {})""".format(num)
                incorrect = False
            else:
                print('Incorrect input, try again.')
        print("SQL query => ", insert)
        cursor.execute(insert)
        connection.commit()
        cursor.close()
        controller.closeConnect(connection)
