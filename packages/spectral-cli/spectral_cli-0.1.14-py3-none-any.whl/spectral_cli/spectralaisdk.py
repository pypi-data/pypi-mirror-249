from functools import wraps
from pyarrow import ArrowInvalid
from retrying import retry
from spectral_cli.config_manager import ConfigManager
from tqdm import tqdm
from web3 import Web3
import click
import os
import pandas as pd
import requests
# from . import CONFIG_PATH, ALCHEMY_URL, ABIS # works for pip package
# works for direct calling
from spectral_cli import CONFIG_PATH, ALCHEMY_URL, ABIS, MODELER_CONTRACT, \
    PRIMARY_IPFS_LINK, SUBSCRIPTION_LIB_URL, CREDIT_SCORING_CONTRACT_ADDRESS, \
    CREDIT_SCORING_TRAINING_DATASET_IPFS_CID, VALIDATOR_WALLET_ADDRESS, \
    CHAIN_ID, GAS, GAS_PRICE_GWEI, TX_EXPLORER_URL

from spectral_cli.ezkl_wrapper.ezkl_wrapper import dump_model, upload_file_to_ipfs, generate_settings_file

config_manager = None


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_from_ipfs(cid, filename, file_type="File"):
    primary_source = PRIMARY_IPFS_LINK
    url = primary_source + cid

    try:
        # Make the GET request to fetch the file content
        response = requests.get(url, timeout=(3, 8), stream=True)

        # Check if the request was successful
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8K
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        # Save the content to the specified file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                progress_bar.update(len(chunk))

        progress_bar.close()
        print(f"{file_type} successfully downloaded!")

    except Exception as e:
        print(
            "Failed to fetch the file from the official gateway. Trying another gateway...")
        response = requests.post(
            "http://ipfs.spectral.finance:5001/api/v0/cat?arg=" + cid)

        # Check if the request was successful
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8K
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        # Save the content to the specified file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                progress_bar.update(len(chunk))

        progress_bar.close()
        print(f"{file_type} successfully fetched from the alternative gateway!")


@click.group()
def cli():
    """Modelers CLI provides tools to interact with Spectral platform and taking part in challenges."""
    pass


def get_multisig_address(address):
    """
    Fetches the MultiSig address for a given address from the API.

    :param address: The address to query.
    :return: A string with the MultiSig address or None.
    """
    url = f"{SUBSCRIPTION_LIB_URL}/getMultiSigAddress/{address}"
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'message' in data and data['message'] == 'No data found':
            return None
        else:
            return data[0]['contract_address']
    elif response.status_code == 404:
        return None


def do_ensure_wallet_exists(config_manager, reconfigure):
    # Check for wallet_private_key and wallet_address

    private_key = config_manager.get('global', 'wallet_private_key')
    address = config_manager.get('global', 'wallet_address')
    config_updated = False

    if private_key is None and address is None and not reconfigure:
        from web3 import Web3
        from eth_account import Account
        # Initialize Web3
        w3 = Web3()
        # Generate a new account
        new_account = Account.create()

        # Extract the private key and address
        private_key = new_account._private_key.hex()
        address = new_account.address
        config_manager.set('global', 'wallet_private_key', private_key)
        config_manager.set('global', 'wallet_address', address)
        click.echo(
            f"A new wallet address has been generated for this machine {address}\nTo see how to connect local wallet with your main wallet check https://docs.spectral.finance/modeler-handbook/3.-submission/step-6-phase-1-commit-to-model#link-your-local-spectral-cli-to-your-spectral-account\n")
        return -1
    elif reconfigure:
        # Show masked values and ask for new ones if the user wants to change them
        private_key_masked = mask_value(private_key)
        address_masked = mask_value(address)
        click.echo(f"\n[Your CLI Wallet address]: {address_masked}")
        new_address = click.prompt(
            "Enter new wallet address or press Enter to keep the current one\n", default="", show_default=False)

        if new_address:
            config_manager.set('global', 'wallet_address', new_address)
            config_updated = True
        click.echo(f"\n[Wallet private key]: {private_key_masked}")

        new_private_key = click.prompt(
            "Enter new wallet private key or press Enter to keep the current one\n", default="", show_default=False)
        if new_private_key:
            config_manager.set('global', 'wallet_private_key', new_private_key)
            config_updated = True

    if config_updated:
        click.echo("Config has been updated. Make sure your wallet is connected to Multisig wallet https://docs.spectral.finance/modeler-handbook/3.-submission/step-6-phase-1-commit-to-model#link-your-local-spectral-cli-to-your-spectral-account\n")
    return config_manager


def ensure_wallet_exists(reconfigure=False):
    def decorator(func):
        @wraps(func)
        def wrapper(config_manager, *args, **kwargs):
            do_ensure_wallet_exists(config_manager, reconfigure)

            return func(config_manager, *args, **kwargs)
        return wrapper
    return decorator


def mask_value(value):
    if value:
        return f"{value[:3]}*****{value[-3:]}"
    return ""


def ensure_global_config(reconfigure=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config_manager = ConfigManager(CONFIG_PATH)
            config_updated = False

            config_manager.set('global', 'multisig_wallet_address', '')

            api_key = config_manager.get('global', 'spectral_api_key')
            alchemy_api_key = config_manager.get('global', 'alchemy_api_key')
            wallet_address = config_manager.get('global', 'wallet_address')
            wallet_private_key = config_manager.get(
                'global', 'wallet_private_key')

            if not api_key or reconfigure:
                api_key_masked = mask_value(api_key)
                click.echo(f"[Spectral API key]: {api_key_masked}")

                new_api_key = click.prompt(
                    "Enter Spectral API key or press Enter to keep the current one. To check how to get your Spectral API key, please visit https://docs.spectral.finance/modeler-handbook/3.-submission/step-5-configure-spectral-cli#1.-obtain-spectral-api-key\n", default="", show_default=False)
                if new_api_key:
                    config_manager.set(
                        'global', 'spectral_api_key', new_api_key)
                    config_updated = True
                elif not reconfigure:
                    print("Spectral API key is required. Please visit https://docs.spectral.finance/modeler-handbook/3.-submission/step-5-configure-spectral-cli#1.-obtain-spectral-api-key to learn how to get it.")
                    return -1

            if not alchemy_api_key or reconfigure:
                alchemy_api_key_masked = mask_value(alchemy_api_key)
                click.echo(f"[Alchemy API key]: {alchemy_api_key_masked}")
                new_alchemy_api_key = click.prompt(
                    "Enter new Alchemy API key or press Enter to keep the current one. To learn how to get your Alchemy API Key, please visit https://docs.spectral.finance/modeler-handbook/3.-submission/step-5-configure-spectral-cli#2.-obtain-alchemy-api-key\n", default="", show_default=False)

                if new_alchemy_api_key:
                    config_manager.set(
                        'global', 'alchemy_api_key', new_alchemy_api_key)
                    config_updated = True
                elif not reconfigure:
                    print("Alchemy API key is required. Please visit https://docs.spectral.finance/modeler-handbook/3.-submission/step-5-configure-spectral-cli#2.-obtain-alchemy-api-key to learn how to get it.")
                    return -1

            if not wallet_address:
                from web3 import Web3
                from eth_account import Account
                # Initialize Web3
                w3 = Web3()
                # Generate a new account
                new_account = Account.create()

                # Extract the private key and address
                private_key = new_account._private_key.hex()
                address = new_account.address
                config_manager.set('global', 'wallet_private_key', private_key)
                config_manager.set('global', 'wallet_address', address)
                click.echo(
                    f"A new wallet address has been generated for this machine {address}\nTo see how to connect local wallet with your main wallet check https://docs.spectral.finance/modeler-handbook/3.-submission/step-6-phase-1-commit-to-model#link-your-local-spectral-cli-to-your-spectral-account\n")
                config_updated = True

            if config_manager.get('global', 'wallet_address') and not config_manager.get('global', 'multisig_wallet_address') and not reconfigure:
                multisig_wallet_address = get_multisig_address(
                    config_manager.get('global', 'wallet_address'))
                if multisig_wallet_address:
                    config_manager.set(
                        'global', 'multisig_wallet_address', multisig_wallet_address)
                else:
                    click.echo("Your wallet address is not connected to any multisig wallet. Visit https://docs.spectral.finance/modeler-handbook/3.-submission/step-6-phase-1-commit-to-model#link-your-local-spectral-cli-to-your-spectral-account to see how to connect it.\n")
                    return -1

            if config_updated:
                click.echo("Config has been updated.")
            return func(config_manager, *args, **kwargs)
        return wrapper
    return decorator


@cli.command()
def list_challenges():
    """List all available challenges."""
    print(
        f"""Available challenges:\n  Credit Scoring: {CREDIT_SCORING_CONTRACT_ADDRESS}""")


@cli.command()
def show_wallet():
    """Show the wallet address used by this CLI."""
    config_manager = ConfigManager(CONFIG_PATH)
    wallet_address = config_manager.get('global', 'wallet_address')
    if wallet_address:
        print(f"Your Spectral CLI wallet address: {wallet_address}")
    else:
        print("Spectral CLI wallet address is not set. Please run `spectral-cli configure` to set it up.")


@cli.command()
def show_configuration():
    """List current configuration."""
    config_manager = ConfigManager(CONFIG_PATH)
    config_manager.show_config()


@cli.command()
@click.argument('challenge_id')
def fetch_training_data(challenge_id):
    """Fetch training dataset."""
    # competition_abi = ABIS['Competition']
    # web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    # w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL + web3_provider_api_key))
    # contract = w3.eth.contract(address=challenge_id, abi=competition_abi)
    # ipfsTrainingDataset = contract.functions.ipfsTrainingDataset().call()
    if challenge_id == CREDIT_SCORING_CONTRACT_ADDRESS:
        ipfsTrainingDataset = CREDIT_SCORING_TRAINING_DATASET_IPFS_CID
        filename = f"{challenge_id}_training_data.parquet"
        fetch_from_ipfs(ipfsTrainingDataset, filename, "Training dataset")
    else:
        print("Invalid challenge ID. Please check the list of available challenges by running `spectral-cli list-challenges`.")


@cli.command()
@ensure_global_config(reconfigure=False)
@ensure_wallet_exists(reconfigure=False)
@click.argument('challenge_id')
def fetch_testing_data(config_manager, challenge_id):
    """Fetch testing dataset."""
    competition_abi = ABIS['Competition']
    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL + web3_provider_api_key))
    contract = w3.eth.contract(address=challenge_id, abi=competition_abi)
    modeler_contract_address = contract.functions.modelerContract().call()
    modeler_abi = ABIS['Modeler']
    modeler_contract = w3.eth.contract(
        address=modeler_contract_address, abi=modeler_abi)
    multisig_wallet_address = config_manager.get(
        'global', 'multisig_wallet_address')
    modeller_challanges = modeler_contract.functions.modelerChallenges(
        multisig_wallet_address).call()
    if not modeller_challanges:
        print("The file with your challenge data is not available yet. Please try again in a couple of minutes.")
        return -1
    ipfs_hash = modeller_challanges[0]
    if not ipfs_hash:
        print("The file with your challenge data is not available yet. Please try again in a couple of minutes.")
        return -1
    fetch_from_ipfs(
        ipfs_hash, _get_testing_dataset_filename(challenge_id), "Testing dataset")


@cli.command()
@ensure_global_config()
@ensure_wallet_exists(reconfigure=False)
@click.argument('challenge_id')
@click.argument('submission_file')
def submit_inferences(config_manager, challenge_id, submission_file):
    """Make a submission."""
    if not _validate_submission_file(challenge_id, submission_file):
        print("Submission file invalid. Please make sure you're submitting a valid dataset.")
        return -1

    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider((ALCHEMY_URL + web3_provider_api_key)))
    modeler_abi = ABIS['Modeler']
    modeler_address = MODELER_CONTRACT
    modeler_contract = w3.eth.contract(
        address=modeler_address, abi=modeler_abi)
    multisig_wallet_address = config_manager.get(
        'global', 'multisig_wallet_address')
    if modeler_contract.functions.modelerChallenges(
            multisig_wallet_address).call()[0] == '':
        print("The testing dataset for the latest model commitment is not ready yet. Please try again in a couple of minutes and make sure that your inferences are based on the latest version of your testing dataset.")
        return -1

    ipfs_api_key = config_manager.get('global', 'spectral_api_key')
    inferences_cid = upload_file_to_ipfs(submission_file, ipfs_api_key)
    if not inferences_cid:
        print("Submission failed. Please try again.")
        return -1
    print(
        f"Submitting response with CID: {inferences_cid} to challenge: {challenge_id}. This may take a moment.")
    destination_wallet_address_private_key = config_manager.get(
        'global', 'wallet_private_key')
    destination_wallet_address = config_manager.get('global', 'wallet_address')
    competition_abi = ABIS['Competition']
    validator_wallet_address = VALIDATOR_WALLET_ADDRESS
    wallet_simple_abi = ABIS['WalletSimple']

    current_block = w3.eth.block_number

    current_block_timestamp = w3.eth.get_block(current_block)['timestamp']
    competition_contract = w3.eth.contract(
        address=challenge_id, abi=competition_abi)
    multisig_contract = w3.eth.contract(
        address=multisig_wallet_address, abi=wallet_simple_abi)

    commit_function_data = {}
    contract_address = None
    commit_function_data = modeler_contract.functions.respondToChallenge(validator_wallet_address, inferences_cid).build_transaction({
        'chainId': CHAIN_ID,
        'gas': GAS,
        'gasPrice': w3.to_wei(GAS_PRICE_GWEI, 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)
    })['data']
    contract_address = modeler_address

    import time
    next_sequence_id = multisig_contract.functions.getNextSequenceId().call()
    expire_time = int(time.time()) + 3600  # Current time + 1 hour
    sequence_id = next_sequence_id
    signature = '0x'  # No signature needed for a 1-2 multisig

    txn_details = {
        'chainId': CHAIN_ID,
        'gas': GAS,
        'gasPrice': w3.to_wei(GAS_PRICE_GWEI, 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)
    }
    multisig_txn = multisig_contract.functions.sendMultiSig(
        contract_address,
        0,
        commit_function_data,
        expire_time,
        sequence_id,
        signature
    ).build_transaction(txn_details)

    private_key = destination_wallet_address_private_key
    signed_multisig_txn = w3.eth.account.sign_transaction(
        multisig_txn, private_key)

    try:
        multisig_txn_hash = w3.eth.send_raw_transaction(
            signed_multisig_txn.rawTransaction)
        multisig_txn_receipt = w3.eth.wait_for_transaction_receipt(
            multisig_txn_hash)
        tx_hash = multisig_txn_receipt['transactionHash']
        tx_hash = tx_hash.hex()
        status = multisig_txn_receipt['status']
        if status == 1:
            print('Your inferences have been recorded successfully!')
        else:
            print('Submitting your inferences failed')
        print(
            f"You can check status of that transaction under: {TX_EXPLORER_URL}/{str(tx_hash)}")
    except Exception as e:
        config_manager = ConfigManager(CONFIG_PATH)
        wallet_address = config_manager.get('global', 'wallet_address')
        if "insufficient funds for" in str(e) or "intrinsic gas too low" in str(e):
            print("Transaction failed with error: Insufficient funds. Please make sure you have enough ETH in your wallet.")
            print(f"Your CLI wallet address is: {wallet_address}")
        else:
            print("Transaction failed with error:", str(e))


@cli.command()
@ensure_global_config()
@ensure_wallet_exists(reconfigure=False)
@click.argument('model_path')
@click.argument('input_json_path')
@click.argument('challenge_id')
def commit(config_manager, model_path, input_json_path, challenge_id):
    """Commit to a machine learning model."""
    ipfs_api_key = config_manager.get('global', 'spectral_api_key')
    model_cid = dump_model(model_path, input_json_path, ipfs_api_key)
    if not model_cid:
        print("Uploading your commitment to IPFS failed. Please try again.")
        return -1
    print(
        f"Submitting model with CID: {model_cid} to challenge: {challenge_id}. This may take a moment.")
    destination_wallet_address_private_key = config_manager.get(
        'global', 'wallet_private_key')
    destination_wallet_address = config_manager.get('global', 'wallet_address')
    multisig_wallet_address = config_manager.get(
        'global', 'multisig_wallet_address')
    competition_abi = ABIS['Competition']
    modeler_abi = ABIS['Modeler']
    modeler_address = MODELER_CONTRACT
    wallet_simple_abi = ABIS['WalletSimple']

    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider((ALCHEMY_URL + web3_provider_api_key)))
    current_block = w3.eth.block_number

    current_block_timestamp = w3.eth.get_block(current_block)['timestamp']
    competition_contract = w3.eth.contract(
        address=challenge_id, abi=competition_abi)
    modeler_contract = w3.eth.contract(
        address=modeler_address, abi=modeler_abi)
    multisig_contract = w3.eth.contract(
        address=multisig_wallet_address, abi=wallet_simple_abi)

    commit_function_data = {}
    contract_address = None
    if modeler_contract.functions.modelers(multisig_wallet_address).call()[0] == '':
        commit_function_data = competition_contract.functions.signUpToCompetition(model_cid).build_transaction({
            'chainId': CHAIN_ID,
            'gas': GAS,
            'gasPrice': w3.to_wei(GAS_PRICE_GWEI, 'gwei'),
            'nonce': w3.eth.get_transaction_count(destination_wallet_address)
        })['data']
        contract_address = challenge_id
    else:
        confirmation_string = click.prompt(
            "You already committed to a model. The proceeding will replace your current commitment and will trigger the creation of a new testing dataset. Type REPLACE to proceed or anything else to cancel.", default="", show_default=False)
        if confirmation_string != "REPLACE":
            print("Process cancelled.")
            return -1
        commit_function_data = modeler_contract.functions.updateModel(model_cid).build_transaction({
            'chainId': CHAIN_ID,
            'gas': GAS,
            'gasPrice': w3.to_wei(GAS_PRICE_GWEI, 'gwei'),
            'nonce': w3.eth.get_transaction_count(destination_wallet_address)
        })['data']
        contract_address = modeler_address

    import time
    next_sequence_id = multisig_contract.functions.getNextSequenceId().call()
    expire_time = int(time.time()) + 3600  # Current time + 1 hour
    sequence_id = next_sequence_id
    signature = '0x'  # No signature needed for a 1-2 multisig

    txn_details = {
        'chainId': CHAIN_ID,
        'gas': GAS,
        'gasPrice': w3.to_wei(GAS_PRICE_GWEI, 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)
    }
    multisig_txn = multisig_contract.functions.sendMultiSig(
        contract_address,
        0,
        commit_function_data,
        expire_time,
        sequence_id,
        signature
    ).build_transaction(txn_details)

    private_key = destination_wallet_address_private_key
    signed_multisig_txn = w3.eth.account.sign_transaction(
        multisig_txn, private_key)

    try:
        multisig_txn_hash = w3.eth.send_raw_transaction(
            signed_multisig_txn.rawTransaction)
        multisig_txn_receipt = w3.eth.wait_for_transaction_receipt(
            multisig_txn_hash)
        tx_hash = multisig_txn_receipt['transactionHash']
        tx_hash = tx_hash.hex()
        status = multisig_txn_receipt['status']
        if status == 1:
            print('Your submission has been recorded successfully!')
        else:
            print('Your submission failed')
        print(
            f"You can check status of that transaction under: {TX_EXPLORER_URL}/{str(tx_hash)}")
    except Exception as e:
        config_manager = ConfigManager(CONFIG_PATH)
        wallet_address = config_manager.get('global', 'wallet_address')
        if "insufficient funds for" in str(e) or "intrinsic gas too low" in str(e):
            print("Transaction failed with error: Insufficient funds. Please make sure you have enough ETH in your wallet.")
            print(f"Your CLI wallet address is: {wallet_address}")
        else:
            print("Transaction failed with error:", str(e))


@cli.command()
@click.argument('model_path')
@click.argument('input_json_path')
def commit_local(model_path, input_json_path):
    """Create local commitment file."""
    local_commitment_path = generate_settings_file(model_path, input_json_path)
    print("Local commitment file: ", local_commitment_path)


def remove_global_config():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(CONFIG_PATH):
                os.remove(CONFIG_PATH)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@cli.command()
@ensure_global_config(reconfigure=True)
@click.option('--force', is_flag=True, help='Force reconfiguration.')
def configure(config_manager, force):
    """Configure the CLI, --force to overwrite wallet."""
    if force:
        do_ensure_wallet_exists(config_manager, reconfigure=True)
    pass


def _validate_submission_file(challenge_id, submission_file):
    click.echo("Validating submission file")
    testing_df = _get_testing_data_frame(challenge_id)
    try:
        submission_df = pd.read_parquet(submission_file)
        (testing_df_rows, _cols) = testing_df.shape
        (submission_df_rows, _cols) = submission_df.shape
        if submission_df_rows == testing_df_rows:
            return True
        return False
    except ArrowInvalid:
        return False


def _get_testing_data_frame(challenge_id):
    testing_dataset_filename = _get_testing_dataset_filename(challenge_id)
    if not os.path.exists(testing_dataset_filename):
        testing_dataset_filename = click.prompt("Please enter the absolute path to the Testing Dataset for this challenge")

    try:
        return pd.read_parquet(testing_dataset_filename)
    except FileNotFoundError:
        click.echo("Error: Testing dataset not found")
        _get_testing_data_frame(challenge_id)
    except ArrowInvalid:
        click.echo("Error: Testing dataset invalid")
        _get_testing_data_frame(challenge_id)

def _get_testing_dataset_filename(challenge_id):
    return f"{challenge_id}_testing_dataset.parquet"


if __name__ == '__main__':
    cli()
    pass
