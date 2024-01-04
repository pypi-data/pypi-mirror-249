from spectral_cli.abis.abis import load_abis
import os
CONFIG_PATH = os.path.expanduser("~/.spectral/config_dev.ini")
ALCHEMY_URL = "https://arb-goerli.g.alchemy.com/v2/"
ABIS = load_abis()
MODELER_CONTRACT = "0x5d538650b17097142122be8B09404d400B1A28Ca"
PRIMARY_IPFS_LINK = "http://silver-absent-kite-292.mypinata.cloud/ipfs/"
SUBSCRIPTION_LIB_URL = "https://subscription-library.dev.spectral.finance"
CREDIT_SCORING_CONTRACT_ADDRESS = "0x0163655101Dd34f5a7D8cC9c52Fa60AfcED1c929"
CREDIT_SCORING_TRAINING_DATASET_IPFS_CID = "QmTqZdaVrHmh9kQFhEjeobk1p4FkhDB2uwZMUHsh6fgMcB"
VALIDATOR_WALLET_ADDRESS = "0xc001C50946AF123B8dD85171B05F43000feCfA22"
CHAIN_ID = 421613
GAS = 4000000
GAS_PRICE_GWEI = '0.12'
TX_EXPLORER_URL = "https://goerli.arbiscan.io/tx"

PLUMBER_URL = 'https://plumber.dev.spectral.finance'

os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
