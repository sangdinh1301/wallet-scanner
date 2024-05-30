import json
from dotenv import dotenv_values
from web3 import Web3
from mnemonic import Mnemonic
from eth_account import Account


def enable_hd_wallet_features():
    Account.enable_unaudited_hdwallet_features()


def generate_random_mnemonic():
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)


def get_account_from_mnemonic(mnemonic_phrase):
    mnemo = Mnemonic("english")
    if not mnemo.check(mnemonic_phrase):
        raise ValueError("Invalid mnemonic phrase")
    return Account.from_mnemonic(mnemonic_phrase)


def get_balance(web3, address):
    balance_wei = web3.eth.get_balance(address)
    return web3.from_wei(balance_wei, 'ether')


def write_to_txt(new_line, filename):
    with open(filename, 'a') as file:
        file.write(new_line + '\n')


def configure_rpc_nodes(env_vars):
    return {
        'eth': f"https://mainnet.infura.io/v3/{env_vars['INFURA_API_KEY']}",
        'op': f"https://optimism-mainnet.infura.io/v3/{env_vars['INFURA_API_KEY']}",
        'bsc': "https://bsc-dataseed.binance.org/",
        'polygon': 'https://polygon-rpc.com',
        'base': 'https://base.llamarpc.com',
        'arbitrum': 'https://arb1.arbitrum.io/rpc',
    }


def main():
    env_vars = dotenv_values()

    enable_hd_wallet_features()

    rpc_nodes = configure_rpc_nodes(env_vars)

    blockchain_clients = {}
    for blockchain, url in rpc_nodes.items():
        blockchain_clients[blockchain] = Web3(Web3.HTTPProvider(url))

    while True:
        try:
            mnemonic_phrase = generate_random_mnemonic()

            account = get_account_from_mnemonic(mnemonic_phrase)
            address = account.address

            balances = {}
            for blockchain, web3 in blockchain_clients.items():
                balances[blockchain] = get_balance(web3, address)

            data = (
                f'Address: {address}\n'
                f'Mnemonic phrase: {mnemonic_phrase}\n'
            )

            for blockchain, balance in balances.items():
                data += f'Balance on {blockchain.upper()}: {balance}\n'

            print(data)

            has_non_empty_value = any(value for value in balances.values())

            if not has_non_empty_value:
                continue

            write_to_txt(data, 'balances.txt')
        except Exception as error:
            print(error)
            continue


if __name__ == "__main__":
    main()
