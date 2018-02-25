def updateuser(sid, code, year):
    with open("userinfo.txt", "r+") as file:
        d = file.readlines()
        file.seek(0)
        for x in d:
            l = x.split(":")
            if l[0] != sid:
                file.write(x)
        file.write(sid+":"+code+":"+year+"\n")
        file.truncate()
        file.close

updateuser("4711","CA","123")