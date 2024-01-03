from Crypto.Hash import keccak
from web3 import Web3, Account
from urllib.parse import urlparse
import json

def inputBytes(func):
    
    def wrapper(cont):
        if isinstance(cont,str):
            cont = cont.encode()
        assert isinstance(cont,bytes)
        return func(cont)
    
    return wrapper

@inputBytes
def keccak_256(cont: bytes, bits=256) -> str:
    hash_obj = keccak.new(data=cont, digest_bits=bits)
    return hash_obj.hexdigest()

sha3 = SHA3 = keccak_256

@inputBytes
def funcSign(cont: bytes) -> str:
    keccak256Hash = keccak_256(cont)
    return '0x' + keccak256Hash[:8]

web3_ = None
pub_ = None
priv_ = None

def setArgs(pub=None, priv=None):
    global pub_, priv_
    pub_ = pub
    priv_ = priv
    print("Success set public and private key")


def W3(chain) -> Web3:
    global web3_
    if isinstance(chain, str) and urlparse(chain).scheme:  # RPC
        web3_ = Web3(Web3.HTTPProvider(chain))
        assert web3_.is_connected(), "Unable to connect to chain by provided RPC"
    elif isinstance(chain, int): # ChainId
        if chain == 5: # Goerli
            web3_ = GoerliWeb3()
        elif chain == 11155111: # Sepolia
            web3_ = SepoliaWeb3()
        else:
            raise ValueError("Unknown Chain ID, please update")
    elif isinstance(chain, str): # Chain name
        if chain.lower() == 'Goerli'.lower() or 'Goerli'.lower().startswith(chain.lower()):
            web3_ = GoerliWeb3()
        elif chain.lower() == 'Sepolia'.lower() or 'Sepolia'.lower().startswith(chain.lower()):
            web3_ = SepoliaWeb3()
        else:
            raise ValueError("Unknown Chain Name, please update")
    else:
        raise ValueError("Unsupported input type. Please input RPC/chainId/chainName")
    return web3_

def SepoliaWeb3(rpc='https://ethereum-sepolia.publicnode.com'):
    # Sepolia
    sepolia_rpc = rpc
    SepoliaWeb3 = Web3(Web3.HTTPProvider(sepolia_rpc))
    SepoliaWeb3.__setattr__('name','sepolia')
    assert SepoliaWeb3.is_connected(), "Unable to connect to chain"
    return SepoliaWeb3

def GoerliWeb3(rpc='https://ethereum-goerli.publicnode.com'):
    # Goerli
    goerli_rpc = rpc
    GoerliWeb3 = Web3(Web3.HTTPProvider(goerli_rpc))
    GoerliWeb3.__setattr__('name', 'goerli')
    assert GoerliWeb3.is_connected(), "Unable to connect to chain"
    return GoerliWeb3


def deployBytecode(bytecode: str, web3=None, pub=None, priv=None, gas=3000000, abi=None):
    """
    Deploy contract with bytecode

    Args:
        bytecode (hex str): Bytecode of contract.
        web3 (Web3): The Web3 instance connected to the blockchain.
        pub (str): The public key of the sender's account.
        priv (str): The private key of the sender's account.
        gas (int, optional): The gas limit for the transaction (default: 3000000).
        abi (dict, optional): ABI of contract

    Returns:
        contract: The deployed contract.
                  contract.address for address in blockchain
    """
    if abi is not None:
        cont_Args = {'abi':kwargs['abi']}

    web3 = web3 if web3 is not None else web3_
    pub = pub if pub is not None else pub_
    priv = pub if priv is not None else priv_

    if pub is None and priv is None:
        raise ValueError("Give me pub and priv by function args or setArgs(pub, priv)")

    if any(i is None for i in [pub, priv, web3]):
        raise ValueError("Missing args.")

    contract = web3.eth.contract(bytecode=bytecode, **cont_Args)
    deploy_tx = contract.constructor(con_addr).build_transaction({
        'from': pub,
        'gas': gas,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(pub)
    })
    # Sign
    signed_deploy_transaction = Account.sign_transaction(deploy_tx, private_key=priv)
    transaction_hash = web3.eth.send_raw_transaction(signed_deploy_transaction.rawTransaction)
    print(f"{transaction_hash = }")
    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    print("transaction_receipt: ")
    for i in transaction_receipt:
        print(f"{i} : {transaction_receipt[i].__repr__()}")
    contract_address = transaction_receipt['contractAddress']
    print(f'{contract_address = }')
    return contract


def sendTx(func, web3=None, pub=None, priv=None, gas=3000000, **kwargs):
    """
    Send a transaction to the blockchain.

    Args:
        func (ContractFunction): The contract function to call.
                                 eg. contract.functions.myFunc(1,2)
        web3 (Web3): The Web3 instance connected to the blockchain.
        pub (str): The public key of the sender's account.
        priv (str): The private key of the sender's account.
        gas (int, optional): The gas limit for the transaction (default: 3000000).
        **kwargs: Additional keyword arguments for the contract function.
                  eg. value=10**18

    Returns:
        bytes: The transaction hash.

    Raises:
        ValueError: Missing args or args not set
    """
    web3 = web3 if web3 is not None else web3_
    pub = pub if pub is not None else pub_
    priv = pub if priv is not None else priv_

    if pub is None and priv is None:
        raise ValueError("Give me pub and priv by function args or setArgs(pub, priv)")

    if any(i is None for i in [pub, priv, web3]):
        raise ValueError("Missing args.")

    tx = func.build_transaction({ # 函数调用交易这里不需要data参数
        'from': pub,
        'gas': gas,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(pub),
        **kwargs # maybe "value" or "to"
    })
    signed_transaction = Account.sign_transaction(tx, private_key=priv)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"{transaction_hash = }")
    if hasattr(web3,'name'):
        print(f"https://{web3.name}.etherscan.io/tx/{transaction_hash.hex()}")

    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    print("transaction_receipt: ")
    for i in transaction_receipt:
        print(f"{i} : {transaction_receipt[i].__repr__()}")
    return transaction_hash


if __name__ == '__main__':
    print(funcSign('balanceOf(address)'))
