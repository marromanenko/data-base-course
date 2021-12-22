from view import Menu
from db import Base, engine
from sqlalchemy import MetaData
metadata = MetaData()
Base.metadata.create_all(engine)
Menu.mainmenu()
print("PostgreSQL connection is closed")
