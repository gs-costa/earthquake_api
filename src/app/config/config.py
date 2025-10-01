from os import getenv


class Environment:
    POSTGRES_USER = getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = getenv("POSTGRES_DB", "postgres")
    POSTGRES_PORT = getenv("POSTGRES_PORT", 5432)
    POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
    POSTGRES_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    API_USERNAME = getenv("API_USERNAME", "admin")
    API_PASSWORD = getenv("API_PASSWORD", "admin")
    API_REALM = getenv("API_REALM", "EarthquakeAPI")
