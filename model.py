import controller
import time

tables = {
    1: 'User',
    2: 'Post',
    3: 'Comments',
    4: 'User_Comments',
    5: 'User_Post',
}


class Model:
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
    def insert_for_table1(usname, usbirth_date, usid):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'This User ID already exists'"
            insert = 'DO $$ BEGIN if not exists (select "userID" from "User" where "userID" = {}) then INSERT ' \
                         'INTO "User"("userID", "name", "birth date") VALUES ({},{},{}); ' \
                         'raise notice {}; else raise notice {}; ' \
                         'end if; end $$;'.format(usid, usid, usname, usbirth_date, "'added'", notice)
            restart = False
        print('SQl query => ', insert)
        cursor.execute(insert)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def insert_for_table2(poid, poname, potopic, pouser):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'This Post ID already exists or this User ID does not exist'"
            insert = 'DO $$  BEGIN IF EXISTS (select "userID" from "User" where "userID" = {}) and not exists ' \
                     '(select "postID" from "Post" where "postID" = {}) THEN ' \
                     'INSERT INTO "Post"("postID", "namepost", "topic", "userID") values ({}, {}, {}, {}); RAISE NOTICE {};' \
                     ' ELSE RAISE NOTICE {}; END IF; ' \
                     'END $$;'.format(pouser, poid, poid, poname, potopic, pouser, "'added'", notice)
            restart = False
        print('SQl query => ', insert)
        cursor.execute(insert)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def insert_for_table3(coid, codate, cotext, copost):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'This Comment ID already exists or this Post ID does not exist'"
            insert = 'DO $$  BEGIN IF EXISTS (select "postID" from "Post" where "postID" = {}) and not exists ' \
                     '(select "commentID" from "Comments" where "commentID" = {}) THEN ' \
                     'INSERT INTO "Comments"("commentID", "date", "text", "postID") values ({}, {}, {}, {}); RAISE NOTICE {};' \
                     ' ELSE RAISE NOTICE {}; END IF; END $$;'.format(copost, coid, coid, codate, cotext, copost,
                                                                     "'added'", notice)
            restart = False
        print('SQl query => ', insert)
        cursor.execute(insert)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def delete_for_table1(usid):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            delete = 'delete from "User_Post" where "User_userID" = {};' \
                         'delete from "User_Comments" where "User_userID" = {};' \
                         'delete from "Comments" where "postID" in (select "postID" from "Post" where "userID" = {});' \
                         'delete from "Post" where "userID" = {};' \
                         'delete from "User" where "userID" = {};'.format(usid, usid, usid, usid, usid)
            restart = False
        print("SQL query => ", delete)
        cursor.execute(delete)
        connection.commit()
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def delete_for_table2(poid):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            delete = 'delete from "User_Comments" where "Comments_commentID" in (select "commentID" from "Comments" where "postID" = {});' \
                     'delete from "User_Post" where "Post_postID" = {};' \
                     'delete from "Comments" where "postID" = {};' \
                     'delete from "Post" where "postID" = {};'.format(poid, poid, poid, poid)
            restart = False
        print("SQL query => ", delete)
        cursor.execute(delete)
        connection.commit()
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def delete_for_table3(coid):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            delete = 'delete from "User_Comments" where "Comments_commentID" = {};' \
                     'delete from "Comments" where "commentID" = {};'.format(coid, coid)
            restart = False
        print("SQL query => ", delete)
        cursor.execute(delete)
        connection.commit()
        cursor.close()
        controller.closeConnect(connection)

    @staticmethod
    def update_for_table1(usid, set):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'There is nothing to update'"
            update = 'DO $$ BEGIN IF EXISTS (select "userID" from "User" where "userID" = {}) THEN ' \
                         'update "User" set {} where "userID" = {}; ' \
                         'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                         'END $$;'.format(usid, set, usid, "'updated'", notice)
            restart = False
            pass
        print("SQL query => ", update)
        cursor.execute(update)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)
        pass

    @staticmethod
    def update_for_table2(poid, set):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'There is nothing to update'"
            update = 'DO $$ BEGIN IF EXISTS (select "postID" from "Post" where "postID" = {}) THEN ' \
                     'update "Post" set {} where "postID" = {}; ' \
                     'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                     'END $$;'.format(poid, set, poid, "'updated'", notice)
            restart = False
            pass
        print("SQL query => ", update)
        cursor.execute(update)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)
        pass

    @staticmethod
    def update_for_table3(coid, set):
        connection = controller.makeConnect()
        cursor = connection.cursor()
        restart = True
        while restart:
            notice = "'There is nothing to update'"
            update = 'DO $$ BEGIN IF EXISTS (select "commentID" from "Comments" where "commentID" = {}) THEN ' \
                     'update "Comments" set {} where "commentID" = {}; ' \
                     'RAISE NOTICE {}; ELSE RAISE NOTICE {}; END IF; ' \
                     'END $$;'.format(coid, set, coid, "'updated'", notice)
            restart = False
            pass
        print("SQL query => ", update)
        cursor.execute(update)
        connection.commit()
        print(connection.notices)
        cursor.close()
        controller.closeConnect(connection)
        pass

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
