import os


def _normalize_database_url(raw_url: str) -> str:
    url = raw_url.strip()

    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)

    if url.startswith("postgresql://") and "+" not in url.split("://", 1)[0]:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")

    mysql_user = os.getenv("MYSQL_USER", "root")
    mysql_password = os.getenv("MYSQL_PASSWORD", "")
    mysql_host = os.getenv("MYSQL_HOST", "localhost")
    mysql_port = os.getenv("MYSQL_PORT", "3306")
    mysql_db = os.getenv("MYSQL_DB", "chat_importer")
    use_sqlite_fallback = os.getenv("USE_SQLITE_FALLBACK", "true").lower() == "true"
    database_url = _normalize_database_url(os.getenv("DATABASE_URL", ""))

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
