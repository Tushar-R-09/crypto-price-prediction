from quixstreams import Application
from loguru import logger

def run(
        # kafka parameters
        kafka_broker_address: str,
        kafka_input_topic: str,
        kafka_output_topic: str,

        # candle parameters
        candle_sec: int
        ):
    """
    Transform a stream of input trades into stream of output candles.

    In 3 steps:
     - Ingest trade from kafka_input_topic
     - Aggregate trades into candles
     - Produce candles to kafka_output_topic
     Arguments:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic name
        kafka_output_topic (str): Kafka output topic name
        candle_sec (int): Candle duration in seconds
    Raises:
        None
    """
    app = Application(
        broker_address=kafka_broker_address
        ,consumer_group='example'
    )

    #Input topic
    trades_topic = app.topic(name=kafka_input_topic, value_serializer='json')

    #Output topic
    candles_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    #Ingest the data
    sdf = app.dataframe(topic = trades_topic)

    # Print it up
    sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))

    # Send data to output topic
    sdf = sdf.to_topic(candles_topic)

    #Start the streaming app
    app.run()

    

if __name__ == "__main__":
    run(
        kafka_broker_address="localhost:31234",
        kafka_input_topic = "trades",
        kafka_output_topic="candles",
        candle_sec = 60
    )