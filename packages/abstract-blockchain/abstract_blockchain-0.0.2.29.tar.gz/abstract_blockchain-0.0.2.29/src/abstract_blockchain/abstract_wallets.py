import os
import secrets
from abstract_utilities.path_utils import makeAllDirs
from abstract_utilities import safe_dump_to_file,create_and_read_json
from eth_account import Account
script_path = os.path.abspath(__file__)

directory_path = os.path.dirname(script_path)
class AbstractWallets:
    def __init__(self,chain ='kovan-optimism'):
        self.wallet_path = makeAllDirs(os.path.join(directory_path,'wallets', 'Wallets.json'))
        self.wallets=create_and_read_json(file_path=self.wallet_path,data=[])
    def add_wall(self,name=""):
        priv = secrets.token_hex(32)
        add = Account.from_key(priv).address
        wallet_js={"add":add,"priv":priv,"name":name}
        self.wallets.append(wallet_js)
        safe_dump_to_file(file_path=self.wallet_path,data=self.wallets)
        return wallet_js
