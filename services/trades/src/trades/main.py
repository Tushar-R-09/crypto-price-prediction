# Create an Application instance with Kafka configs
from loguru import logger
from quixstreams import Application

from trades.kraken_api import KrakenAPI, Trade


def run(
        kafka_broker_address: str,
        kafka_topic_name: str,
        kraken_api: KrakenAPI
        ):
    app = Application(
        broker_address=kafka_broker_address
    )

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic_name
                      ,value_serializer='json'
                      # Can be used from quixstream models import TopicConfig to configure topic if it doesn't exist
                      #, config = TopicConfig(replication_factor=2, num_partitions=2)
                      )

    # Create a Producer instance
    with app.get_producer() as producer:

        while True:
            # Fetch the event from topic
            events: list[Trade] = kraken_api.get_trades()
            #event = {"id": "1", "text": "Lorem ipsum dolor sit amet"}
            # Serialize an event using the defined Topic
            for event in events:
                message = topic.serialize(key=event.product_id,
                                         value=event.to_dict())

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name
                    , value=message.value
                    , key=message.key
                )
                logger.info(f"Produced message: {topic.name}")
                logger.info(f"Trades pushed to kafka{event.to_dict()}")

            # breakpoint()


if __name__ == "__main__":
    from trades.config import config
    kraken_api = KrakenAPI(product_ids=config.product_id)
    #print(config.model_dump())
    run(kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name= config.kafka_topic_name,
        kraken_api = kraken_api)
