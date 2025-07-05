from quixstreams import Application, State
from loguru import logger
from technical_indicator.candles import update_candles_to_state
from technical_indicator.indicators import compute_technical_indicators



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

    # Step 1. Ingest the data from candles input topic
    sdf = app.dataframe(topic = candles_topic)


    # Step 2. Keep only candles for the given 'candles seconds'
    sdf = sdf[sdf['candle_seconds'] == candle_seconds]

    # Step 3. Add candles to state dictionary
    sdf = sdf.apply(update_candles_to_state, stateful=True)

    # logging on console
    # sdf = sdf.update(lambda message: logger.debug(f'Input: {message}'))
    
    # sdf = sdf.update(lambda _: breakpoint())

    # Step 4. Calculate technical indicators
    sdf = sdf.apply(compute_technical_indicators, stateful=True)

    # Print it up on console
    sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))
    
    # Step 5. Send data to output topic
    sdf = sdf.to_topic(technical_indicators_topic)

    #Start the streaming app
    app.run()

    

if __name__ == "__main__":
    from technical_indicator.config import config
    from technical_indicator.table import create_table_in_risingwave

    create_table_in_risingwave(
        table_name=config.table_name_in_risingwave,
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_output_topic
    )

    
    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic = config.kafka_input_topic,
        kafka_output_topic= config.kafka_output_topic,
        kafka_consumer_group= config.kafka_consumer_group,
        candle_seconds = config.candle_seconds
    )