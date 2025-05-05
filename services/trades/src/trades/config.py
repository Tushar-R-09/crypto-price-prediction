from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="services/trades/settings.env",
        env_file_encoding="utf-8"
    )
    
    product_id: list[str] = ["BTC/USD", "BTC/EUR", "ETH/EUR", "ETH/USD", "SOL/USD", "SOL/EUR", "XRP/USD", "XRP/EUR"]
    kafka_broker_address: str = Field(..., alias="KAFKA_BROKER_ADDRESS")
    kafka_topic_name: str = Field(..., alias="KAFKA_TOPIC_NAME")

config = Settings()

#print(config.model_dump())
