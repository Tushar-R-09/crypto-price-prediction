from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    product_id: list[str] = ["BTC/EUR"]
    kafka_broker_address: str 
    kafka_topic_name: str

    model_config = SettingsConfigDict(
        env_file="services/trades/settings.env",  # Use forward slashes for cross-platform compatibility
        env_file_encoding="utf-8"
    )

config = Settings()

#print(config.model_dump())
