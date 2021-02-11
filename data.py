def save(codicescuola, username, password):
    str = codicescuola + " : " + username + " : " + password

    f = open("data.txt", "w")
    f.write(str)
    f.close()

def delete():
    f = open("data.txt", "w")
    f.close()

def load():
    f = open("data.txt", "r")
    str = f.read()
    f.close()

    return str

def getCodice():
    str = load()
    pos = str.find(" : ")
    if(pos != -1):
        str = str[:pos]
    else:
        str = ""

    return str

def getUsername():
    str = load()
    pos = str.find(" : ")
    if pos != -1:
        str = str[pos+3:]
        pos = str.find(" : ")
        if pos != -1:
            str = str[:pos]
    else:
        str = ""

    return str

def getPassword():
    str = load()
    pos = str.find(" : ")
    if pos != -1:
        str = str[pos+3:]
        pos = str.find(" : ")
        if pos != -1:
            str = str[pos+3:]
    else:
        str = ""

    return str

def isEmpty():
    str = load()
    pos = str.find(" : ")
    return pos == -1