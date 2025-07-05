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
    # Simple Moving Average (SMA) for different periods
    # indicators['sma_1'] = stream.SMA(close, timeperiod=1) # just to check the type
    indicators['sma_7'] = stream.SMA(close, timeperiod=7)
    indicators['sma_14'] = stream.SMA(close, timeperiod=14)
    indicators['sma_21'] = stream.SMA(close, timeperiod=21)
    indicators['sma_60'] = stream.SMA(close, timeperiod=60)

    # Exponential Moving Average (EMA) for different periods
    indicators['ema_7'] = stream.EMA(close, timeperiod=7)
    indicators['ema_14'] = stream.EMA(close, timeperiod=14)
    indicators['ema_21'] = stream.EMA(close, timeperiod=21)
    indicators['ema_60'] = stream.EMA(close, timeperiod=60)

    # Relative Strength Index (RSI) for different periods
    indicators['rsi_7'] = stream.RSI(close, timeperiod=7)
    indicators['rsi_14'] = stream.RSI(close, timeperiod=14)
    indicators['rsi_21'] = stream.RSI(close, timeperiod=21)
    indicators['rsi_60'] = stream.RSI(close, timeperiod=60)

    # Moving Average Convergence Divergence (MACD) for different periods
    indicators['macd_7'], indicators['macdsignal_7'], indicators['macdhist_7'] = (
        stream.MACD(close, fastperiod=7, slowperiod=14, signalperiod=9)
    )

    # On-Balance Volume (OBV)
    indicators['obv'] = stream.OBV(close, volume)

    # breakpoint()
    return {
        **candle,  # Include the original candle data
        **indicators,  # Include the computed indicators
    }