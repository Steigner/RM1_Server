# configuration class:
#   input: none
# Note: In this class we set up connections to databases of users and patients,
# also SQLAlchemy properties and NO DEBUG property for python flask server.
# db_users: [SQLite] -> database is located in folder app -> file: db_users.db
# db_patients: [IBM DB2] -> database is hosted in a web cloud, which is managed by IBM company
class Config:
    DEBUG = False
    SECRET_KEY = "secret"
    SQLALCHEMY_BINDS = {
        "db_users": "sqlite:///database/db_users.db",
        "db_patients": "sqlite:///database/db_patients.db",
        # switch between db2 and sqlite
        # 'db_patients': 'db2://sxj87782:6hns9qcp60qx39%409@dashdb-txn-sbox-yp-lon02-13.services.eu-gb.bluemix.net:50000/BLUDB'
    }
    # property for commit changes into databases
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # property which is used for logging
    USE_SESSION_FOR_NEXT = True

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
