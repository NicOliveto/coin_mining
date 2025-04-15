BEGIN;

CREATE SCHEMA IF NOT EXISTS relational_tb;

CREATE TABLE relational_tb.currency_data (
	base_currency_id VARCHAR NOT NULL,
	target_currency_id VARCHAR NOT NULL,
	date_time TIMESTAMP NOT NULL,
	purchase_amt FLOAT NOT NULL,
	sale_amt FLOAT NOT NULL,
	PRIMARY KEY (base_currency_id, target_currency_id, date_time)
);

COMMIT;
