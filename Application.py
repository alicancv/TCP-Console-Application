import UserClass
from UserClass import User
from os import system


logged = False
command = ""
current_user = None

authentication_dictionary = {
    "admin": "admin123",
    "user1": "user1123",
    "user2": "user2123",
    "user3": "user3123",
}

user_dictionary = {
    "admin": UserClass.admin,
    "user1": UserClass.user1,
    "user2": UserClass.user2,
    "user3": UserClass.user3,
}


command_dictionary = {0: "help",
                      1: "authentication", 2: "register", 3: "send message", 4: "show messages", 5: "change group", 6: "make search on messages"}


def writeConnectionList():
    for i in current_user.connections.keys():
        print(f"group: {current_user.groups[i]} connection name: {i}")


def writeCommands():
    print("Avaliable Commands:")
    for i, j in command_dictionary.items():
        if logged == True:
            if i in range(1, 3):
                pass
            else:
                print(f"{i}:{j} ")
        if logged == False:
            if i in range(3, len(command_dictionary)):
                pass
            else:
                print(f"{i}:{j} ")
    print()


def register(username, password, server, port):
    can_register = True

    for i in username:
        if i == ":":
            can_register = False

    if can_register:
        new_user = User(username, password, int(port))
        authentication_dictionary[username] = password
        user_dictionary[username] = new_user
    else:
        print("forbidden character ':' in the username")


def authenticate(user_info):
    if user_info in authentication_dictionary.items():
        return user_dictionary[user_info[0]]
    else:
        return None


def switch(x, dict):
    try:
        if int(x) in dict.keys():
            return dict[int(x)]
    except:
        return "no such a command"


def checkCommand(command):
    request = switch(command, command_dictionary)
    global logged
    global current_user
    if request == "authentication":
        if logged == True:
            return
        while True:
            print("enter your username:")
            username = input()
            print("enter your password:")
            password = input()
            current_user = authenticate((username, password))
            if current_user != None:
                already_connected = current_user.startListen()
                if already_connected:
                    logged = False
                    print(
                        "this user is already connected or a different problem occured")
                    current_user = None
                    break
                logged = True
                break
            else:
                print("username or password is wrong")
                break
    elif request == "register":
        if logged == True:
            return
        print("enter a free port:")
        port = input()
        print("enter a username:")
        username = input()
        print("enter a password:")
        password = input()
        register(username, password, UserClass._server, port)
    elif request == "no such a command":
        print(request)
    elif request == "help":
        print("contact with Alican Sucu 171180062")
    elif request == "send message":
        if logged == False:
            return
        print("Connection List")
        writeConnectionList()
        print("write a connection name to send message to this connection:")
        friend = input()
        if friend in current_user.connections.keys():
            system("cls")
            print("enter '!exit!' to end sending messages")
            try:
                current_user.clientConnect(
                    UserClass._server, current_user.connections[friend])
                messaging = True
            except:
                print(
                    f"failed to connect with other {friend} or a different problem occurred")
                messaging = False

            if messaging:
                while True:
                    msg = input()
                    if msg == "!exit!":
                        current_user.clientDisconnect()
                        break
                    else:
                        current_user.sendMessage(
                            f"{current_user.username}: {msg}")
                        if friend in current_user.message_box.keys():
                            current_user.message_box[friend].append(
                                f"{current_user.username}: {msg}")
                        else:
                            current_user.message_box[friend] = [
                                f"{current_user.username}: {msg}"]
        else:
            print("no such a connection")
    elif request == "show messages":
        writeConnectionList()
        print("write a connection name to show old messages with this connection:")
        friend = input()
        if friend in current_user.connections.keys():
            if friend in current_user.message_box.keys():
                system("cls")
                print(f"messages with {friend}")
                for i in current_user.message_box[friend]:
                    print(i)
            else:
                print(f"you haven't talked yet with {friend}")
        else:
            print("no such a connection")
    elif request == "change group":
        writeConnectionList()
        print("write a connection name to change group of this connection:")
        friend = input()
        if friend in current_user.connections.keys():
            print("what is the new group of this connection:")
            new_group = input()
            if new_group in current_user.groups.values():
                current_user.groups[friend] = new_group
            else:
                print("no such a group")
        else:
            print("no such a connection")
    elif request == "make search on messages":
        print("enter the word you want to search in your messages")
        word = input()
        tmp = []
        for i in current_user.message_box.values():
            for j in i:
                if j.find(word) != -1:
                    print(j)
                    tmp.append(j)
        print(f"\n{len(tmp)} messages have {word} in it")


def main():
    while True:
        if logged:
            print(f"Hello {current_user.username}!")
        writeCommands()
        print("Please enter a command:")
        command = input()
        checkCommand(command)


if __name__ == "__main__":
    main()
