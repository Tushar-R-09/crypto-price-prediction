from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="services/technical_indicator/settings.env",
        env_file_encoding="utf-8"
    )
    kafka_broker_address: str 
    kafka_input_topic: str 
    kafka_output_topic: str
    kafka_consumer_group: str
    candle_seconds: int

    max_candles_in_state: int = 70 

    table_name_in_risingwave: str = "technical_indicators"

    @classmethod
    def from_yaml(
        cls,
        path_to_yaml: str
    ):
        """
        Load the configuration of yaml file and return an instance of the Settings class
        """

config = Settings()

#print(config.model_dump())
