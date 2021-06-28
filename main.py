import os
from collections import OrderedDict

import commands


def format_bookmark(bookmark):
    return '\t'.join(
        str(field) if field else ''
        for field in bookmark
    )


class Option:
    def __init__(self, name, command, prep_call=None,
                 success_message='{result}'):
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.success_message = success_message

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        success, result = self.command.execute(data)

        formatted_result = ''

        if isinstance(result, list):
            for bookmark in result:
                formatted_result += '\n' + format_bookmark(bookmark)
        else:
            formatted_result = result

        if success:
            print(self.success_message.format(result=formatted_result))

    def __str__(self):
        return self.name


def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def get_github_import_options():
    return {
        'github_username': get_user_input('Github username'),
        'preserve_timestamps': get_user_input(
            'Preserve timestamps [Y/N]', required=False) in {'Y', 'y', None},
    }


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice')
        choice = input('Choose an option: ')
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False)
    }

def get_new_bookmark_info():
    return{
        'id': get_user_input('Enter bookmark ID to edit'),
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False)
    }


def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark ID to delete')


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def loop():
    clear_screen()
    print_options(options)
    chosen_option = get_option_choice(options)
    chosen_option.choose()
    _ = input('Press ENTER to return to menu: ')


if __name__ == '__main__':
    print('Welcome to Swill!')

    options = OrderedDict({
        'A': Option('Add a bookmark', commands.AddBookmarkCommand(),
                    prep_call=get_new_bookmark_data,
                    success_message='Bookmark added!'),
        'B': Option('List bookmarks by date',
                    commands.ListBookmarksCommand()),
        'T': Option('List bookmarks by title',
                    commands.ListBookmarksCommand(order_by='title')),

        'E': Option('Edit a bookmark',
                    commands.EditBookmarkCommand(),
                    prep_call=get_new_bookmark_info,
                    success_message='Bookmark updated!'
                    ),

        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(),
                    prep_call=get_bookmark_id_for_deletion,
                    success_message='Bookmark deleted!',
                    ),
        'G': Option('Import GitHub stars',
                    commands.ImportGithubStarsCommand(),
                    prep_call=get_github_import_options,
                    success_message='Imported {result} bookmarks from starred repos!'
                    ),
        'Q': Option('Quit', commands.QuitCommand()),
    })
    while True:
        loop()
