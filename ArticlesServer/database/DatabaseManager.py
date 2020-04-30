from .generate_articles_database import generate_articles_database_from_files


class DatabaseManager:
    _currentDatabase = None

    @staticmethod
    def get_instance():
        return DatabaseManager._currentDatabase

    @staticmethod
    def reload_database():
        DatabaseManager._currentDatabase = generate_articles_database_from_files()
