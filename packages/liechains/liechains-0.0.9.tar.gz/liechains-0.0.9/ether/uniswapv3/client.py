import time
from web3 import Web3
from ether.client import Web3Client
from ether.utils import sort_addrs
from .chains import chains
from eth_abi import encode
from eth_abi.packed import encode_packed
from web3.middleware import construct_sign_and_send_raw_middleware
from . import abis


class Meta(type):
    def __getitem__(self, arg):
        return UniswapV3(Web3Client[arg], chains[arg])


class UniswapV3(metaclass=Meta):
    def __init__(self, web3_client: Web3Client, conf: dict) -> None:
        self.conf = conf
        self.client = web3_client
        self.swap_router = web3_client.eth.contract(
            conf["router"], abi=abis.swap_router
        )

    def with_account(self, private_key: str):
        self.acc = self.client.eth.account.from_key(private_key)
        self.client.middleware_onion.add(construct_sign_and_send_raw_middleware(self.acc))
        self.client.eth.default_account = self.acc.address
        return self

    def get_pool_addr(self, token_a: str, token_b: str, fee: int):
        token0, token1 = sort_addrs(token_a, token_b)

        token0 = Web3.to_bytes(hexstr=token0)
        token1 = Web3.to_bytes(hexstr=token1)
        head = bytes.fromhex("ff") + Web3.to_bytes(hexstr=self.conf["factory"])
        with_addrs = head + Web3.keccak(
            encode(["address", "address", "uint24"], [token0, token1, fee])
        )

        with_initcode = Web3.keccak(
            with_addrs + Web3.to_bytes(hexstr=self.conf["init_code"])
        )
        i = with_initcode[12:]
        return Web3.to_checksum_address(i)

    def build_exactInputSingle(
        self,
        tokenin,
        tokenout,
        fee,
        receipient: str,
        amount_in,
        min_amount_out,
        deadline=None,
        sqrtPriceLimitX96=0,
    ):
        """
        根据参数组装出交易的input
        """
        if not deadline:
            deadline = int(time.time() + 60)
        return self.swap_router.functions.exactInputSingle(
            (
                tokenin,
                tokenout,
                fee,
                receipient,
                deadline,
                amount_in,
                min_amount_out,
                sqrtPriceLimitX96,
            )
        )
