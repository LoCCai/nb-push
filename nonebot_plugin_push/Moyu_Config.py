from pydantic import BaseSettings, Extra, Field


class Moyu_Time(BaseSettings):
    hour: int = Field(0,alias="HOUR")
    minute: int = Field(0,alias="MINUTE")

    class Config:
        extra = "allow"
        case_sensitive = False
        anystr_lower = True


class Moyu_Config(BaseSettings):
    # plugin custom config
    plugin_setting: str = "default"

    moyu_qq_friends: list[int]
    moyu_qq_groups: list[int]

    moyu_inform_time: list[Moyu_Time()] = []

    class Config:
        extra = Extra.allow
        case_sensitive = False
