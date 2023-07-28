from dataclasses import dataclass

from src.functions import read_yaml


@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]


@dataclass
class DBConfig:
    host: str
    database: str
    user: str
    password: str


@dataclass
class LoggingConfig:
    level: str
    file: str
    format: str


@dataclass
class Config:
    bot: BotConfig
    db: DBConfig
    logging: LoggingConfig


def load_config(config_file: str) -> Config:
    data = read_yaml(config_file)

    return Config(
        bot=BotConfig(
            token=data['bot']['token'],
            admin_ids=data['bot']['admin_ids']
        ),
        db=DBConfig(
            database=data['db']['database'],
            host=data['db']['host'],
            user=data['db']['user'],
            password=data['db']['password']
        ),
        logging=LoggingConfig(
            level=data['logging']['level'],
            file=data['logging']['file'],
            format=data['logging']['format'],
        )
    )
