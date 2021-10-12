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