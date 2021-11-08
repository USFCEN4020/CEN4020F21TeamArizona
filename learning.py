def Learning(cursor,source,username):
    currentCourses = dict([(i,course) for i,course in
    enumerate([
        "How to use In College learning",
        "Gamification of learning",
        "Train the Trainer",
        "Understanding the Architectural Design Process",
        "Project Management Simplified"
    ])])
    print("-----------------------------------------------------")
    print("You can press B to go back to the main menu")
    print("Here are the current available courses:")
    print("-----------------------------------------------------")
    for i in currentCourses:
        tookIt = hasTakenCourse(cursor,username,currentCourses[i])
        print(currentCourses[i],"| to select this course press",i,"| Done" if tookIt else "","\n")
    decision = input()
    decision = int(decision) if decision != "B" else decision
    while (decision not in currentCourses.keys()) and decision != "B":
        print("Please pick a valid input")
        decision = input()
        decision = int(decision) if decision != "B" else decision
    if decision == "B":
        return
    if not hasTakenCourse(cursor,username,currentCourses[decision]):
        completeCourse(cursor,source,username,currentCourses[decision])
        print("Course completed!")
    else:
        print("You have already taken this course, would you like to take it again? 0 for yes")
        decision = input()
        if decision == "0":
            print("You have now completed this training")
        else:
            print("Course Cancelled")
    Learning(cursor,source,username)
    


# Database functions:

def completeCourse(cursor,source,username,courseName):
    cursor.execute("INSERT INTO coursesTaken(username,course) VALUES(?,?)",(username,courseName))
    source.commit()

def hasTakenCourse(cursor,username,courseName):
    cursor.execute("SELECT * FROM coursesTaken WHERE username = ? AND course = ?",(username,courseName))
    if len(cursor.fetchall()) > 0:
        return True
    return False