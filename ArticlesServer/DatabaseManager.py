from .generate_articles_database import generate_articles_database


class DatabaseManager:
    _currentDatabase = None

    @staticmethod
    def get_instance():
        return DatabaseManager._currentDatabase

    @staticmethod
    def reload_database(doi_list, finder):
        DatabaseManager._currentDatabase = generate_articles_database(doi_list, finder)
