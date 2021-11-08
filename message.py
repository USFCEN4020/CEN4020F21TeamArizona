<<<<<<< Updated upstream
# Messaging components of the inCollege program
# Students should be able to send and recieve messages from people (friends)
#  If students are not friends system will respond with a message "Im sorry, you are not friends with that person" -done
#  Student will be notified that they have messages waiting for them next time they log in - done
#  Will be able to select message and read it; once they read they can leave it in inbox or delete it -done
#  message will be able to be responded to and sent back to the inbox -done
# Should generate friends list

import inCollege
import connection

def Messages(cursor,source, username):
    print("Read unread | Read Conversation | Send New Message | Read Inbox")
    choice = input()

    if choice.lower() == "read unread":
        ReadUnread(cursor,source,username)
    elif choice.lower() == "read conversation":
        print("Which conversation to read?")
        person = input()
        ReadConversation(cursor,source,username,person)
    elif choice.lower() == "send new message":
        connection.ShowConnections(cursor,source,username)
    elif choice.lower() == "read inbox":
        print("Recieved from who?")
        person = input()
        ReadInbox(cursor,source,username,person)

#check to see if user has any unread messages
# if they do return true else will return false
# Displays options before 
def CheckUnread(cursor, source, username):
    cursor.execute(f"SELECT * FROM messages where receiver = '{username}' AND status = 'unread' ")
    messages = cursor.fetchall()
    messages = list(messages)
    if not messages:
        return False
    else: 
        return True

def CheckFriend(cursor, source, username, receiver):
    cursor.execute(f"SELECT * FROM friends WHERE (friendOne = '{username}' AND friendTwo = '{receiver}') OR (friendOne = '{receiver}' AND friendTwo = '{username}') ")
    status = cursor.fetchall()
    if len(status) == 0:
        return False
    #for some reason makes list of lists
    status = list(status)
    #print(status[0][2])
    if status[0][2] == 'active':
        return True
    else:
        return False

# Send message for starting initial conversaion with new subject & conversation number
# otherwise use reply function
def SendMessage(cursor, source, username, receiver):
    # Check if user has plus membership
    cursor.execute("SELECT * FROM users")
    names = cursor.fetchall()
    names = list(names)
    for name in names:
        if(name[0] == username):
            if(name[8] == "plus"):
                # Get a list of all students in the system
                cursor.execute("SELECT * FROM users")
                items = cursor.fetchall()
                items = list(items)
                print("List of Students: ")
                print("First Name       Last Name")
                print("----------       ---------")
                for item in items:
                    print(item[2] + "   " + "   " + item[3])
                
                print("Who would you like to send a message to? ")
                firstName = input("Enter the student's first name: ")
                lastName = input("Enter the student's last name: ")

                for item in items:
                    if(firstName == item[2] and lastName == item[3]):
                        receiver = item[0]
                
                print("What would you like to send")
                message = input()
                subject = input("Subject:")
                cursor.execute(f"INSERT INTO messages (message, receiver, sender, status, is_friend, subject) VALUES (?, ?, ?, ?, ?, ?);",
                    (message, receiver, username, 'unread', 'active', subject))
                source.commit()
                print("Message sent!")
            elif(name[8] == "standard"):
                #print(username, '->', receiver)
                isFriend = CheckFriend(cursor, source, username, receiver)

                if isFriend == True:
                    print("What would you like to send")
                    message = input()
                    subject = input("Subject:")
                    cursor.execute(f"INSERT INTO messages (message, receiver, sender, status, is_friend, subject) VALUES (?, ?, ?, ?, ?, ?);",
                        (message, receiver, username, 'unread', 'active', subject))
                    source.commit()
                    print("Message sent!")
                else:
                    print("Im sorry, you are not friends with that person")

    
    #cursor.execute(f"SELECT message from messages WHERE mess_no = 0 AND subject = 'Hi' AND receiver = '{username}'")
    #m = cursor.fetchall()
    #print(m)

#Read unread messages and change their status to read
#you can also reply to any unread messages
def ReadUnread(cursor,source,username):
    print("Here are your unread messages")
    cursor.execute(f"SELECT * FROM messages where receiver = '{username}' AND status = 'unread' ")
    messages = cursor.fetchall()
    messages = list(messages)
    for message in messages:
        print(message[3],':',message[1])
        cursor.execute(f"UPDATE messages SET status ='read' WHERE mess_no = '{message[0]}' AND subject = '{message[6]}' ")
        reply = input("Reply:0 | Delete:1 ")
        if reply == "0":
            Reply(cursor,source,username,message)
        elif reply == "1":
            cursor.execute(f"UPDATE messages SET status ='deleted' WHERE mess_no = '{message[0]}' AND subject = '{message[6]}' ")
        else:
            continue
        source.commit()

    inCollege.Options(cursor,source,username)

def ReadInbox(cursor,source,username,person):
    print(f"All messages from {person}")
    cursor.execute(f"SELECT * FROM messages WHERE receiver = '{username}' AND sender = '{person}' AND status != 'deleted' ")
    convo = cursor.fetchall()
    convo = list(convo)
    for message in convo:
        print(message)
    print("-End-")
    inCollege.Options(cursor,source,username)

def ReadConversation(cursor,source,username,person):
    print(f"Conversation with:{person}")
    cursor.execute(f"Select * FROM messages WHERE (receiver = '{username}' AND sender = '{person}') OR (receiver = '{person}' AND sender = '{username}')")
    convo = cursor.fetchall()
    convo = list(convo)
    for message in convo:
        print(message[1])
        
    print("-End-")
    inCollege.Options(cursor,source,username)

#takes info from info(message) tuple list to send message and increment message id for this subject
def Reply(cursor,source,username,info):
    print("Reply")
    print("What would you like to send")
    message = input()
    cursor.execute(f"INSERT INTO messages (message, receiver, sender, status, is_friend, subject) VALUES (?, ?, ?, ?, ?, ?);",
        (message, info[3], username, 'unread', 'active', info[6]))
    print("Reply sent!")
    source.commit()

    # Handle the experience case
def profileMessage(cursor,username):
    cursor.execute(f"SELECT count(belongsTo) FROM profiles WHERE belongsTo='{username}' ")  
    result = cursor.fetchone()
    if result[0] == 0: {
        print("Dont forget to create a profile")
    }

def waitingMessages(cursor,username):
    cursor.execute(f"SELECT * FROM messages WHERE receiver = '{username}' ")  
    result = cursor.fetchone()
    if result[0] >= 1 and result[0] != username: {
        print("You have messages waiting for you")
=======
# Messaging components of the inCollege program
# Students should be able to send and recieve messages from people (friends)
#  If students are not friends system will respond with a message "Im sorry, you are not friends with that person" -done
#  Student will be notified that they have messages waiting for them next time they log in - done
#  Will be able to select message and read it; once they read they can leave it in inbox or delete it -done
#  message will be able to be responded to and sent back to the inbox -done
# Should generate friends list

import inCollege
import connection

def Messages(cursor,source, username):
    print("Read unread | Read Conversation | Send New Message | Read Inbox")
    choice = input()

    if choice.lower() == "read unread":
        ReadUnread(cursor,source,username)
    elif choice.lower() == "read conversation":
        print("Which conversation to read?")
        person = input()
        ReadConversation(cursor,source,username,person)
    elif choice.lower() == "send new message":
        connection.ShowConnections(cursor,source,username)
    elif choice.lower() == "read inbox":
        print("Recieved from who?")
        person = input()
        ReadInbox(cursor,source,username,person)

#check to see if user has any unread messages
# if they do return true else will return false
# Displays options before 
def CheckUnread(cursor, source, username):
    cursor.execute(f"SELECT * FROM messages where receiver = '{username}' AND status = 'unread' ")
    messages = cursor.fetchall()
    messages = list(messages)
    if not messages:
        return False
    else: 
        return True

def CheckFriend(cursor, source, username, receiver):
    cursor.execute(f"SELECT * FROM friends WHERE (friendOne = '{username}' AND friendTwo = '{receiver}') OR (friendOne = '{receiver}' AND friendTwo = '{username}') ")
    status = cursor.fetchall()
    if len(status) == 0:
        return False
    #for some reason makes list of lists
    status = list(status)
    #print(status[0][2])
    if status[0][2] == 'active':
        return True
    else:
        return False

# Send message for starting initial conversaion with new subject & conversation number
# otherwise use reply function
def SendMessage(cursor, source, username, receiver):
    # Check if user has plus membership
    cursor.execute("SELECT * FROM users")
    names = cursor.fetchall()
    names = list(names)
    for name in names:
        if(name[0] == username):
            if(name[8] == "plus"):
                # Get a list of all students in the system
                cursor.execute("SELECT * FROM users")
                items = cursor.fetchall()
                items = list(items)
                print("List of Students: ")
                print("First Name       Last Name")
                print("----------       ---------")
                for item in items:
                    print(item[2] + "   " + "   " + item[3])
                
                print("Who would you like to send a message to? ")
                firstName = input("Enter the student's first name: ")
                lastName = input("Enter the student's last name: ")

                for item in items:
                    if(firstName == item[2] and lastName == item[3]):
                        receiver = item[0]
                
                print("What would you like to send")
                message = input()
                subject = input("Subject:")
                cursor.execute(f"INSERT INTO messages (message, receiver, sender, status, is_friend, subject) VALUES (?, ?, ?, ?, ?, ?);",
                    (message, receiver, username, 'unread', 'active', subject))
                source.commit()
                print("Message sent!")
            elif(name[8] == "standard"):
                #print(username, '->', receiver)
                isFriend = CheckFriend(cursor, source, username, receiver)

                if isFriend == True:
                    print("What would you like to send")
                    message = input()
                    subject = input("Subject:")
                    cursor.execute(f"INSERT INTO messages (message, receiver, sender, status, is_friend, subject) VALUES (?, ?, ?, ?, ?, ?);",
                        (message, receiver, username, 'unread', 'active', subject))
                    source.commit()
                    print("Message sent!")
                else:
                    print("Im sorry, you are not friends with that person")

    
    #cursor.execute(f"SELECT message from messages WHERE mess_no = 0 AND subject = 'Hi' AND receiver = '{username}'")
    #m = cursor.fetchall()
    #print(m)

#Read unread messages and change their status to read
#you can also reply to any unread messages
def ReadUnread(cursor,source,username):
    print("Here are your unread messages")
    cursor.execute(f"SELECT * FROM messages where receiver = '{username}' AND status = 'unread' ")
    messages = cursor.fetchall()
    messages = list(messages)
    for message in messages:
        print(message[3],':',message[1])
        cursor.execute(f"UPDATE messages SET status ='read' WHERE mess_no = '{message[0]}' AND subject = '{message[6]}' ")
        reply = input("Reply:0 | Delete:1 ")
        if reply == "0":
            Reply(cursor,source,username,message)
        elif reply == "1":
            cursor.execute(f"UPDATE messages SET status ='deleted' WHERE mess_no = '{message[0]}' AND subject = '{message[6]}' ")
        else:
            continue
        source.commit()

    inCollege.Options(cursor,source,username)

def ReadInbox(cursor,source,username,person):
    print(f"All messages from {person}")
    cursor.execute(f"SELECT * FROM messages WHERE receiver = '{username}' AND sender = '{person}' AND status != 'deleted' ")
    convo = cursor.fetchall()
    convo = list(convo)
    for message in convo:
        print(message)
    print("-End-")
    inCollege.Options(cursor,source,username)

def ReadConversation(cursor,source,username,person):
    print(f"Conversation with:{person}")
    cursor.execute(f"Select * FROM messages WHERE (receiver = '{username}' AND sender = '{person}') OR (receiver = '{person}' AND sender = '{username}')")
    convo = cursor.fetchall()
    convo = list(convo)
    for message in convo:
        print(message[1])
        
    print("-End-")
    inCollege.Options(cursor,source,username)

#takes info from info(message) tuple list to send message and increment message id for this subject
def Reply(cursor,source,username,info):
    print("Reply")
    print("What would you like to send")
    message = input()
    cursor.execute(f"INSERT INTO messages (message, receiver, sender, status, is_friend, subject) VALUES (?, ?, ?, ?, ?, ?);",
        (message, info[3], username, 'unread', 'active', info[6]))
    print("Reply sent!")
    source.commit()

    # Handle the experience case
def profileMessage(cursor,username):
    cursor.execute(f"SELECT count(belongsTo) FROM profiles WHERE belongsTo='{username}' ")  
    result = cursor.fetchone()
    if result[0] == 0: {
        print("Dont forget to create a profile")
    }

def waitingMessages(cursor,username):
    cursor.execute(f"SELECT * FROM messages WHERE receiver = '{username}' ")  
    result = cursor.fetchone()
    if result[0] >= 1 and result[0] != username: {
        print("You have messages waiting for you")
>>>>>>> Stashed changes
    }