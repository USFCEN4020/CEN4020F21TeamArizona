# Gabriel Gusmao de Almeida
# Tural Hagverdigev U10263909
# Antonio Gonzalez U57195076

# References:
# How to mock a single call to the bultin input() function with pytest - https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
# How to mock consecutive calls to input() with pytest - https://stackoverflow.com/questions/59986625/how-to-simulate-two-consecutive-console-inputs-with-pytest-monkeypatch
# How to read stdout with pytest - https://docs.pytest.org/en/6.2.x/capture.html

import inCollege
import sqlite3 as sql
import pytest
import os


# Creating a test database to not interfere with data from the primary one
TEST_DB_FILENAME = "test_database.sqlite"
@pytest.fixture
def testDB():
        os.system(f"python inCollegeDatabase.py {TEST_DB_FILENAME}")
        source = sql.connect(TEST_DB_FILENAME)
        cursor = source.cursor()
        return cursor,source

@pytest.fixture
def destroyTestDB():
    return lambda : os.system(f"rm {TEST_DB_FILENAME}")

#Asserting that login fails when username does not exist
def test_FailedLogIn(monkeypatch,capsys,testDB,destroyTestDB):
    inputs = iter(['bart','simpson'])
    desiredOutput = 'user does not exist with this username and password combination\n'
    monkeypatch.setattr('builtins.input', lambda _="":next(inputs))
    cursor, _ = testDB
    try:
        inCollege.logIn(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
    destroyTestDB()
        
#Asserting that sign ups with weak passwords won't be allowed
def test_WeakPasswords(monkeypatch,capsys,testDB,destroyTestDB):
    tests = [iter(['bart', 'simpson']),iter(['bart','Simpson']),iter(['bart','Simpson1']),
            iter(['bart','Simpson@']),iter(['bart','simpson12@'])]
    desiredOutput = "Invalid option. Password must between 8 and 12 characters, have a digit, capital letter, and a special character\n"
    cursor, source = testDB
    for inputs in tests:
        monkeypatch.setattr('builtins.input',lambda _="":next(inputs))
        try:
            inCollege.signUp(cursor,source)
        except(StopIteration):
            output = capsys.readouterr().out
            assert output == desiredOutput
    destroyTestDB()

#Asserting successful sign up when the password is strong enough
def test_ValidSignUp(monkeypatch,capsys,testDB,destroyTestDB):
    inputs = iter(['bart','Simpson12@','Bart','Simpson'])
    desiredOutput = 'Logged in!\n'
    monkeypatch.setattr('builtins.input',lambda _="":next(inputs))
    cursor, source = testDB
    try:
        inCollege.signUp(cursor,source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
    destroyTestDB()

#Asserting that sign ups where the username already exists will fail
def test_UsernameExistsInSignUp(monkeypatch,capsys,testDB,destroyTestDB):
    inputs = iter(['bart'])
    desiredOutput = 'Username already exists\n'
    monkeypatch.setattr('builtins.input',lambda _="":next(inputs))
    cursor, source = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
    ('bart','Simpson@12', 'bart', 'simpson'))
    try:
        inCollege.signUp(cursor,source)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
    destroyTestDB()

#Asserting successful login when account is in database
def test_SuccessfullLogin(monkeypatch,capsys,testDB,destroyTestDB):
    inputs = iter(['bart','Simpson12@'])
    desiredOutput = 'Logged in!\n'
    monkeypatch.setattr('builtins.input',lambda _="":next(inputs))
    cursor, _ = testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
    ('bart','Simpson12@', 'bart', 'simpson'))
    try:
        inCollege.logIn(cursor)
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
    destroyTestDB()

def test_MaxAccounts(monkeypatch,capsys,testDB,destroyTestDB):
    tests = [iter(['bart','Simpson12@','Bart','Simpson']),iter(['marge', 'Simpson12@','Marge','Simpson']),
        iter(['homer','Simpson12@','Homer','Simpson']),iter(['maggie','Simpson12@','Maggie','Simpson']),
        iter(['lisa','Simpson12@','Lisa','Simpson']),iter(['mrburns','Simpson12@','Mr.','Burns'])]
    desiredOutput = "Unable to sign up. There is already the maximum number of users.\n"
    cursor, source = testDB
    for inputs in tests:
        monkeypatch.setattr('builtins.input',lambda _="":next(inputs))
        try:
            inCollege.signUp(cursor,source)
        except(StopIteration):
            output = capsys.readouterr().out
            assert output == desiredOutput
    destroyTestDB()

#Asserting that 5 skills show up after logged in and skills option is selected
def test_SkillsAreDisplaying(monkeypatch,capsys):
    inputs = iter(["learn skill"])
    desiredOutput = "Select Option\n============================================================\n______________________________________________________________\nC++ | Java | Python | SQL | JavaScript | No Selection\n______________________________________________________________\n"
    monkeypatch.setattr('builtins.input',lambda _="":next(inputs))
    try:
        inCollege.Options("")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

#Assert that if a existing user is found when searched
def test_SearchExistingUser(monkeypatch,capsys,testDB,destroyTestDB):
    inputs = iter(["homer","simpson"])
    desiredOutput = "They are a part of the InCollege system\nSearch again: 0\n"
    monkeypatch.setattr('builtins.input',lambda _="":next(inputs))
    cursor, _= testDB
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?);',
    ('homer','Simpson12@', 'homer', 'simpson'))
    try:
        inCollege.FindPerson1(cursor,"")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
    destroyTestDB()

#Assert that if a non existing user is not found when searched
def test_SearchNonExistingUser(monkeypatch,capsys,testDB,destroyTestDB):
    inputs = iter(['Mr.','Burns'])
    desiredOutput = "They are not yet a part of the InCollege system\nSearch again: 0\n"
    cursor, _= testDB
    monkeypatch.setattr('builtins.input',lambda _="":next(inputs))
    try:
        inCollege.FindPerson1(cursor,"")
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput
    destroyTestDB()

def test_video(monkeypatch, capsys):
    inputs = iter(['0',])
    desiredOutput = "Video is now playing\n"
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    try:
        inCollege.PlayVideo()
    except(StopIteration):
        output = capsys.readouterr().out
        assert output == desiredOutput

def test_userSuccessStory(capsys):
    desiredOutput="Thanks to inCollege I was able to meet with fellow college students and establish connections\nthat allowed me to learn new skills, and become a prime job candidate. Soon after signing up for inCollege\nI was learning new coding languages and working on personal project. Now I'm about start my first job at Microsoft\n--Alyssa (Arizona)\n"
    inCollege.successStory()
    output = capsys.readouterr().out
    assert output == desiredOutput