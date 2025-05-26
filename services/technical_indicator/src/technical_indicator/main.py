from quixstreams import Application
from loguru import logger



def run(
        # kafka parameters
        kafka_broker_address: str,
        kafka_input_topic: str,
        kafka_output_topic: str,
        kafka_consumer_group: str,
        # candle parameters
        candle_seconds: int
        ):
    """
    Transform a stream of input candles into stream of technical indicators.

    In 3 steps:
     - Ingest candles from kafka_input_topic
     - Aggregate candles into technical indicators
     - Produce technical indicators to kafka_output_topic
     Arguments:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic name
        kafka_output_topic (str): Kafka output topic name
        kafka_consumer_group (str): Kafka consumer group name
        candle_sec (int): Candle duration in seconds
    Raises:
        None
    """
    app = Application(
        broker_address=kafka_broker_address
        ,consumer_group=kafka_consumer_group
    )

    #Input topic
    candles_topic = app.topic(name=kafka_input_topic, value_serializer='json')

    #Output topic
    technical_indicators_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    #Ingest the data from candles topic
    sdf = app.dataframe(topic = candles_topic)


    # Keep only candles for the given 'candles seconds'
    sdf = sdf[sdf['candle_seconds'] == candle_seconds]

    # Step 2. Compute technical indicators

    # Print it up
    sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))
    
    # Send data to output topic
    sdf = sdf.to_topic(technical_indicators_topic)

    #Start the streaming app
    app.run()

    

if __name__ == "__main__":
    from technical_indicator.config import config
    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic = config.kafka_input_topic,
        kafka_output_topic= config.kafka_output_topic,
        kafka_consumer_group= config.kafka_consumer_group,
        candle_seconds = config.candle_seconds
    )