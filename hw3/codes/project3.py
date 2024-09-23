import subprocess

selection=input("Select a model:rdt1.0,rdt2.0,rdt3.0,tcp\n")



if selection=="rdt1.0":
    subprocess.run(["python", "rdt1main.py"])
elif selection=="rdt2.0":
    subprocess.run(["python", "rdt2main.py"])
elif selection=="rdt3.0":
    subprocess.run(["python", "rdt3main.py"])
elif selection=="tcp":
    subprocess.run(["python", "tcpmain.py"])
else:
    print("Invalid input ")
