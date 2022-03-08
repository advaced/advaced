-- Blockchain table v1.0.0
CREATE TABLE blockchain (
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

-- Wallets
CREATE TABLE accounts (
    name VARCHAR(32) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,

    public_key VARCHAR(128) NOT NULL,
    private_key_hash VARCHAR(128) NOT NULL -- sault: password
);

-- Known-nodes-archive
CREATE TABLE nodes_archive (
    ip_address VARCHAR(32) NOT NULL,
    port INT(11) NOT NULL
);

-- Versionstamps
CREATE TABLE versionstamps (
    version VARCHAR(16) NOT NULL,
    timestamp DATETIME NOT NULL,

    signature VARCHAR(128) NOT NULL
);

-- Developer public-keys
CREATE TABLE dev_keys (
    public_key
);

-- Nodes to burn
CREATE TABLE to_burn (
    address VARCHAR(128) NOT NULL,

    -- The wrong data the block spread
    data TEXT NOT NULL
);
