from model import Model
import psycopg2


class Menu:
    # Main Method that calls main menu of the controller
    @staticmethod
    def mainmenu():
        exit = False
        print("Welcome!")
        while not exit:
            print('''
            Main menu
            0 => Show one table
            1 => Show all table
            2 => Insert data
            3 => Delete data
            4 => Update data
            5 => Select data
            6 => Randomize data
            7 => Exit''')
            choice = input('Make your choice => ')
            if choice == '0':
                Model.showOneTable()
            elif choice == '1':
                Model.showAllTables()
            elif choice == '2':
                end_insert = False
                while not end_insert:
                    try:
                        Model.insert()
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                        Model.insert()
                    incorrect = True
                    while incorrect:
                        num = input('Continue insertion? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_insert = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                            pass
                        else:
                            print('Incorrect input, try again.')
            elif choice == '3':
                end_delete = False
                while not end_delete:
                    try:
                        Model.delete()
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                        Model.delete()
                    incorrect = True
                    while incorrect:
                        num = input('Continue deletion? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_delete = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                            pass
                        else:
                            print('Incorrect input, try again.')
            elif choice == '4':
                end_update = False
                while not end_update:
                    try:
                        Model.update()
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                        Model.update()
                    incorrect = True
                    while incorrect:
                        num = input('Continue updation? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_update = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                            pass
                        else:
                            print('Incorrect input, try again.')
            elif choice == '5':
                end_select = False
                while not end_select:
                    try:
                        Model.select()
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                        Model.select()
                    incorrect = True
                    while incorrect:
                        num = input('Continue selection? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_select = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                            pass
                        else:
                            print('Incorrect input, try again.')
            elif choice == '6':
                end_random = False
                while not end_random:
                    try:
                        Model.random()
                    except (Exception, psycopg2.Error) as error:
                        print("PostgreSQL Error: ", error)
                        Model.random()
                    incorrect = True
                    while incorrect:
                        num = input('Continue randomization? 1 - Yes; 2 - No =>')
                        if num == '2':
                            end_random = True
                            incorrect = False
                        elif num == '1':
                            incorrect = False
                        else:
                            print('Incorrect input, try again.')
            elif choice == '7':
                exit = True
            else:
                print('Incorrect input, try again.')
            incorrect = True
            while incorrect:
                end = input('Continue work with DB? 1 - Yes; 2 - No. = >')
                if end == '2':
                    incorrect = False
                    exit = True
                elif end == '1':
                    incorrect = False
                else:
                    print('Incorrect input, try again.')
