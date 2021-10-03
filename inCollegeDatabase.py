import sqlite3 as sql
from sys import argv

#creates a database called database.sqlite and inputs the user table
lnCollege = "database.sqlite" if len(argv) == 1 else argv[1]
source = sql.connect(lnCollege, timeout=10)

cursor = source.cursor()

createTable = """

CREATE TABLE users
(
    username TEXT PRIMARY KEY,
    password TEXT,
    firstName TEXT,
    lastName TEXT,
    email TEXT,
    sms TEXT,
    ad TEXT,
    language TEXT
);

"""


createJobTable = """

CREATE TABLE jobs
(
    title TEXT,
    description TEXT,
    employer TEXT,
    location TEXT,
    salary INTEGER,
    first TEXT,
    last TEXT
);

"""

# =============================================================================
# createOptionTable = """
# 
# CREATE TABLE options
# {
#      
#      email TEXT,
#      sms TEXT,
#      ad TEXT,
#      language TEXT
# };
# 
# """
# =============================================================================

cursor.execute(createTable)
cursor.execute(createJobTable)
#cursor.execute(createOptionTable)
source.commit()

#INPUT ANY OTHER NECESSARY TABLE

source.close()