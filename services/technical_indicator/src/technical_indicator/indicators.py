from talib import stream
from loguru import logger
import numpy as np
def compute_technical_indicators(
        candle: dict,
        state: dict,
):
    candles = state.get('candles', default=[])

    logger.debug(f"no of candles is : {len(candle)}")

    # Extract the open, close, high, low, volume candles
    open = np.array([c['open'] for c in candles])  # Extract close prices from candles
    high = np.array([c['high'] for c in candles]) 
    low = np.array([c['low'] for c in candles]) 
    close = np.array([c['close'] for c in candles]) 
    volume = np.array([c['volume'] for c in candles]) 

    indicators = {}
    #Simple moving average
    # - window: 7
    # - window : 14
    #indicators["sma_1"] = stream.SMA(close, timeperiod = 1)
    indicators["sma_7"] = stream.SMA(close, timeperiod = 7)
    indicators["sma_14"] = stream.SMA(close, timeperiod = 14)
    indicators["sma_21"]= stream.SMA(close, timeperiod = 21)
    indicators["sma_60"] = stream.SMA(close, timeperiod = 60)

    #breakpoint()  # Debugging breakpoint, remove in production

    return {
        **candle,  # Include the original candle data
        **indicators,  # Include the computed indicators
    }