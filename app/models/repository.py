import os
import time

from time import mktime
from datetime import datetime
from git import Repo

class Repository(object):

    def __init__(self, repo, name):
        self.repo = repo;
        self.name = name

    def get_updated_at(self):
        return self.__get_date_time(self.repo.head.commit.committed_date)

    def added_files(self):
        return self.__filter_changes("A")

    def deleted_files(self):
        return self.__filter_changes("D")

    def modified_files(self):
        return self.__filter_changes("M")

    def list_files(self):
        return [blob.name for blob in self.repo.head.commit.tree.blobs]

# Private
    def __get_date_time(self, timestamp):
        t = time.gmtime(self.repo.head.commit.committed_date)
        return datetime.fromtimestamp(mktime(t))

    def __filter_changes(self, change_type):
        return [change for change in 
                self.repo.commit("HEAD~1").diff().iter_change_type(change_type)]


# Class methods
    def all(directory):
        return [Repository.find(directory, name) for name in os.listdir(directory)
                            if os.path.isdir(os.path.join(directory, name))
                            and Repository.__is_repo(os.path.join(directory, name))]

    def find(repo_directory, repository_name):
        repo_path = os.path.join(repo_directory, repository_name)
        if os.path.isdir(repo_path) and Repository.__is_repo(repo_path):
            return Repository(Repo(repo_path), repository_name)
        else:
            return None

    def __is_repo(directory):
        try:
            Repo(directory)
        except:
            return False
        return True
