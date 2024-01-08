from abstract_security import get_env_value
from abstract_utilities import make_list,safe_json_loads,safe_dump_to_file,safe_read_from_json,create_and_read_json
from abstract_utilities.list_utils import remove_from_list
from abstract_utilities.path_utils import makeAllDirs
from .rpc_functions import *
import requests
import json
import os
from .abstract_rpcs import RPCBridge
class w3Manager:
    def __init__(self):
        self.w3_management = {}
        self.default_rpc_js = get_default_rpc(Network_Name="Ethereum")  # Assuming get_default_rpc is defined elsewhere
        self.default_rpc_mgr = RPCBridge(rpc_js=self.default_rpc_js)  # Assuming get_new_rpc_bridge is defined elsewhere
        self.default_w3 = self.default_rpc_mgr.w3

    def add_to_list(self, address, w3=None, rpc=None,rpc_js=None):
        normalized_address = get_normalized_address(address)
        if not w3 and rpc:
            w3 = self.create_w3(address, rpc=rpc)
        self.w3_management[normalized_address] = {'w3': w3 or self.default_w3, 'rpc': rpc or self.default_rpc_mgr.rpc,'rpc_js':rpc_js or self.default_rpc_js}
    def retrieve_w3(self, address,rpc=None,rpc_js=None):
        rpc_dict = {"rpc":rpc,"rpc_js":rpc_js}
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.w3_management:
            self.add_to_list(address)
        values,keys=[],[]
        for key,item in rpc_dict.items():
            if item:
                values.append(item)
                keys.append(key)
        if values:
            self.ammend_to_list( address, keys, values)
        return self.w3_management[normalized_address]['w3']
    def retrieve_rpc(self, address):
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.w3_management:
            self.add_to_list(address)
        return self.w3_management[normalized_address]['rpc']
    def retrieve_rpc_js(self, address):
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.w3_management:
            self.add_to_list(address)
        return self.w3_management[normalized_address]['rpc_js']
    def create_w3(self, address, rpc=None):
        if isinstance(rpc, dict):
            self.ammend_to_list(get_normalized_address(address), ['rpc_js'], [rpc])
            rpc = rpc.get('user_settings', rpc.get('rpc', self.default_rpc_mgr.rpc))
            if rpc and 'rpc' in rpc and isinstance(rpc,dict):
                rpc=rpc.get('rpc')
            
        elif rpc is None:
            rpc = self.default_rpc_mgr.rpc

        try:
            new_w3 = Web3(Web3.HTTPProvider(rpc))
            self.ammend_to_list(address, ['w3', 'rpc'], [new_w3, rpc])
            return new_w3
        except Exception as e:
            print(f"Error creating w3 from rpc {rpc}: {e}")
            self.add_to_list(address)  # Fallback to default w3
            return self.default_w3

    def ammend_to_list(self, address, keys, values):
        normalized_address = get_normalized_address(address)
        if normalized_address not in self.w3_management:
            self.add_to_list(address)
        for i, key in enumerate(keys):
            self.w3_management[normalized_address][key] = values[i]
w3_mgr = w3Manager()            
apiCallDesc = {'multiTopic': {'description': 'searchtopics', 'example': 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=12878196&toBlock=12879196&topic0=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef&topic0_1_opr=and&topic1=0x0000000000000000000000000000000000000000000000000000000000000000&page=1&offset=1000&apikey=YourApiKeyToken', 'pieces': {'module': ['logs'], 'action': ['getLogs'], 'fromBlock': [], 'toBlock': [], 'topic0': [], 'topic0_1_opr': ['and'], 'topic1': [], 'page': [], 'offset': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['fromBlock', 'toBlock', 'topic0', 'topic1', 'page', 'offset'], 'title': 'multitopic'},
               'topicSearch': {'description': 'getbytopic', 'title': 'topicsearch', 'pieces': {'module': ['logs'], 'action': ['getLogs'], 'fromBlock': [], 'toBlock': ['latest'], 'address': [], 'topic0': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['fromBlock', 'address', 'topic0'], 'example': 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0x33990122638b9132ca29c723bdf037f1a891a70c&topic0=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545&apikey=YourApiKeyToken'},
               'EthBalForSnglAddrs': {'description': 'GetEtherBalanceforasingleAddress\nexample:\n/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest&apikey=YourApiKeyToken', 'title': 'GetEtherBalanceforasingleAddress', 'pieces': {'module': ['account'], 'action': ['balance'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest&apikey=YourApiKeyToken'}, 'HistEthBalForSnglAddrsByBlkno': {'description': 'GetHistoricalEtherBalanceforasingleAddressByBlockNo\nexample:\n/api?module=account&action=balancehistory&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&blockno=8000000&apikey=YourApiKeyToken', 'title': 'GetHistoricalEtherBalanceforasingleAddressByBlockNo', 'pieces': {'module': ['account'], 'action': ['balancehistory'], 'address': [], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'blockno'], 'example': '/api?module=account&action=balancehistory&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&blockno=8000000&apikey=YourApiKeyToken'}, 'EthBalForMulAddrsesInSnglCall': {'description': 'GetEtherBalanceformultipleAddressesinasinglecall\nexample:\n/api?module=account&action=balancemulti&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a,0x63a9975ba31b0b9626b34300f7f627147df1f526,0x198ef1ec325a96cc354c7266a038be8b5c558f67&tag=latest&apikey=YourApiKeyToken', 'title': 'GetEtherBalanceformultipleAddressesinasinglecall', 'pieces': {'module': ['account'], 'action': ['balancemulti'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=account&action=balancemulti&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a,0x63a9975ba31b0b9626b34300f7f627147df1f526,0x198ef1ec325a96cc354c7266a038be8b5c558f67&tag=latest&apikey=YourApiKeyToken'}, 'LstOfNrmlTxnsByAddrs': {'description': 'GetalistofNormalTransactionsByAddress\nexample:\n/api?module=account&action=txlist&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken', 'title': 'GetalistofNormalTransactionsByAddress', 'pieces': {'module': ['account'], 'action': ['txlist'], 'address': [], 'startblock': [], 'endblock': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'startblock', 'endblock'], 'example': '/api?module=account&action=txlist&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken'}, 'LstOfIntlTxnsByAddrs': {'description': 'GetalistofInternalTransactionsbyAddress\nexample:\n/api?module=account&action=txlistinternal&address=0x2c1ba59d6f58433fb1eaee7d20b26ed83bda51a3&startblock=0&endblock=2702578&sort=asc&apikey=YourApiKeyToken', 'title': 'GetalistofInternalTransactionsbyAddress', 'pieces': {'module': ['account'], 'action': ['txlistinternal'], 'address': [], 'startblock': [], 'endblock': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'startblock', 'endblock'], 'example': '/api?module=account&action=txlistinternal&address=0x2c1ba59d6f58433fb1eaee7d20b26ed83bda51a3&startblock=0&endblock=2702578&sort=asc&apikey=YourApiKeyToken'}, 'IntlTxnsByTxnHash': {'description': 'GetInternalTransactionsbyTransactionHash\nexample:\n/api?module=account&action=txlistinternal&txhash=0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170&apikey=YourApiKeyToken', 'title': 'GetInternalTransactionsbyTransactionHash', 'pieces': {'module': ['account'], 'action': ['txlistinternal'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=account&action=txlistinternal&txhash=0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170&apikey=YourApiKeyToken'}, 'IntlTxnsByBlkRng': {'description': 'GetInternalTransactionsbyBlockRange\nexample:\n/api?module=account&action=txlistinternal&startblock=0&endblock=2702578&page=1&offset=10&sort=asc&apikey=YourApiKeyToken', 'title': 'GetInternalTransactionsbyBlockRange', 'pieces': {'module': ['account'], 'action': ['txlistinternal'], 'startblock': [], 'endblock': [], 'page': [], 'offset': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startblock', 'endblock', 'page', 'offset'], 'example': '/api?module=account&action=txlistinternal&startblock=0&endblock=2702578&page=1&offset=10&sort=asc&apikey=YourApiKeyToken'}, 'LstOfErc20-TknTransferEventsByAddrs': {'description': 'GetalistofERC20-TokenTransferEventsbyAddress\nexample:\n/api?module=account&action=tokentx&address=0x4e83362442b8d1bec281594cea3050c8eb01311c&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken', 'title': 'GetalistofERC20-TokenTransferEventsbyAddress', 'pieces': {'module': ['account'], 'action': ['tokentx'], 'address': [], 'startblock': [], 'endblock': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'startblock', 'endblock'], 'example': '/api?module=account&action=tokentx&address=0x4e83362442b8d1bec281594cea3050c8eb01311c&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken'}, 'LstOfErc721-TknTransferEventsByAddrs': {'description': 'GetalistofERC721-TokenTransferEventsbyAddress\nexample:\n/api?module=account&action=tokennfttx&address=0x6975be450864c02b4613023c2152ee0743572325&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken', 'title': 'GetalistofERC721-TokenTransferEventsbyAddress', 'pieces': {'module': ['account'], 'action': ['tokennfttx'], 'address': [], 'startblock': [], 'endblock': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'startblock', 'endblock'], 'example': '/api?module=account&action=tokennfttx&address=0x6975be450864c02b4613023c2152ee0743572325&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken'}, 'LstOfBlksMinedByAddrs': {'description': 'GetlistofBlocksMinedbyAddress\nexample:\n/api?module=account&action=getminedblocks&address=0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b&blocktype=blocks&apikey=YourApiKeyToken', 'title': 'GetlistofBlocksMinedbyAddress', 'pieces': {'module': ['account'], 'action': ['getminedblocks'], 'address': [], 'blocktype': ['blocks'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=account&action=getminedblocks&address=0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b&blocktype=blocks&apikey=YourApiKeyToken'}, 'GetContractABIforVerifiedContractSourceCodes': {'description': 'GetContractABIforVerifiedContractSourceCodes\nexample:\n/api?module=contract&action=getabi&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken', 'title': 'GetContractABIforVerifiedContractSourceCodes', 'pieces': {'module': ['contract'], 'action': ['getabi'], 'address': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=contract&action=getabi&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken'}, 'CntrctSrcCodeForVerifiedCntrctSrcCodes': {'description': 'GetContractSourceCodeforVerifiedContractSourceCodes\nexample:\n/api?module=contract&action=getsourcecode&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken', 'title': 'GetContractSourceCodeforVerifiedContractSourceCodes', 'pieces': {'module': ['contract'], 'action': ['getsourcecode'], 'address': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=contract&action=getsourcecode&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken'}, 'HeckCntrctExecutionStatus': {'description': 'CheckContractExecutionStatus(iftherewasanerrorduringcontractexecution)\nexample:\n/api?module=transaction&action=getstatus&txhash=0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a&apikey=YourApiKeyToken', 'title': 'CheckContractExecutionStatus(iftherewasanerrorduringcontractexecution)', 'pieces': {'module': ['transaction'], 'action': ['getstatus'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=transaction&action=getstatus&txhash=0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a&apikey=YourApiKeyToken'}, 'HeckTxnReceiptStatus': {'description': 'CheckTransactionReceiptStatus(OnlyapplicableforPostByzantiumforktransactions)\nexample:\n/api?module=transaction&action=gettxreceiptstatus&txhash=0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76&apikey=YourApiKeyToken', 'title': 'CheckTransactionReceiptStatus(OnlyapplicableforPostByzantiumforktransactions)', 'pieces': {'module': ['transaction'], 'action': ['gettxreceiptstatus'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=transaction&action=gettxreceiptstatus&txhash=0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76&apikey=YourApiKeyToken'},
 'Blk&UncleRewByBlkno': {'description': 'GetBlockAndUncleRewardsbyBlockNo\nexample:\n/api?module=block&action=getblockreward&blockno=2165403&apikey=YourApiKeyToken', 'title': 'GetBlockAndUncleRewardsbyBlockNo', 'pieces': {'module': ['block'], 'action': ['getblockreward'], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['blockno'], 'example': '/api?module=block&action=getblockreward&blockno=2165403&apikey=YourApiKeyToken'}, 'EstBlkCountdownTimeByBlkno': {'description': 'GetEstimatedBlockCountdownTimebyBlockNo\nexample:\n/api?module=block&action=getblockcountdown&blockno=9100000&apikey=YourApiKeyToken', 'title': 'GetEstimatedBlockCountdownTimebyBlockNo', 'pieces': {'module': ['block'], 'action': ['getblockcountdown'], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['blockno'], 'example': '/api?module=block&action=getblockcountdown&blockno=9100000&apikey=YourApiKeyToken'}, 'BlkNumByTimestamp': {'description': 'GetBlockNumberbyTimestamp\nexample:\n/api?module=block&action=getblocknobytime&timestamp=1578638524&closest=before&apikey=YourApiKeyToken', 'title': 'GetBlockNumberbyTimestamp', 'pieces': {'module': ['block'], 'action': ['getblocknobytime'], 'timestamp': [], 'closest': ['before'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['timestamp'], 'example': '/api?module=block&action=getblocknobytime&timestamp=1578638524&closest=before&apikey=YourApiKeyToken'}, 'EventLogsFromBlkNum': {'description': 'GetEventLogsfromblocknumber379224tolatestBlock,wherelogaddress=0x33990122638b9132ca29c723bdf037f1a891a70candtopic[0]=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545\nexample:\n/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0x33990122638b9132ca29c723bdf037f1a891a70c&topic0=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545&apikey=YourApiKeyToken', 'title': 'GetEventLogsfromblocknumber379224tolatestBlock,wherelogaddress=0x33990122638b9132ca29c723bdf037f1a891a70candtopic[0]=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545', 'pieces': {'module': ['logs'], 'action': ['getLogs'], 'fromBlock': [], 'toBlock': ['latest'], 'address': [], 'topic0': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['fromBlock', 'address', 'topic0'], 'example': '/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0x33990122638b9132ca29c723bdf037f1a891a70c&topic0=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545&apikey=YourApiKeyToken'}, 'Th_blknum': {'description': 'eth_blockNumber\nexample:\n/api?module=proxy&action=eth_blockNumber&apikey=YourApiKeyToken', 'title': 'eth_blockNumber', 'pieces': {'module': ['proxy'], 'action': ['eth_blockNumber'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=proxy&action=eth_blockNumber&apikey=YourApiKeyToken'}, 'Th_getblkbynum': {'description': 'eth_getBlockByNumber\nexample:\n/api?module=proxy&action=eth_getBlockByNumber&tag=0x10d4f&boolean=true&apikey=YourApiKeyToken', 'title': 'eth_getBlockByNumber', 'pieces': {'module': ['proxy'], 'action': ['eth_getBlockByNumber'], 'tag': [], 'boolean': ['true'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['tag'], 'example': '/api?module=proxy&action=eth_getBlockByNumber&tag=0x10d4f&boolean=true&apikey=YourApiKeyToken'}, 'Th_getunclebyblknum&index': {'description': 'eth_getUncleByBlockNumberAndIndex\nexample:\n/api?module=proxy&action=eth_getUncleByBlockNumberAndIndex&tag=0x210A9B&index=0x0&apikey=YourApiKeyToken', 'title': 'eth_getUncleByBlockNumberAndIndex', 'pieces': {'module': ['proxy'], 'action': ['eth_getUncleByBlockNumberAndIndex'], 'tag': [], 'index': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['tag', 'index'], 'example': '/api?module=proxy&action=eth_getUncleByBlockNumberAndIndex&tag=0x210A9B&index=0x0&apikey=YourApiKeyToken'}, 'Th_getblktxncountbynum': {'description': 'eth_getBlockTransactionCountByNumber\nexample:\n/api?module=proxy&action=eth_getBlockTransactionCountByNumber&tag=0x10FB78&apikey=YourApiKeyToken', 'title': 'eth_getBlockTransactionCountByNumber', 'pieces': {'module': ['proxy'], 'action': ['eth_getBlockTransactionCountByNumber'], 'tag': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['tag'], 'example': '/api?module=proxy&action=eth_getBlockTransactionCountByNumber&tag=0x10FB78&apikey=YourApiKeyToken'}, 'Th_gettxnbyhash': {'description': 'eth_getTransactionByHash\nexample:\n/api?module=proxy&action=eth_getTransactionByHash&txhash=0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1&apikey=YourApiKeyToken', 'title': 'eth_getTransactionByHash', 'pieces': {'module': ['proxy'], 'action': ['eth_getTransactionByHash'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=proxy&action=eth_getTransactionByHash&txhash=0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1&apikey=YourApiKeyToken'}, 'Th_gettxnbyblknum&index': {'description': 'eth_getTransactionByBlockNumberAndIndex\nexample:\n/api?module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag=0x10d4f&index=0x0&apikey=YourApiKeyToken', 'title': 'eth_getTransactionByBlockNumberAndIndex', 'pieces': {'module': ['proxy'], 'action': ['eth_getTransactionByBlockNumberAndIndex'], 'tag': [], 'index': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['tag', 'index'], 'example': '/api?module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag=0x10d4f&index=0x0&apikey=YourApiKeyToken'}, 'Th_gettxncount': {'description': 'eth_getTransactionCount\nexample:\n/api?module=proxy&action=eth_getTransactionCount&address=0x2910543af39aba0cd09dbb2d50200b3e800a63d2&tag=latest&apikey=YourApiKeyToken', 'title': 'eth_getTransactionCount', 'pieces': {'module': ['proxy'], 'action': ['eth_getTransactionCount'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=proxy&action=eth_getTransactionCount&address=0x2910543af39aba0cd09dbb2d50200b3e800a63d2&tag=latest&apikey=YourApiKeyToken'}, 'Th_sendrawtxn': {'description': 'eth_sendRawTransaction\nexample:\n/api?module=proxy&action=eth_sendRawTransaction&hex=0xf904808000831cfde080&apikey=YourApiKeyToken', 'title': 'eth_sendRawTransaction', 'pieces': {'module': ['proxy'], 'action': ['eth_sendRawTransaction'], 'hex': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['hex'], 'example': '/api?module=proxy&action=eth_sendRawTransaction&hex=0xf904808000831cfde080&apikey=YourApiKeyToken'}, 'Th_gettxnreceipt': {'description': 'eth_getTransactionReceipt\nexample:\n/api?module=proxy&action=eth_getTransactionReceipt&txhash=0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1&apikey=YourApiKeyToken', 'title': 'eth_getTransactionReceipt', 'pieces': {'module': ['proxy'], 'action': ['eth_getTransactionReceipt'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=proxy&action=eth_getTransactionReceipt&txhash=0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1&apikey=YourApiKeyToken'}, 'Th_call': {'description': 'eth_call\nexample:\n/api?module=proxy&action=eth_call&to=0xAEEF46DB4855E25702F8237E8f403FddcaF931C0&data=0x70a08231000000000000000000000000e16359506c028e51f16be38986ec5746251e9724&tag=latest&apikey=YourApiKeyToken', 'title': 'eth_call', 'pieces': {'module': ['proxy'], 'action': ['eth_call'], 'to': [], 'data': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['to', 'data'], 'example': '/api?module=proxy&action=eth_call&to=0xAEEF46DB4855E25702F8237E8f403FddcaF931C0&data=0x70a08231000000000000000000000000e16359506c028e51f16be38986ec5746251e9724&tag=latest&apikey=YourApiKeyToken'}, 'Th_getcode': {'description': 'eth_getCode\nexample:\n/api?module=proxy&action=eth_getCode&address=0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c&tag=latest&apikey=YourApiKeyToken', 'title': 'eth_getCode', 'pieces': {'module': ['proxy'], 'action': ['eth_getCode'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=proxy&action=eth_getCode&address=0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c&tag=latest&apikey=YourApiKeyToken'}, 'Th_getstorageat': {'description': 'eth_getStorageAt\nexample:\n/api?module=proxy&action=eth_getStorageAt&address=0x6e03d9cce9d60f3e9f2597e13cd4c54c55330cfd&position=0x0&tag=latest&apikey=YourApiKeyToken', 'title': 'eth_getStorageAt', 'pieces': {'module': ['proxy'], 'action': ['eth_getStorageAt'], 'address': [], 'position': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'position'], 'example': '/api?module=proxy&action=eth_getStorageAt&address=0x6e03d9cce9d60f3e9f2597e13cd4c54c55330cfd&position=0x0&tag=latest&apikey=YourApiKeyToken'}, 'Th_gasprice': {'description': 'eth_gasPrice\nexample:\n/api?module=proxy&action=eth_gasPrice&apikey=YourApiKeyToken', 'title': 'eth_gasPrice', 'pieces': {'module': ['proxy'], 'action': ['eth_gasPrice'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=proxy&action=eth_gasPrice&apikey=YourApiKeyToken'}, 'Th_estimategas': {'description': 'eth_estimateGas\nexample:\n/api?module=proxy&action=eth_estimateGas&to=0xf0160428a8552ac9bb7e050d90eeade4ddd52843&value=0xff22&gasPrice=0x051da038cc&gas=0xffffff&apikey=YourApiKeyToken', 'title': 'eth_estimateGas', 'pieces': {'module': ['proxy'], 'action': ['eth_estimateGas'], 'to': [], 'value': [], 'gasPrice': [], 'gas': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['to', 'value', 'gasPrice', 'gas'], 'example': '/api?module=proxy&action=eth_estimateGas&to=0xf0160428a8552ac9bb7e050d90eeade4ddd52843&value=0xff22&gasPrice=0x051da038cc&gas=0xffffff&apikey=YourApiKeyToken'}, 'Erc20-tknTotalsupplyByCntrctaddrs': {'description': 'GetERC20-TokenTotalSupplybyContractAddress\nexample:\n/api?module=stats&action=tokensupply&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&apikey=YourApiKeyToken', 'title': 'GetERC20-TokenTotalSupplybyContractAddress', 'pieces': {'module':
 ['stats'], 'action': ['tokensupply'], 'contractaddress': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress'], 'example': '/api?module=stats&action=tokensupply&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&apikey=YourApiKeyToken'}, 'HistErc20-tknTotalsupplyByCntrctaddrs&Blkno': {'description': 'GetHistoricalERC20-TokenTotalSupplybyContractAddress&BlockNo\nexample:\n/api?module=stats&action=tokensupplyhistory&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&blockno=8000000&apikey=YourApiKeyToken', 'title': 'GetHistoricalERC20-TokenTotalSupplybyContractAddress&BlockNo', 'pieces': {'module': ['stats'], 'action': ['tokensupplyhistory'], 'contractaddress': [], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress', 'blockno'], 'example': '/api?module=stats&action=tokensupplyhistory&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&blockno=8000000&apikey=YourApiKeyToken'}, 'I>[deprecated]</i>GetTknTotalsupplyByTknname': {'description': '<i>[Deprecated]</i>GetTokenTotalSupplybyTokenName(<divstyle=text-decoration:line-through>SupportedTokenNames:DGD,MKR,FirstBlood,HackerGold,ICONOMI,Pluton,REP,SNGLS</div>).Thishasfeaturebeendeprecated,insteadusetheApiabovetolookupanyERC20tokensupplybyitscontractaddress\nexample:\n/api?module=stats&action=tokensupply&tokenname=DGD&apikey=YourApiKeyToken', 'title': '<i>[Deprecated]</i>GetTokenTotalSupplybyTokenName(<divstyle=text-decoration:line-through>SupportedTokenNames:DGD,MKR,FirstBlood,HackerGold,ICONOMI,Pluton,REP,SNGLS</div>).Thishasfeaturebeendeprecated,insteadusetheApiabovetolookupanyERC20tokensupplybyitscontractaddress', 'pieces': {'module': ['stats'], 'action': ['tokensupply'], 'tokenname': ['DGD'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=stats&action=tokensupply&tokenname=DGD&apikey=YourApiKeyToken'}, 'Erc20-tknAccountBalForTkncntrctaddrs': {'description': 'GetERC20-TokenAccountBalanceforTokenContractAddress\nexample:\n/api?module=account&action=tokenbalance&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&tag=latest&apikey=YourApiKeyToken', 'title': 'GetERC20-TokenAccountBalanceforTokenContractAddress', 'pieces': {'module': ['account'], 'action': ['tokenbalance'], 'contractaddress': [], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress', 'address'], 'example': '/api?module=account&action=tokenbalance&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&tag=latest&apikey=YourApiKeyToken'}, 'HistErc20-tknAccountBalForTkncntrctaddrsByBlkno': {'description': 'GetHistoricalERC20-TokenAccountBalanceforTokenContractAddressbyBlockNo\nexample:\n/api?module=account&action=tokenbalancehistory&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&blockno=8000000&apikey=YourApiKeyToken', 'title': 'GetHistoricalERC20-TokenAccountBalanceforTokenContractAddressbyBlockNo', 'pieces': {'module': ['account'], 'action': ['tokenbalancehistory'], 'contractaddress': [], 'address': [], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress', 'address', 'blockno'], 'example': '/api?module=account&action=tokenbalancehistory&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&blockno=8000000&apikey=YourApiKeyToken'}, 'I>[deprecated]</i>GetTknAccountBalByKnownTknname': {'description': '<i>[Deprecated]</i>GetTokenAccountBalancebyknownTokenName(<divstyle=text-decoration:line-through>SupportedTokenNames:DGD,MKR,FirstBlood,ICONOMI,Pluton,REP,SNGLS</div>).Thisfeaturehasbeendeprecated,insteadusetheApiabovetolookupanyERC20tokenbalancebyitscontractaddress\nexample:\n/api?module=account&action=tokenbalance&tokenname=DGD&address=0x4366ddc115d8cf213c564da36e64c8ebaa30cdbd&tag=latest&apikey=YourApiKeyToken', 'title': '<i>[Deprecated]</i>GetTokenAccountBalancebyknownTokenName(<divstyle=text-decoration:line-through>SupportedTokenNames:DGD,MKR,FirstBlood,ICONOMI,Pluton,REP,SNGLS</div>).Thisfeaturehasbeendeprecated,insteadusetheApiabovetolookupanyERC20tokenbalancebyitscontractaddress', 'pieces': {'module': ['account'], 'action': ['tokenbalance'], 'tokenname': ['DGD'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=account&action=tokenbalance&tokenname=DGD&address=0x4366ddc115d8cf213c564da36e64c8ebaa30cdbd&tag=latest&apikey=YourApiKeyToken'}, 'TknInfoByCntrctaddrs': {'description': 'GetTokenInfobyContractAddress\nexample:\n/api?module=token&action=tokeninfo&contractaddress=0x0e3a2a1f2146d86a604adc220b4967a898d7fe07&apikey=YourApiKeyToken', 'title': 'GetTokenInfobyContractAddress', 'pieces': {'module': ['token'], 'action': ['tokeninfo'], 'contractaddress': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress'], 'example': '/api?module=token&action=tokeninfo&contractaddress=0x0e3a2a1f2146d86a604adc220b4967a898d7fe07&apikey=YourApiKeyToken'}, 'EstimationOfConfirmationTime': {'description': 'GetEstimationofConfirmationTime\nexample:\n/api?module=gastracker&action=gasestimate&gasprice=2000000000&apikey=YourApiKeyToken', 'title': 'GetEstimationofConfirmationTime', 'pieces': {'module': ['gastracker'], 'action': ['gasestimate'], 'gasprice': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['gasprice'], 'example': '/api?module=gastracker&action=gasestimate&gasprice=2000000000&apikey=YourApiKeyToken'}, 'GasOracle': {'description': 'GetGasOracle\nexample:\n/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken', 'title': 'GetGasOracle', 'pieces': {'module': ['gastracker'], 'action': ['gasoracle'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken'}, 'TotalSupplyOfEth': {'description': 'GetTotalSupplyofEther\nexample:\n/api?module=stats&action=ethsupply&apikey=YourApiKeyToken', 'title': 'GetTotalSupplyofEther', 'pieces': {'module': ['stats'], 'action': ['ethsupply'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=stats&action=ethsupply&apikey=YourApiKeyToken'}, 'EthLastPrice': {'description': 'GetETHERLastPrice\nexample:\n/api?module=stats&action=ethprice&apikey=YourApiKeyToken', 'title': 'GetETHERLastPrice', 'pieces': {'module': ['stats'], 'action': ['ethprice'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=stats&action=ethprice&apikey=YourApiKeyToken'}, 'EtheumNodesSize': {'description': 'GetEthereumNodesSize\nexample:\n/api?module=stats&action=chainsize&startdate=2019-02-01&enddate=2019-02-28&clienttype=geth&syncmode=default&sort=asc&apikey=YourApiKeyToken', 'title': 'GetEthereumNodesSize', 'pieces': {'module': ['stats'], 'action': ['chainsize'], 'startdate': [], 'enddate': [], 'clienttype': ['geth'], 'syncmode': ['default'], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=chainsize&startdate=2019-02-01&enddate=2019-02-28&clienttype=geth&syncmode=default&sort=asc&apikey=YourApiKeyToken'}, 'EthHistPrice': {'description': 'GetETHERHistoricalPrice\nexample:\n/api?module=stats&action=ethdailyprice&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetETHERHistoricalPrice', 'pieces': {'module': ['stats'], 'action': ['ethdailyprice'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=ethdailyprice&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'EthHistDailyMarketCap': {'description': 'GetETHERHistoricalDailyMarketCap\nexample:\n/api?module=stats&action=ethdailymarketcap&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetETHERHistoricalDailyMarketCap', 'pieces': {'module': ['stats'], 'action': ['ethdailymarketcap'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=ethdailymarketcap&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyTxnCount': {'description': 'GetDailyTransactionCount\nexample:\n/api?module=stats&action=dailytx&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyTransactionCount', 'pieces': {'module': ['stats'], 'action': ['dailytx'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailytx&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyNewAddrsCount': {'description': 'GetDailyNewAddressCount\nexample:\n/api?module=stats&action=dailynewaddress&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyNewAddressCount', 'pieces': {'module': ['stats'], 'action': ['dailynewaddress'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailynewaddress&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageBlkSize': {'description': 'GetDailyAverageBlockSize\nexample:\n/api?module=stats&action=dailyavgblocksize&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageBlockSize', 'pieces': {'module': ['stats'], 'action': ['dailyavgblocksize'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavgblocksize&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageBlkTimeForBlkToBeIncludedInTheEtheumBlkchain': {'description':
 'GetDailyAverageBlockTimeforABlocktobeIncludedintheEthereumBlockchain\nexample:\n/api?module=stats&action=dailyavgblocktime&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageBlockTimeforABlocktobeIncludedintheEthereumBlockchain', 'pieces': {'module': ['stats'], 'action': ['dailyavgblocktime'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavgblocktime&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageGasPriceUsed': {'description': 'GetDailyAverageGasPriceUsed\nexample:\n/api?module=stats&action=dailyavggasprice&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageGasPriceUsed', 'pieces': {'module': ['stats'], 'action': ['dailyavggasprice'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavggasprice&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageGasLimit': {'description': 'GetDailyAverageGasLimit\nexample:\n/api?module=stats&action=dailyavggaslimit&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageGasLimit', 'pieces': {'module': ['stats'], 'action': ['dailyavggaslimit'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavggaslimit&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyTotalGasUsed': {'description': 'GetDailyTotalGasUsed\nexample:\n/api?module=stats&action=dailygasused&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyTotalGasUsed', 'pieces': {'module': ['stats'], 'action': ['dailygasused'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailygasused&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyBlkRew': {'description': 'GetDailyBlockRewards\nexample:\n/api?module=stats&action=dailyblockrewards&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyBlockRewards', 'pieces': {'module': ['stats'], 'action': ['dailyblockrewards'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyblockrewards&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyBlkCount&BlkRew': {'description': 'GetDailyBlockCountandBlockRewards\nexample:\n/api?module=stats&action=dailyblkcount&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyBlockCountandBlockRewards', 'pieces': {'module': ['stats'], 'action': ['dailyblkcount'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyblkcount&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyUncleBlkCount&UncleBlkRew': {'description': 'GetDailyUncleBlockCountandUncleBlockRewards\nexample:\n/api?module=stats&action=dailyuncleblkcount&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyUncleBlockCountandUncleBlockRewards', 'pieces': {'module': ['stats'], 'action': ['dailyuncleblkcount'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyuncleblkcount&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageNetworkHashRate': {'description': 'GetDailyAverageNetworkHashRate\nexample:\n/api?module=stats&action=dailyavghashrate&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageNetworkHashRate', 'pieces': {'module': ['stats'], 'action': ['dailyavghashrate'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavghashrate&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageNetworkDifficulty': {'description': 'GetDailyAverageNetworkDifficulty\nexample:\n/api?module=stats&action=dailyavgnetdifficulty&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageNetworkDifficulty', 'pieces': {'module': ['stats'], 'action': ['dailyavgnetdifficulty'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavgnetdifficulty&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyTotalTxnFee': {'description': 'GetDailyTotalTransactionFee\nexample:\n/api?module=stats&action=dailytxnfee&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyTotalTransactionFee', 'pieces': {'module': ['stats'], 'action': ['dailytxnfee'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailytxnfee&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyNetworkUtilization': {'description': 'GetDailyNetworkUtilization\nexample:\n/api?module=stats&action=dailynetutilization&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyNetworkUtilization', 'pieces': {'module': ['stats'], 'action': ['dailynetutilization'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailynetutilization&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyEnsRegistrationCount': {'description': 'GetDailyENSRegistrationCount\nexample:\n/api?module=stats&action=dailyensregister&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyENSRegistrationCount', 'pieces': {'module': ['stats'], 'action': ['dailyensregister'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyensregister&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}}
options = {'module': ['logs', 'account', 'contract', 'transaction', 'block', 'proxy', 'stats', 'token', 'gastracker'], 'action': ['getLogs', 'balance', 'balancehistory', 'balancemulti', 'txlist', 'txlistinternal', 'tokentx', 'tokennfttx', 'getminedblocks', 'getabi', 'getsourcecode', 'getstatus', 'gettxreceiptstatus', 'getblockreward', 'getblockcountdown', 'getblocknobytime', 'eth_blockNumber', 'eth_getBlockByNumber', 'eth_getUncleByBlockNumberAndIndex', 'eth_getBlockTransactionCountByNumber', 'eth_getTransactionByHash', 'eth_getTransactionByBlockNumberAndIndex', 'eth_getTransactionCount', 'eth_sendRawTransaction', 'eth_getTransactionReceipt', 'eth_call', 'eth_getCode', 'eth_getStorageAt', 'eth_gasPrice', 'eth_estimateGas', 'tokensupply', 'tokensupplyhistory', 'tokenbalance', 'tokenbalancehistory', 'tokeninfo', 'gasestimate', 'gasoracle', 'ethsupply', 'ethprice', 'chainsize', 'ethdailyprice', 'ethdailymarketcap', 'dailytx', 'dailynewaddress', 'dailyavgblocksize', 'dailyavgblocktime', 'dailyavggasprice', 'dailyavggaslimit', 'dailygasused', 'dailyblockrewards', 'dailyblkcount', 'dailyuncleblkcount', 'dailyavghashrate', 'dailyavgnetdifficulty', 'dailytxnfee', 'dailynetutilization', 'dailyensregister']}
inputs = ['fromBlock', 'toBlock', 'topic0', 'topic1', 'page', 'offset', 'address', 'blockno', 'startblock', 'endblock', 'txhash', 'timestamp', 'tag', 'index', 'hex', 'to', 'data', 'position', 'value', 'gasPrice', 'gas', 'contractaddress', 'gasprice', 'startdate', 'enddate','apikey']
def get_api_key(scanner,env_key=None):
    if env_key:
        return get_env_value(key = env_key,deep_scan=True)
    for network in [scanner,'etherscan']:
        env_value = get_env_value(key = f"{network}_api",deep_scan=True)
        if env_value:
            return env_value
def generate_api_variables(generated_url):
    js_all={}
    for each in generated_url.split('?')[-1].split('&'):
        api_key = each.split('=')[0]
        api_val = each.split('=')[1]
        if api_key not in js_all:
            js_all[api_key]= []
        if api_val not in js_all[api_key]:
            js_all[api_key].append(api_val)
    return js_all
def get_generated_url_output(scanner='etherscan.io',selected_api='CntrctSrcCodeForVerifiedCntrctSrcCodes',env_key=None,fromBlock=None,
                             toBlock=None,
                             topic0=None,
                             topic1=None,
                             page=None,
                             offset=None,
                             address=None,
                             contractaddress=None,
                             blockno=None,
                             startblock=None,
                             endblock=None,
                             txhash=None,
                             timestamp=None,
                             tag=None,
                             index=None,
                             hex=None,
                             to=None,
                             data=None,
                             position=None,
                             value=None,
                             gasPrice=None,
                             gas=None,
                             gasprice=None,
                             startdate=None,
                             enddate=None,
                             apikey=None):
    apikey=get_api_key(scanner,env_key=env_key)
    generated_url = apiCallDesc[selected_api]['example']
    values = generate_api_variables(generated_url=generated_url)
    if scanner:
        text=f"https://{('api.' if 'api' != scanner[:len('api')] else '')}{scanner}/api?module={values.get('module')[0]}&action={values.get('action')[0]}"
        js_all_keys = list(values.keys())
        js_all_keys = js_all_keys[2:]
        each_log = {}
        key_values = [fromBlock, toBlock, topic0, topic1, page, offset, address, blockno, startblock, endblock, txhash, timestamp, tag, index, hex, to, data, position, value, gasPrice, gas,contractaddress, gasprice, startdate, enddate,apikey]
        for i,key in enumerate(inputs):
            values[key] = key_values[i]
        for i,each in enumerate(js_all_keys):
            if each not in each_log:
                each_log[each]=0
            value=values.get(each,'')
            if value and isinstance(value,list):
                if len(value) > each_log[each]:
                    value = value[each_log[each]]
            text+="&"+f"{each}"+"="+f"{value}"
            each_log[each]+=1
        text = text.split('apikey=')[0]+f"apikey={apikey}"
        # Here's where you would combine the base URL with the user's inputs 
        # to generate the full API URL. I'm just simulating this step.
        return text

def checksum(address: str=None,rpc_mgr=None,rpc=None,rpc_js=None):
    """
    Attempt to convert the address to a checksum address.

    :param address: Ethereum address to convert.
    :return: Checksum Ethereum address.
    :raises ValueError: If the address is invalid.
    """
    if rpc_mgr:
        if rpc or rpc_js:
            rpc_mgr.update_rpc_js(rpc_js=roc_jc,rpc=rpc)
    if address == None:
        return
    checkSumRefference = create_and_read_json(file_path=get_check_sum_path(),data={})
    if isinstance(address,str):
        
        refferenced_address = checkSumRefference.get(address.lower())
        if refferenced_address:
            return refferenced_address
         
        checked_address = w3_mgr.retrieve_w3(address,rpc=rpc).to_checksum_address(address)
        checkSumRefference[address.lower()]=checked_address
        safe_dump_to_file(file_path=get_check_sum_path(),data=checkSumRefference)
        return checked_address
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in {file_path}")

def write_json(file_path, data):
    if 'user_settings' in data:
        if 'w3' in data['user_settings']:
            del data['user_settings']['w3']
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_directory_path():
    return os.path.dirname(os.path.abspath(__file__))

def get_data_directory():
    return os.path.join(get_directory_path(), 'data')

def get_check_sum_path():
    return os.path.join(get_data_directory(), 'check_sums.json')

def get_source_code_directory():
    return os.path.join(get_data_directory(), 'source_codes')

def create_address_directory(address):
    return os.path.join(get_source_code_directory(),get_normalized_address(address))

def create_network_name_directory(address,network_name):
    return os.path.join(create_address_directory(address),get_normalized_file_name(network_name))

def get_response(response):
    # Improved error handling and response parsing
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print(f"Error processing response: {e}")
        return None
def strip_web(url):
    if isinstance(url,dict):
        url = url.get('url',url)        
    if url:
        if url.startswith("http://"):
            url = url.replace("http://", '', 1)
        elif url.startswith("https://"):
            url = url.replace("https://", '', 1)
        url = url.split('/')[0]
        return url
def make_request(url):
        response = get_response(requests.get(url))
        return response
def get_normalized_address(address):
    if address:
        return str(address).lower()
def get_normalized_file_name(name):
    return name.lower().replace(' ','_')
def get_new_rpc_bridge(rpc_js=None):
    return RPCBridge(rpc_js=rpc_js)

# Simplified to focus on checking source code existence
def check_source_code(address):
    contract_path = create_address_directory(address)
    if os.path.isdir(contract_path):
        rpc_name = w3_mgr.retrieve_rpc_js(address).get('name')
        files = [rpc_name]+os.listdir(contract_path)
        for file in files:
            if file:
                path = os.path.join(contract_path,file)
                source_code_path = os.path.join(path,'source_code.json')
                if os.path.isfile(source_code_path):
                    return source_code_path
    
    

def save_source_code(rpc_js, source_code, address):
    # Simplified saving process
    address_dir = os.path.join(get_source_code_directory(), get_normalized_address(address))
    network_dir = os.path.join(address_dir,get_normalized_file_name(rpc_js['name']))
    rpc_path = os.path.join(network_dir, 'rpc_data.json')
    source_code_path = os.path.join(network_dir, 'source_code.json')
    os.makedirs(address_dir,exist_ok=True)
    os.makedirs(network_dir,exist_ok=True)
    
    write_json(file_path=rpc_path,data=rpc_js)
    write_json(file_path=source_code_path,data=source_code)
    return network_dir

def get_source_code_path(address, rpc_js=None):
    
    source_code_path = check_source_code(address)
    if source_code_path:
        return os.path.dirname(source_code_path)
    derive_network(address=address)
    source_code_path = check_source_code(address)
    if source_code_path:
        return os.path.dirname(source_code_path)
    

def get_response(response):
    get_response,count = None,0
    while get_response == None and count <3:
        try:
            if count ==2:
                get_response = response.text
            if count ==1:
                get_response = response.json()
            if count == 0:
                status_code = response.status_code
        except Exception as e:
            print(e)
        count+=1
    response = get_response or response
    if isinstance(response,dict):
        response = response.get('result',response)
    return safe_json_loads(response)
def make_request(url):

    return get_response(requests.get(url))
    

def derive_network(address=None,multiple=False,initial_network='ethereum'):
    networks_found = []
    
    rpc_mgr_reference = get_new_rpc_bridge(rpc_js=initial_network)
    rpc_list,common_chains = get_default_rpc_list(),get_common_chains()
    initial_network = initial_network or rpc_mgr_reference.name or common_chains[0]
    
    address = checksum(address=address)
    source_code = check_source_code(address)
    if source_code:
        return {"network":read_json(os.path.join(os.path.dirname(source_code),'rpc_data.json')),"contract_data":read_json(source_code)}
    network_list = make_list(initial_network)+common_chains+rpc_list

    for list_itteration,rpc_js in enumerate(network_list):
        found = False
        if rpc_js:
            rpc_mgr = RPCBridge(rpc_js=rpc_js)
            url=get_generated_url_output(scanner=rpc_mgr.scanner,address=address)
         
            response =make_request(url)
            if response and isinstance(response,list):
                if response[0] and isinstance(response[0],dict):
                    if "ContractName" in response[0].keys() and response[0].get("ContractName") not in [None,'',' ']:
                        found = True 
            if found:
                if multiple:
                    save_source_code(rpc_js=rpc_mgr.rpc_js,source_code=response,address=address)
                    networks_found.append({"network":rpc_mgr.rpc_js,"contract_data":response})
                else:
                    save_source_code(rpc_js=rpc_mgr.rpc_js,source_code=response,address=address)
                    return {"network":rpc_mgr.rpc_js,"contract_data":response}
                     
        
            rpc_list = remove_from_list(rpc_list,'name',rpc_mgr_reference.rpc_js['name'])
    return networks_found

