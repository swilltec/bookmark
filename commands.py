import sys
import requests
from datetime import datetime
from abc import ABC, abstractmethod

from persistence import BookmarkDatabase


persistence = BookmarkDatabase()


class Command(ABC):

    @abstractmethod
    def execute(self, data):
        pass


class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        persistence.create(data)
        return True, None


class ListBookmarksCommand(Command):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self, data=None):
        return True, persistence.list(order_by=self.order_by)


class DeleteBookmarkCommand(Command):
    def execute(self, data):
        persistence.delete(data)
        return True, None


class EditBookmarkCommand(Command):
    def execute(self, data):
        persistence.edit(data)
        return True, None


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

        return True, f'Imported {bookmarks_imported} bookmarks from starred repos!'


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()
