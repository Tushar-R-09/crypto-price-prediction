from quixstreams import Application
from loguru import logger


def init_candle(trade: dict) -> dict:

    """
    Initialize the candle with the first trade
    Returns the initial candle state

    """

    return {
        'open': trade['price'],
        'high': trade['volume'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['quantity'],
        'pairs': trade['product_id']
    }

def update_candle(candle: dict, trade: dict) -> dict:
    """
    Takes the candle and new state, update the current state of the candle

    Args: 
        candle (dict): current state of the candle
        trade (dict): new state of the candle

    Returns:
        dict: updated candle state
    
    """

    # Open price doesn't change, so there is no update to it
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['close'] = trade['price']
    candle['volume'] += trade['quantity']

    return candle

def run(
        # kafka parameters
        kafka_broker_address: str,
        kafka_input_topic: str,
        kafka_output_topic: str,

        # candle parameters
        candle_seconds: int,
        emit_incomplete_candle: bool = True
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
    #sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))

    #Aggeregation of trades into candles using tumbling windows
    from datetime import timedelta
    sdf = (
        sdf.tumbling_window(
        timedelta(seconds=candle_seconds))
        #create a "reduce" aggregation with "reducer" and "initializer" functions
        .reduce(reducer=update_candle, initializer = init_candle)
    )

    if emit_incomplete_candle:
        # Emit incomplete candles
        sdf = sdf.current()

    else:
        # Emit only complete candles
        sdf = sdf.final()

    # Send data to output topic
    sdf = sdf.to_topic(candles_topic)

    #Start the streaming app
    app.run()

    

if __name__ == "__main__":
    run(
        kafka_broker_address="localhost:31234",
        kafka_input_topic = "trades",
        kafka_output_topic="candles",
        candle_seconds = 60
    )