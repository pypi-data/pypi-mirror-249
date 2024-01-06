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
        self.level = 0
        self.money = 0
        self.functions.clear()

    def updatestats(self, level: int = 0, money: int = 0):

        self.level += level
        self.money += money

    def run(self):

        command = self.functions.ask(f"Commands: {', '.join(self.commands)}")
        self.functions.clear()
        if command.lower() in self.commands:
            return command.lower()
        else:
            self.functions.write("That is not a valid option")
            return
          
    def __str__(self):

        return f"{self.username}\n{(len(self.username) + 1) * '-'}\nLevel: {self.level}\nMoney: {self.money}\n"
    
