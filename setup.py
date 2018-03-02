import pip

packages = ['ujson', 'google', 'wikipedia', 'requests', 'discord.py']

print("installing packages:")
try:
    for package in packages:
        print("package \n")
        pip.main('install', package)
    print("all done, now start the bot by running")
    print("python3 main.py")

except Exception:
    print("something went wrong")
