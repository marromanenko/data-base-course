class View:

    def __init__(self, table, records):
        self.table = table
        self.records = records

    @staticmethod
    def list():
        print('''
        1 => User
        2 => Post
        3 => Comments
        4 => User_Comments
        5 => User_Post
        ''')

    @staticmethod
    def list_for_update():
        print('''
            1 => User
            2 => Post
            3 => Comments
            ''')

    @staticmethod
    def attribute_list_for_search(table):
        if table == 1:
            print('''
            please write on which column you want to search (name, birth date or userID)
            ''')
        elif table == 2:
            print('''
            please write on which column you want to search (postID, userID, namepost or topic)
            ''')
        elif table == 3:
            print('''
            please write on which column you want to search (commentID, postID, date or text)
            ''')
        elif table == 4:
            print('''
            please write on which column you want to search (User_userID, Comments_commentID or ID)
            ''')
        elif table == 5:
            print('''
            please write on which column you want to search (User_userID, Post_postID or ID)
            ''')

    @staticmethod
    def attribute_list(table):
        if table == 1:
            print('''
                1 => name
                2 => birth date
                3 => userID
                ''')
        elif table == 2:
            print('''
                1 => postID
                2 => userID
                3 => namepost
                4 => topic
                ''')
        elif table == 3:
            print('''
                1 => commentID
                2 => postID
                3 => date
                4 => text
                ''')
        elif table == 4:
            print('''
                1 => User_userID
                2 => Comments_commentID
                3 => ID
                ''')
        elif table == 5:
            print('''
                1 => User_userID
                2 => Post_postID
                3 => ID
                ''')

    @staticmethod
    def attribute_list_for_update(table):
        if table == 1:
            print('''
                    1 => name
                    2 => birth date
                    ''')
        elif table == 2:
            print('''
                    1 => namepost
                    2 => topic
                    ''')
        elif table == 3:
            print('''
                    1 => date
                    2 => text
                    ''')


    def show(self):
        print("____________________")
        if self.table == 1:
            for row in self.records:
                print("ID = ", row[0])
                print("Name = ", row[1])
                print("Birth date = ", row[2])
                print("____________________")
        elif self.table == 2:
            for row in self.records:
                print("Post ID = ", row[0])
                print("User ID = ", row[1])
                print("Name of the post = ", row[2])
                print("Topic = ", row[3])
                print("____________________")
        elif self.table == 3:
            for row in self.records:
                print("Comment ID = ", row[0])
                print("Post ID = ", row[1])
                print("Date = ", row[2])
                print("Text = ", row[3])
                print("____________________")
        elif self.table == 4:
            for row in self.records:
                print("User = ", row[0])
                print("Comment = ", row[1])
                print("ID = ", row[2])
                print("____________________")
        elif self.table == 5:
            for row in self.records:
                print("User = ", row[0])
                print("Post = ", row[1])
                print("ID = ", row[2])
                print("____________________")

# Method that prints the result of select query
    def showSelect(self):
        if self.table == 1:
            for row in self.records:
                print("User = ", row[0])
                print("Name of the post = ", row[1])
                print("Topic = ", row[2])
                print("____________________")
        elif self.table == 2:
            for row in self.records:
                print("Topic = ", row[0])
                print("Date = ", row[1])
                print("Text = ", row[2])
                print("____________________")
        elif self.table == 3:
            for row in self.records:
                print("User = ", row[0])
                print("Date = ", row[1])
                print("Text = ", row[2])
                print("____________________")
        else:
            print('\nIncorrect input, try again.')
