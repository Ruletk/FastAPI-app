from envparse import Env


env = Env()


REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://fastapi:fastapi@192.168.3.2:5432/fastapi",
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://fastapi:fastapi@192.168.3.2:5432/fastapi_test",
)
