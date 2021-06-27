import sys
import requests
from datetime import datetime
from abc import ABC, abstractmethod
 
from database import DatabaseManager


db = DatabaseManager('bookmarks.db')


class Command(ABC):
    
    @abstractmethod
    def execute(self, data):
        pass

class CreateBookmarksTableCommand(Command):
    def execute(self):
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null'
        })


class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!'


class ListBookmarksCommand(Command):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand(Command):
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted!'


class QuitCommand(Command):
    def execute(self):
        sys.exit()


class ImportGithubStarsCommand(Command):

    def _extract_bookmark_info(self, repo):
        return {
            'title': repo.get('name'),
            'url': repo.get('html_url'),
            'notes': repo.get('description'),
        }

    def execute(self, data):
        bookmarks_imported = 0

        github_username = data.get('github_username')
        next_page_of_results = \
            f'https://api.github.com/users/{github_username}/starred'

        while next_page_of_results:
            print('Loading')
            stars_response = requests.get(
                next_page_of_results,
                headers={'Accept': 'application/vnd.github.v3.star+json'},
            )
            next_page_of_results = \
                stars_response.links.get('next', {}).get('url')

            for repo_info in stars_response.json():
                repo = repo_info.get('repo')

                if data.get('preserve_timestamp'):
                    timestamp = datetime.strptime(
                        repo_info.get('starred_at'), '%Y-%m-%dT%H:%M:%SZ')
                else:
                    timestamp = None

                bookmarks_imported += 1

                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo),
                    timestamp=timestamp,
                )

        return f'Imported {bookmarks_imported} bookmarks from starred repos!'
