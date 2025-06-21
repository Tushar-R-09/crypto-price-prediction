from technical_indicator.config import config
from quixstreams import State

def are_same_window(candle: dict, previous_candle: dict) -> bool:
    """
    Check if two candles belong to the same time window and crypto currency.

    Args:
        candle (dict): The current candle.
        previous_candle (dict): The previous candle.

    Returns:
        bool: True if both candles belong to the same time window, False otherwise.
    """
    return (
        candle["pair"] == previous_candle["pair"] and
        candle['window_start_ms'] == previous_candle['window_start_ms'] and
        candle['window_end_ms'] == previous_candle['window_end_ms']
    )

def update_candles_to_state(candle: dict, state: State):
        """
        Takes the current state (with the list of N previous candles) and the new candle,
        and updates the state with the new candle.

        It can either happen that the new candle is part of the same window
        (i.e. it has the same start and end time as the last candle in the state),
        or it is a new window (i.e. it has a different start and end time than the last candle in the state).

        Args:
            candle (dict): The new candle to add to the state.
            state (State): The current state of the application with list of N previous candles.

        Returns:
            dict: The updated state.
        """
        candles = state.get('candles', default=[])
        # We need to check if the candles belong to same window second
        # (window_start_ms, window_end_ms) as candles[-1]
        if not candles:
             candles.append(candle)
        if are_same_window(candle, candles[-1]):
            candles[-1] = candle
        else:
            candles.append(candle)
        
        
        if len(candles) > config.max_candles_in_state:
            # Remove the oldest candle if we exceed the max candles in state
            candles.pop(0)
        state.set('candles', candles)

        return candle