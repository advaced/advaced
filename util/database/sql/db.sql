-- Blockchain table v1.0.0
CREATE TABLE IF NOT EXISTS blockchain (
    block_index INT(32) UNIQUE NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,

    version VARCHAR(16) NOT NULL,
    timestamp DATETIME NOT NULL,

    base_fee DECIMAL NOT NULL,

    hash VARCHAR(64) NOT NULL,

    validator VARCHAR(128) NOT NULL,
    signature VARCHAR(128) NOT NULL
);

-- Transaction table v1.0.0
CREATE TABLE IF NOT EXISTS transactions (
    block_index INT(32) NOT NULL,

    sender VARCHAR(128) NOT NULL,
    recipient VARCHAR(128) NOT NULL,

    amount INT(32) NOT NULL,
    fee INT(32) NOT NULL,

    type VARCHAR(32) NOT NULL,
    timestamp DATETIME NOT NULL,

    hash VARCHAR(64) NOT NULL,
    signature VARCHAR(128) NOT NULL
);

-- Wallets
CREATE TABLE IF NOT EXISTS accounts (
    name VARCHAR(32) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,

    private_key_hash VARCHAR(128) NOT NULL
);

-- Known-nodes-archive
CREATE TABLE IF NOT EXISTS nodes_archive (
    ip_address VARCHAR(32) NOT NULL,
    port INT(11) NOT NULL
);

-- Version stamps
CREATE TABLE IF NOT EXISTS version_stamps (
    version VARCHAR(16) NOT NULL,
    timestamp DATETIME NOT NULL,

    network VARCHAR(16) NOT NULL,

    public_key VARCHAR(128) NOT NULL,
    signature VARCHAR(128) NOT NULL
);

-- Developer public-keys
CREATE TABLE IF NOT EXISTS dev_keys (
    public_key VARCHAR(128) NOT NULL
);

-- Development tests
INSERT INTO version_stamps VALUES('1.0.0', '2022-03-10 10:07:17.687452', 'mainnet',
 '0521b81c2857947d986722fffdd54ccda0114a635ff19d6bc725e080cf26c7f76b0185a8a87f257e86d9d722922dabcdfffe8e06281b1295a539a2a081e4d56a', -- pub key
 '6d569b9363cd7467a16ea517576604cb3c6ebba4f101ed58fc7288b43701fae1726262fa8436307b5542996336222aec1fad25e21e093c7c2fb802c6e50d2350'); -- signature

INSERT INTO dev_keys VALUES('0521b81c2857947d986722fffdd54ccda0114a635ff19d6bc725e080cf26c7f76b0185a8a87f257e86d9d722922dabcdfffe8e06281b1295a539a2a081e4d56a');
