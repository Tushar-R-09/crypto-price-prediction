# Create an Application instance with Kafka configs
from quixstreams import Application
from kraken_api import KrakenAPI, Trade
from loguru import logger


def run(
        kafka_broker_address: str,
        kafka_topic_name: str,
        kraken_api: KrakenAPI
        ):
    app = Application(
        broker_address=kafka_broker_address
        ,consumer_group='example'
    )

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic_name
                      ,value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:

        while True:
            # Fetch the event from topic
            events: list[Trade] = kraken_api.get_trades()
            #event = {"id": "1", "text": "Lorem ipsum dolor sit amet"}
            # Serialize an event using the defined Topic 
            for event in events:
                message = topic.serialize(#key=event["id"],
                                         value=event.to_dict())

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name
                    , value=message.value
                   # , key=message.key
                )
                logger.info(f"Produced message: {topic.name}")
            
            # breakpoint()


if __name__ == "__main__":

    kraken_api = KrakenAPI(product_ids=["BTC/EUR"])
    run(kafka_broker_address="localhost:9092",
        kafka_topic_name="trades",
        kraken_api = kraken_api)