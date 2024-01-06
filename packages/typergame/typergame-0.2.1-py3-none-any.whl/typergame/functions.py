import os, sys, time

class Functions:

    def __init__(self, defaultdelay: int, defaultnewline: bool):

        self.defaultdelay = defaultdelay
        self.defaultnewline = defaultnewline

    def clear(self):

        try:
            os.system("cls")
        except:
            os.system("clear")

    def pause(self, delay: str):

        time.sleep(delay)

    def write(self, text: str, delay: int = None, newline: bool = None):

        if delay == None:
            runningdelay = self.defaultdelay
        else:
            runningdelay = delay
        if newline == None:
            runningnewline = self.defaultnewline
        else:
            runningnewline = newline
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            self.pause(runningdelay)
        if runningnewline:
            print()

    def ask(self, question: str, delay: int = None):

        self.write(question, delay, True)
        return input("> ")

