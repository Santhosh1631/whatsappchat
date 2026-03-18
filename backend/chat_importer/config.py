import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")

    mysql_user = os.getenv("MYSQL_USER", "root")
    mysql_password = os.getenv("MYSQL_PASSWORD", "")
    mysql_host = os.getenv("MYSQL_HOST", "localhost")
    mysql_port = os.getenv("MYSQL_PORT", "3306")
    mysql_db = os.getenv("MYSQL_DB", "chat_importer")
    use_sqlite_fallback = os.getenv("USE_SQLITE_FALLBACK", "true").lower() == "true"
    database_url = os.getenv("DATABASE_URL", "").strip()

    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    elif use_sqlite_fallback and not mysql_password:
        SQLALCHEMY_DATABASE_URI = "sqlite:///chat_importer_dev.db"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "25")) * 1024 * 1024
