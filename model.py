import controller
import time
from view import View

tables = {
    1: 'User',
    2: 'Post',
    3: 'Comments',
    4: 'User_Comments',
    5: 'User_Post',
}


class Model:
    @staticmethod
    def validTable():
        incorrect = True
        while incorrect:
            table = input('Choose table number => ')
            if table.isdigit():
                table = int(table)
                if table >= 1 and table <= 5:
                    incorrect = False
                else:
                    print('Incorrect input, try again.')
            else:
                print('Incorrect input, try again.')
        return table

    @staticmethod
    def showAllTables():
        connection = controller.makeConnect()
        cursor = connection.cursor()
        for table in range(1, 6):
            table_name = '''"''' + tables[table] + '''"'''
            print(tables[table])
            show = 'select * from public.{}'.format(table_name)
            print("SQL query => ", show)
            print('')
            cursor.execute(show)
            records = cursor.fetchall()
            obj = View(table, records)
            obj.show()
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def showOneTable():
        View.list()
        connection = controller.makeConnect()
        cursor = connection.cursor()
        table = Model.validTable()
        table_name = '''"''' + tables[table] + '''"'''
        print(tables[table])
        show = 'select * from public.{}'.format(table_name)
        print("SQL query => ", show)
        print('')
        cursor.execute(show)
        records = cursor.fetchall()
        obj = View(table, records)
        obj.show()
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def insert():
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            View.list()
            table = Model.validTable()
            if table == 1:
                usname = "'" + input("Name = ") + "'"
                usbirth_date = "'" + input("Birth date = ") + "'"
                usid = "'" + input('User ID = ') + "'"
                notice = "'This User ID already exists'"
                insert = 'DO $$ BEGIN if not exists (select "userID" from "User" where "userID" = {}) then INSERT ' \
                         'INTO "User"("userID", "name", "birth date") VALUES ({},{},{}); ' \
                         'raise notice {}; else raise notice {}; ' \
                         'end if; end $$;'.format(usid, usid, usname, usbirth_date, "'added'", notice)
                restart = False
            elif table == 2:
                poid = "'" + input('ID = ') + "'"
                poname = "'" + input('Name of the post = ') + "'"
                potopic = "'" + input('Topic = ') + "'"
                pouser = "'" + input('User ID = ') + "'"
                notice = "'This Post ID already exists or this User ID does not exist'"
                insert = 'DO $$  BEGIN IF EXISTS (select "userID" from "User" where "userID" = {}) and not exists ' \
                         '(select "postID" from "Post" where "postID" = {}) THEN ' \
                         'INSERT INTO "Post"("postID", "namepost", "topic", "userID") values ({}, {}, {}, {}); RAISE NOTICE {};' \
                         ' ELSE RAISE NOTICE {}; END IF; ' \
                         'END $$;'.format(pouser, poid, poid, poname, potopic, pouser, "'added'", notice)
                restart = False
            elif table == 3:
                coid = "'" + input('Comment ID = ') + "'"
                codate = "'" + input('Date = ') + "'"
                cotext = "'" + input('Text = ') + "'"
                copost = "'" + input('PostID = ') + "'"
                notice = "'This Comment ID already exists or this Post ID does not exist'"
                insert = 'DO $$  BEGIN IF EXISTS (select "postID" from "Post" where "postID" = {}) and not exists ' \
                         '(select "commentID" from "Comments" where "commentID" = {}) THEN ' \
                         'INSERT INTO "Comments"("commentID", "date", "text", "postID") values ({}, {}, {}, {}); RAISE NOTICE {};' \
                         ' ELSE RAISE NOTICE {}; END IF; END $$;'.format(copost, coid, coid, codate, cotext, copost, "'added'", notice)
                restart = False
            elif table == 4:
                ucid = "'" + input('ID = ') + "'"
                uccomment = "'" + input('Comment = ') + "'"
                ucuser = "'" + input('User = ') + "'"
                notice = "'This ID already exists or this User ID/Comment ID does not exist'"
                insert = 'DO $$ BEGIN IF EXISTS (select "userID" from "User" where "userID" = {}) and ' \
                         'EXISTS (select "commentID" from "Comments" where "commentID" = {}) and ' \
                         'not exists (select "ID" from "User_Comments" where "ID" = {}) THEN ' \
                         'INSERT INTO "User_Comments"("ID", "User_userID", "Comments_commentID") VALUES ({},{},{}); ' \
                         'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                         'END $$;'.format(ucuser, uccomment, ucid, ucid, ucuser, uccomment, "'added'", notice)
                restart = False
            elif table == 5:
                upid = "'" + input('ID = ') + "'"
                upuser = "'" + input('User = ') + "'"
                uppost = "'" + input('Post = ') + "'"
                notice = "'This ID already exists or this User ID/Comment ID does not exist'"
                insert = 'DO $$ BEGIN IF EXISTS (select "userID" from "User" where "userID" = {}) and ' \
                         'EXISTS (select "postID" from "Post" where "postID" = {}) and ' \
                         'not exists (select "ID" from "User_Post" where "ID" = {}) THEN ' \
                         'INSERT INTO "User_Post"("ID", "User_userID", "Post_postID") VALUES ({},{},{}); ' \
                         'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                         'END $$;'.format(upuser, uppost, upid, upid, upuser, uppost, "'added'", notice)
                restart = False
            else:
                print('Incorrect input, try again.')
        print(tables[table])
        print('SQl query => ', insert)
        cursor.execute(insert)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def delete():
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            View.list()
            table = Model.validTable()
            if table == 1:
                usid = "'" + input('Attribute to delete User ID = ') + "'"
                delete = 'delete from "User_Post" where "User_userID" = {};' \
                         'delete from "User_Comments" where "User_userID" = {};' \
                         'delete from "Comments" where "postID" in (select "postID" from "Post" where "userID" = {});' \
                         'delete from "Post" where "userID" = {};' \
                         'delete from "User" where "userID" = {};'.format(usid, usid, usid, usid, usid)
                restart = False
            elif table == 2:
                poid = "'" + input('Attribute to delete Post ID = ') + "'"
                delete = 'delete from "User_Comments" where "Comments_commentID" in (select "commentID" from "Comments" where "postID" = {});' \
                         'delete from "User_Post" where "Post_postID" = {};'\
                         'delete from "Comments" where "postID" = {};' \
                         'delete from "Post" where "postID" = {};'.format(poid, poid, poid, poid)
                restart = False
            elif table == 3:
                coid = "'" + input('Attribute to delete Comment ID = ') + "'"
                delete = 'delete from "User_Comments" where "Comments_commentID" = {};' \
                         'delete from "Comments" where "commentID" = {};'.format(coid, coid)
                restart = False
            elif table == 4:
                ucid = "'" + input('Attribute to delete ID = ') + "'"
                delete = 'delete from "User_Comments" where "ID" =  {}'.format(ucid)
                restart = False
            elif table == 5:
                upid = "'" + input('Attribute to delete ID = ') + "'"
                delete = 'delete from "User_Post" where "ID" = {}'.format(upid)
                restart = False
            else:
                print('Incorrect input, try again.')
        print(tables[table])
        print("SQL query => ", delete)
        cursor.execute(delete)
        connection.commit()
        print('Data deleted successfully!')
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def update():
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            View.list_for_update()
            table = Model.validTable()
            if table == 1:
                usid = "'" + input('Attribute to update(where) User ID = ') + "'"
                View.attribute_list_for_update(1)
                in_restart = True
                while in_restart:
                    num = input('Number of attribute =>')
                    if num == '1':
                        value = "'" + input('New value of attribute = ') + "'"
                        set = '"name" = {}'.format(value)
                        in_restart = False
                    elif num == '2':
                        value = "'" + input('New value of attribute = ') + "'"
                        set = '"birth date" = {}'.format(value)
                        in_restart = False
                    else:
                        print('Incorrect input, try again.')
                notice = "'There is nothing to update'"
                update = 'DO $$ BEGIN IF EXISTS (select "userID" from "User" where "userID" = {}) THEN ' \
                         'update "User" set {} where "userID" = {}; ' \
                         'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                         'END $$;'.format(usid, set, usid, value, notice)
                restart = False
                pass
            elif table == 2:
                poid = "'" + input('Attribute to update(where) Post ID = ') + "'"
                View.attribute_list_for_update(2)
                in_restart = True
                while in_restart:
                    num = input('Number of attribute =>')
                    if num == '1':
                        value = "'" + input('New value of attribute = ') + "'"
                        set = '"namepost"= {}'.format(value)
                        in_restart = False
                    elif num == '2':
                        value = "'" + input('New value of attribute = ') + "'"
                        set = '"topic"= {}'.format(value)
                        in_restart = False
                    else:
                        print('Incorrect input, try again.')
                notice = "'There is nothing to update'"
                update = 'DO $$ BEGIN IF EXISTS (select "postID" from "Post" where "postID" = {}) THEN ' \
                         'update "Post" set {} where "postID" = {}; ' \
                         'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                         'END $$;'.format(poid, set, poid, value, notice)
                restart = False
                pass
            elif table == 3:
                coid = "'" + input('Attribute to update(where) Comment ID = ') + "'"
                View.attribute_list_for_update(3)
                in_restart = True
                while in_restart:
                    num = input('Number of attribute =>')
                    if num == '1':
                        value = "'" + input('New value of attribute = ') + "'"
                        set = '"date"= {}'.format(value)
                        in_restart = False
                    elif num == '2':
                        value = "'" + input('New value of attribute = ') + "'"
                        set = '"text"= {}'.format(value)
                        in_restart = False
                    else:
                        print('Incorrect input, try again.')
                notice = "'There is nothing to update'"
                update = 'DO $$ BEGIN IF EXISTS (select "commentID" from "Comments" where "commentID" = {}) THEN ' \
                         'update "Comments" set {} where "commentID" = {}; ' \
                         'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                         'END $$;'.format(coid, set, coid, value, notice)
                restart = False
                pass
            else:
                print('Incorrect input, try again.')
        print(tables[table])
        print("SQL query => ", update)
        cursor.execute(update)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)
        pass

    @staticmethod
    def select():
        connection = controller.makeConnect()
        cursor = connection.cursor()
        print('1 => Show name and topic of post which created by *user name*')
        print('2 => Show date and text of comment which is under the *post topic*')
        print('3 => Show date and text of comment which created by *user name*')
        choice = input('Your choice is ')
        choice = int(choice)
        if choice == 1:
            user = input('Enter required user name = ')
            select = """select "name", "namepost", "topic" from (select c."name", p."namepost", p."topic"
                 from "Post" p left join "User" c on c."userID" = p."userID"
                     where c."name" LIKE '{}' group by c."name", p."namepost", p."topic") as foo""".format(user)
        elif choice == 2:
            post = input('Enter required post topic = ')
            select = """select "topic", "date", "text" from (select c."topic", p."date", p."text"
                 from "Comments" p left join "Post" c on c."postID" = p."postID"
                     where c."topic" LIKE '{}' group by c."topic", p."date", p."text") as foo""".format(post)
        elif choice == 3:
            user = input('Enter required user name = ')
            select = """select "name", "date", "text" from (select c."name", p."date", p."text"
                 from "Comments" p left join "User" c on c."userID" = p."postID"
                     where c."name" LIKE '{}' group by c."name", p."date", p."text") as foo""".format(user)
        else:
            print('Try again')
        print("SQL query => ", select)
        beg = int(time.time() * 1000)
        cursor.execute(select)
        end = int(time.time() * 1000) - beg
        records = cursor.fetchall()
        obj = View(choice, records)
        obj.showSelect()
        print('Time of request = {} ms'.format(end))
        print('Data selected successfully!')
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def random():
        connection = controller.makeConnect()
        cursor = connection.cursor()
        incorrect = True
        while incorrect:
            num = input('How much datas do you want to add => ')
            num = int(num)
            View.list()
            table = Model.validTable()
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
            elif table == 4:
                insert = "INSERT INTO User_Comments select " \
                         "from generate_series(1,{})".format(num)
                incorrect = False
            elif table == 5:
                insert = "INSERT INTO User_Post select " \
                         "from generate_series(1,{})".format(num)
                incorrect = False
            else:
                print('Incorrect input, try again.')
        print(tables[table])
        print("SQL query => ", insert)
        cursor.execute(insert)
        connection.commit()
        print('Inserted randomly')
        cursor.close()
        controller.closeConnect(connection)
