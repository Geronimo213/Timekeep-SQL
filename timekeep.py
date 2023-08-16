import mysql.connector
import bcrypt
import getpass
import time
import datetime

clear = "\n" * 100


class user:
    id = 0
    name = ""
    pwd_hash = ""

    def __str__(self):
        return "{0} \n{1} \n{2}".format(self.id, self.name, self.pwd_hash)


class project:
    id = None
    name = ""
    hours = None
    user_id = None

    def __init__(self, id, name, hours, user_id):
        self.id = id
        self.name = name
        self.hours = hours
        self.user_id = user_id
    def __str__(self):
        return "Name: {0} \nHours: {1} \n".format(self.name, self.hours / 60)


def updateHours(project, connection):
    cursor = connection.cursor()
    cursor.execute("update project set hours = '%s' where project_id = %s", (int(project.hours), project.id))
    connection.commit()
    cursor.close()

def deleteProject(project, connection):
    cursor = connection.cursor()
    cursor.execute("delete from project where project_id = '%s'", (project.id,))
    connection.commit()
    cursor.close()

def createProject(connection, usrID):
    cursor = connection.cursor()
    projName = input("Project name: ")
    projHours = 0
    projUserID = usrID
    cursor.execute("insert into project (project_name, hours, user_id) values (%s, %s, %s)", (projName, projHours, projUserID))
    connection.commit()
    cursor.close()
def changeHours(project, connection):
    project.hours = int(input("New hours: "))
    cursor = connection.cursor()
    cursor.execute("update project set hours = %s where project_id = %s", (project.hours, project.id))
    connection.commit()
    cursor.close()

def changeName(project, connection):
    project.name = input("New name: ")
    cursor = connection.cursor()
    cursor.execute("update project set project_name = %s where project_id = %s", (project.name, project.id))
    connection.commit()
    cursor.close()

def refresh(connection):
    mycursor = connection.cursor()
    mycursor.execute("select * from project where user_id = %s", (usr.id,))


    rs = mycursor.fetchall()

    projects = []
    for each in rs:
        project_id = each[0]
        project_name = each[1]
        project_hours = each[2]
        project_user_id = each[3]
        projects.append(project(project_id, project_name, project_hours, project_user_id))
    mycursor.close()
    return projects



mydb = mysql.connector.connect(

    host="",
    user="",
    passwd="",
    database=""
)

mycursor = mydb.cursor()



userPrompt = input("Username? (or '+' to create new user): ")

if (userPrompt == "+"):
    newUser = input("New username: ")
    mycursor.execute("select exists(select * from user where username = %s)", (newUser,))
    rs = mycursor.fetchone()
    if rs[0] == 1:
        print ("User already exists. Exiting program.")
        exit()
    else:
        newPass = getpass.getpass("New Password: ")
        newPass = bcrypt.hashpw(newPass.encode(), bcrypt.gensalt())
        mycursor.execute("insert into user (username, pwd_hash) values (%s, %s)", (newUser, newPass))
        mydb.commit()
        userPrompt = newUser

mycursor.execute("Select * from user where username = %s", (userPrompt,))
rs = mycursor.fetchone()
mycursor.close()

usr = user()

usr.id = rs[0]
usr.name = rs[1]
usr.pwd_hash = rs[2]

pwd = getpass.getpass("Password: ")
check = bcrypt.checkpw(pwd.encode(), usr.pwd_hash.encode())

if not check:
    print("Wrong password. Exiting program.")
    quit()

projects = refresh(mydb)



while True:
    print("Select a project or '+' to create or  'exit' to exit.")
    for index, proj in enumerate(projects):
        print(index + 1, proj.name)
    usrInput = input()

    if usrInput == '+':
        createProject(mydb, usr.id)
        projects.clear()
        projects = refresh(mydb)
        continue
    if usrInput.lower() == "exit":
        mycursor.close()
        mydb.close()
        quit()
    else:
        while True:
            selection = int(usrInput) - 1
            if selection < len(projects):
                selection = projects[selection]
            else:
                print(clear)
                print("That project doesn't exist. Try again")
                break
            print(clear)
            print("1.Start Working 2.Delete 3.Edit name 4.Edit hours 5.Go back")
            print(selection)
            usrInput = input()
            if usrInput == "1":
                startTime = datetime.datetime.now()
                input("Press enter when finished...")
                elapsedTime = datetime.datetime.now() - startTime
                elapsedTime = elapsedTime.seconds // 60
                selection.hours += elapsedTime
                updateHours(selection, mydb)
            if usrInput == "2":
                deleteProject(selection, mydb)
                projects.clear()
                projects = refresh(mydb)
                break
            if usrInput == "3":
                changeName(selection, mydb)
                projects.clear()
                projects = refresh(mydb)
                break
            if usrInput == "4":
                changeHours(project, mydb)
                projects.clear()
                projects = refresh(mydb)
            if usrInput == "5":
                break
            else: break
                





