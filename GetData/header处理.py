with open("headers","r") as header_text:
    for item in header_text.readlines()[0:-2]:
        index = item[0:-1].find(":")
        print("\""+item[0:index]+"\":\""+item[index+2:-1]+"\",")