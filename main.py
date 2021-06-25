import commands


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data \
            else self.command.execute()
        print(message)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    print('Welcome to Swill!')
    commands.CreateBookmarksTableCommand().execute()
