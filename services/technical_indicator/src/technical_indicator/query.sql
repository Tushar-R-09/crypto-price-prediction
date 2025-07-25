CREATE TABLE technical_indicators (
	pair VARCHAR,
	open FLOAT,
	high FLOAT,
	low FLOAT,
	close FLOAT,
	volume FLOAT,
	window_start_ms BIGINT,
	window_end_ms BIGINT,
	candle_seconds INT,
	sma_7 FLOAT,
	sma_14 FLOAT,
	sma_21 FLOAT,
	sma_60 FLOAT,
	ema_7 FLOAT,
	ema_14 FLOAT,
	ema_21 FLOAT,
	ema_60 FLOAT,
	rsi_7 FLOAT,
	rsi_14 FLOAT,
	rsi_21 FLOAT,
	rsi_60 FLOAT,
	macd_7 FLOAT,
	macdsignal_7 FLOAT,
	macdhist_7 FLOAT,
	obv FLOAT,
    
    PRIMARY KEY (pair, window_start_ms, window_end_ms)
) WITH (
    connector='kafka',
    topic='technical_indicators',
    properties.bootstrap.server='kafka-e11b-kafka-bootstrap.kafka.svc.cluster.local:9092'
) FORMAT PLAIN ENCODE JSON;