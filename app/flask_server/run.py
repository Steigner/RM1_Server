# ===================================================================
# | Author: Martin Juricek    | Github: https://github.com/Steigner |
# | SuperVisor: Roman Parak   | Github: https://github.com/rparak   |
# ===================================================================
# | Licence: MIT                                                    |
# ===================================================================
# To-Do List:
#   Delete acces to database in db2 IBM.!!

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
