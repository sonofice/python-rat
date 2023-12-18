cmnd = "user"

if cmnd.lower == "exit":
    print("exiting")
    #cmnd = cmnd.encode()
    #conn.sendall(cmnd)
    #break
if cmnd.lower == "listdir":
    result = os.path.dirname(os.path.realpath(__file__))
    print(result)
if cmnd.lower == "user":
    result = os.getlogin()
    print(result)

else:
    result = "passing"
    pass

print(result)
