import logging
import os
from dataclasses import dataclass

from environs import Env



@dataclass
class BotSettings:
    token: str
    admin_ids: list[int]

@dataclass
class OpenAiSettings:
    api_key: str
    model: str
    temperature: float
    system_prompt: str

@dataclass
class GoogleCalendar:
    api_key: str
    token_file: str



@dataclass
class DatabaseSettings:
    name: str
    port: int
    host: str
    user: str
    password: str



@dataclass
class RedisSettings:
    host: str
    port: int
    db: int
    password: str
    username: str


@dataclass
class Config:
    bot: BotSettings
    db: DatabaseSettings
    redis: RedisSettings
    OpenAi: OpenAiSettings
    Calendar: GoogleCalendar



def get_config() -> Config:
    env = Env()
    env.read_env()

    bot_token = env.str("BOT_TOKEN")
    admin_ids = env.int("ADMIN_IDS")

    db = DatabaseSettings(
        name=env.str("POSTGRES_DB"),
        host=env("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        user=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD")
    )

    redis = RedisSettings(
        host=env("REDIS_HOST"),
        port=env.int("REDIS_PORT"),
        db=env.int("REDIS_DATABASE"),
        password=env("REDIS_PASSWORD", default=""),
        username=env("REDIS_USERNAME", default=""),
    )

    OpenAi = OpenAiSettings(
        api_key=env("OPENAI_API_KEY"),
        model=env("OPENAI_MODEL"),
        temperature=env.float("OPENAI_TEMPERATURE", default=0.7),
        system_prompt=env("OPENAI_SYSTEM_PROMPT")
    )

    Calendar = GoogleCalendar(
        api_key=env("GOOGLE_CREDENTIALS_FILE"),
        token_file=env("GOOGLE_TOKEN_FILE"),
    )

    return Config(
        bot=BotSettings(
            token=bot_token,
            admin_ids=admin_ids
        ),
        db=db,
        redis=redis,
        OpenAi=OpenAi,
        Calendar=Calendar
    )