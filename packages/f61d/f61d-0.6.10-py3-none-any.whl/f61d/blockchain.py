from Crypto.Hash import keccak
from web3 import Web3

def inputBytes(func):

    def wrapper(cont):
        if isinstance(cont,str):
            cont = cont.encode()
        assert isinstance(cont,bytes)
        return func(cont)

    return wrapper

@inputBytes
def keccak_256(cont):
    hash_obj = keccak.new(digest_bits=256)
    hash_obj.update(cont)
    return hash_obj.hexdigest()

SHA3 = keccak_256
sha3 = SHA3

@inputBytes
def funcSign(cont):
    keccak256Hash = keccak_256(cont)
    return '0x' + keccak256Hash[:8]


def SepoliaWeb3():
    # Sepolia
    sepolia_rpc = 'https://ethereum-sepolia.publicnode.com'
    SepoliaWeb3 = Web3(Web3.HTTPProvider(sepolia_rpc))
    return SepoliaWeb3

def GoerliWeb3():
    # Goerli
    goerli_rpc = 'https://ethereum-goerli.publicnode.com'
    GoerliWeb3 = Web3(Web3.HTTPProvider(goerli_rpc))
    return GoerliWeb3

if __name__ == '__main__':
    print(funcSign('balanceOf(address)'))
