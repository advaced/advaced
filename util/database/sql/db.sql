-- Blockchain table v1.0.0
CREATE TABLE blockchain (
    block_index INT(32) UNIQUE NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,

    version VARCHAR(5) NOT NULL,
    timestamp DATETIME NOT NULL,

    base_fee DECIMAL NOT NULL,

    hash VARCHAR(64) NOT NULL,

    validator VARCHAR(128) NOT NULL,
    signature VARCHAR(128) NOT NULL
);

-- Transaction table v1.0.0
CREATE TABLE transactions (
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

-- Known-nodes-archive
CREATE TABLE nodes_archive (
    ip_address VARCHAR(32) NOT NULL,
    port INT(11) NOT NULL
);

-- Nodes to burn
CREATE TABLE to_burn (
    address VARCHAR(128) NOT NULL,

    -- The wrong data the block spread
    data TEXT NOT NULL
);
