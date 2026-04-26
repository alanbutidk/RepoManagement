from ok import Task, ArgumentNotGivenError

Task.wait(5)
print("Waited 5 seconds")
Task.FileExists("ok.py")
print(Task.SuccessFileExistsCode)
#DataList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#Task.WriteToFile("hello.py", data=DataList)
MyFileData = Task.ReadFromFile("hello.py")
#print(MyFileData)
Task.WriteToFile("hello.c", data=MyFileData)
Task.CheckArg("hello", tell=True)
Task.ExitWithoutDynamicErrors("Exit test", verbose=True)