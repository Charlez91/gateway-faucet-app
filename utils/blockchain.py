import os
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy
from dotenv import load_dotenv

load_dotenv()
#add a node and initialize it. using mainnet moralis eth node
web3 = Web3(Web3.HTTPProvider(os.environ.get('SEPOLIA_NODE')))
#web3.eth.set_gas_price_strategy(medium_gas_price_strategy)

#web3.provider.cache_allowed_requests = True
print("Web3 connection initialized: ",web3.is_connected())

pk = os.environ.get('PRIVATE_KEY')

def get_account():
    '''Instantiate an Account object from private key'''
    account = web3.eth.account.from_key(pk)
    return account

def get_gas_fee():
    '''Get current gas fee for the network in wei'''
    #gas_fee = web3.eth.generate_gas_price()
    gas_fee = web3.eth.gas_price
    return gas_fee

def check_address(address:str):
    '''
    Check to know if `address` is a valid checksum ETH address
    '''
    is_address = web3.is_address(address)
    return is_address

def build_transaction(receiving_address:str, amount:float=0.0001, account= get_account()):
    ''' Build a new txn '''
    value = web3.to_wei(amount,'ether')
    fee = get_gas_fee()
    txn = {
        'from': account.address,
        'to': web3.to_checksum_address(receiving_address),
        'value': value,
        'nonce': web3.eth.get_transaction_count(account.address),
        #'gas':  get_gas_fee() if get_gas_fee()<value else web3.to_wei(0.00001, 'ether'),
        "gas":60000,
        'maxFeePerGas': int(fee*0.8),
        'maxPriorityFeePerGas': int(fee*0.5),
        'chainId':11155111
    }
    print(txn)
    return txn

def sign_and_send_txn(txn:dict):    
    ''' Sign tx with a private key and Send the signed transaction '''
    signed = web3.eth.account.sign_transaction(txn, pk)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(signed, tx_hash)
    return tx_hash

def get_txn(tx_hash):
    tx = web3.eth.get_transaction(tx_hash)
    assert tx["from"] == get_account().address
    return tx

def get_txn_receipt(tx_hash):
    tx = web3.eth.get_transaction_receipt(tx_hash)
    assert tx["from"] == get_account().address
    return tx.status, tx