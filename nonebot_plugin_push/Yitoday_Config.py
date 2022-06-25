from pydantic import BaseSettings, Extra, Field


class Yitoday_Time(BaseSettings):
    hour: int = Field(0,alias="HOUR")
    minute: int = Field(0,alias="MINUTE")

    class Config:
        extra = "allow"
        case_sensitive = False
        anystr_lower = True


class Yitoday_Config(BaseSettings):
    # plugin custom config
    plugin_setting: str = "default"

    yitoday_qq_friends: list[int]
    yitoday_qq_groups: list[int]

    yitoday_inform_time: list[Yitoday_Time()] = []

    class Config:
        extra = Extra.allow
        case_sensitive = False
