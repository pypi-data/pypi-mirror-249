from eth_account import Account


class Wallet:
    def __init__(self, mnemonic) -> None:
        self.mnemonic = mnemonic
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return [Account.from_mnemonic(self.mnemonic,account_path=f"m/44'/60'/0'/0/{i}") for i in range(index.start,index.stop)]
        else:
            return Account.from_mnemonic(self.mnemonic,account_path=f"m/44'/60'/0'/0/{index}")
