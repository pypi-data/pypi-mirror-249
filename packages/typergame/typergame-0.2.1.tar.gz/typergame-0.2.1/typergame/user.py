from .functions import Functions

class User:

    def __init__(self, projectname: str, commands: list, defaultdelay: int, defaultnewline: bool):
        
        self.functions = Functions(defaultdelay, defaultnewline)
        self.projectname = projectname
        runningcommands = []
        for command in commands:
            runningcommands.append(command.lower())
        self.commands = runningcommands
        self.functions.clear()
        self.functions.write(f"Welcome to {self.projectname}")
        self.username = self.functions.ask("Choose a username")
        self.stats = {}
        self.functions.clear()

    def addstats(self, stat: str):

        self.stats[stat.lower()] = 0

    def updatestats(self, stat: str, value: int):

        self.stats[stat.lower()] += value

    def run(self):

        command = self.functions.ask(f"Commands: {', '.join(self.commands)}")
        self.functions.clear()
        if command.lower() in self.commands:
            return command.lower()
        else:
            self.functions.write("That is not a valid option")
            self.functions.clear()
            return
          
    def __str__(self):

        runningstats = ""
        for stat in list(self.stats.keys()):
            runningstats += f"{stat.lower()}: {self.stats[stat]}\n"
        return f"{self.username}\n{(len(self.username) + 1) * '-'}\n{runningstats}"
    
