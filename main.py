import controller
from menu import Menu


connection = controller.makeConnect()
cursor = connection.cursor()
Menu.mainmenu()
cursor.close()
connection.close()
print("PostgreSQL connection is closed")
