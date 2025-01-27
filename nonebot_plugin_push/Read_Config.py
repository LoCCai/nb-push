from pydantic import BaseSettings, Extra, Field


class Read_Time(BaseSettings):
    hour: int = Field(0,alias="HOUR")
    minute: int = Field(0,alias="MINUTE")

    class Config:
        extra = "allow"
        case_sensitive = False
        anystr_lower = True


class Read_Config(BaseSettings):
    # plugin custom config
    plugin_setting: str = "default"

    read_qq_friends: list[int]
    read_qq_groups: list[int]

    read_inform_time: list[Read_Time()] = []

    class Config:
        extra = Extra.allow
        case_sensitive = False
