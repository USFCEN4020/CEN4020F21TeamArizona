import inCollege
import jobs
import message
import profile

class Connection:
    def __init__(self,connection_tuple,username,cursor,source):
        if connection_tuple[0] == username:
            self.user = connection_tuple[0]
            self.friend = connection_tuple[1]
        else:
            self.user = connection_tuple[1]
            self.friend = connection_tuple[0]
        self.status = connection_tuple[2]
        self.dbCursor = cursor
        self.dbSource = source
    def disconnect(self):
        query = """
            DELETE FROM friends WHERE
            (friendOne = ? AND friendTwo = ?) OR 
            (friendOne = ? AND friendTwo = ?)
        """
        self.dbCursor.execute(query,(self.user,self.friend,self.friend,self.user))
        self.dbSource.commit()
        for attribute in self.__dict__:
            self.__dict__[attribute] = None

def getConnections(cursor,source,username):
    cursor.execute(f"SELECT * FROM friends WHERE friendOne = ? OR friendTwo = ?",(username,username))
    return [Connection(result,username,cursor,source) for result in cursor.fetchall()] 


# View friends. Assumes that we want to display the friend's username
def ShowConnections(cursor, source, username):
    # Check if user has plus membership
    cursor.execute("SELECT * FROM users")
    names = cursor.fetchall()
    names = list(names)
    hadResult = False
    for name in names:
        if (name[0] == username):
            if (name[8] == "plus"):
                print("Would you like to send a message? type 'message' ")
                choice = input()
                choice.lower()
                if choice == "message":
                    message.SendMessage(cursor, source, username, "")
            elif (name[8] == "standard"):
                connections = getConnections(cursor, source, username)
                hadResult = False
                for connection in connections:
                    if connection.status != "pending":
                        hadResult = True
                        print(f"Connection's name: {connection.friend}")
                        connectionProfile = profile.readProfile(cursor, connection.friend)
                        if connectionProfile:
                            print("This connection has a profile, would you like to look at it? 'yes' to view it")
                            choice = input()
                            if choice == 'yes':
                                profile.printProfile(connectionProfile)
                        print("Would you like to disconnect with this person? type 'disconnect' if you would like it.")
                        print("Would you like to send a message? type 'message' ")
                        choice = input()
                        choice.lower()
                        if choice == "disconnect":
                            exFriend = connection.friend
                            connection.disconnect()
                            print(f"You disconnected with {exFriend}")
                        elif choice == "message":
                            message.SendMessage(cursor, source, username, connection.friend)

    if not hadResult:
        print("No connections were found")
    inCollege.Options(cursor, source, username)


# send a friend request
def MakeFriend(cursor, source, username):
    last_name = input("Please enter a last name, 0 for none: ")
    major = input("Please enter a major, 0 for none: ")
    university = input("Please enter a university, 0 for none: ")

    if last_name == '0' and major == '0' and university == '0':
        choice = input(
            "Invalid. Please enter at least one name, major or university. Would you like to search again? 0 for yes ")
        if choice == '0':
            MakeFriend(cursor, source, username)
        else:
            inCollege.Options(cursor, source, username)
    found = False
    if major == '0' and university == '0':
        cursor.execute("SELECT * FROM users")
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if last_name == item[3]:
                cursor.execute(
                    "SELECT * FROM friends WHERE (friendOne == ? AND friendTwo == ?) OR (friendOne == ? AND friendTwo == ?);",
                    (username, item[0], item[0], username))
                values = cursor.fetchall()
                values = list(values)
                if len(values) == 1:
                    continue
                if username != item[0]:
                    decision = input(item[2] + ' ' + item[
                        3] + ' is in the College System? Would you like to add this person? 0 for yes: ')
                    if decision == '0':
                        cursor.execute("INSERT INTO friends (friendOne, friendTwo, status) VALUES (?, ?, 'pending');",
                                       (username, item[0]))
                        source.commit()
                        print("Friend Request Sent")
    else:
        cursor.execute("SELECT * FROM users, profiles WHERE profiles.belongsTo == users.username;")
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            if (last_name == '0' or last_name == item[3]) and (major == '0' or major == item[10]) and (
                    university == '0' or university == item[11]):
                cursor.execute(
                    "SELECT * FROM friends WHERE (friendOne == ? AND friendTwo == ?) OR (friendOne == ? AND friendTwo == ?);",
                    (username, item[0], item[0], username))
                values = cursor.fetchall()
                values = list(values)
                if len(values) == 1:
                    continue
                if username != item[0]:
                    decision = input(item[2] + ' ' + item[
                        3] + ' is in the College System. Would you like to add this person? 0 for yes: ')
                    if decision == '0':
                        cursor.execute("INSERT INTO friends (friendOne, friendTwo, status) VALUES (?, ?, 'pending');",
                                       (username, item[0]))
                        source.commit()
                        print("Friend Request Sent")
    inCollege.Options(cursor, source, username)


# view any incoming friend requests or pending friend requests
def ViewFriendRequest(cursor, source, username):
    choice = input("View Incoming Friend Requests or Pending Requests Sent? 0 for incoming: ")
    if choice == '0':
        cursor.execute("SELECT * FROM friends WHERE friendTwo == ? AND status == 'pending';", (username,))
        items = cursor.fetchall()
        items = list(items)
        for item in items:
            option = input("Would you like to accept " + item[0] + "? 0 for accept: ")
            if option == '0':
                cursor.execute("UPDATE friends SET status='active' WHERE friendOne == ? AND friendTwo == ?;",
                               (item[0], username))
                source.commit()
            else:
                cursor.execute("DELETE FROM friends WHERE friendOne == ? AND friendTwo == ?;", (item[0], username))
                source.commit()
    else:
        cursor.execute("SELECT * FROM friends WHERE friendOne == ? AND status == 'pending'", (username,))
        items = cursor.fetchall()
        items = list(items)
        print("Pending Requests Sent: ")
        for item in items:
            print(item[1])

    decision = input("Would you like to return to the main menu? 0 for yes: ")
    if decision == '0':
        inCollege.Options(cursor, source, username)
    else:
        ViewFriendRequest(cursor, source, username)