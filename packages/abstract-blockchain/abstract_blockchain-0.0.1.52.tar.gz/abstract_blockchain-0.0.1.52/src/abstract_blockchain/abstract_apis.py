from abstract_webtools import DynamicRateLimiterManager
from .abstract_rpcs import RPCGUIManager,RPCBridge
from abstract_utilities import safe_json_loads,is_number,safe_json_loads,make_list
from abstract_utilities.list_utils import remove_from_list,filter_json_list_values,recursive_json_list
from abstract_security import get_env_value
import requests
import os
from abstract_gui import AbstractWindowManager,sg,ensure_nested_list,expandable,make_component,text_to_key

class ApiGUI:
    def __init__(self,api_mgr=None,rpc_mgr=None,
                 rpc_js:dict=None,
                 rpc_gui:bool=False,
                 address:str=None,
                 contract_address:str=None,
                 start_block:str=None,
                 end_block:str=None,
                 rpc_network:str=None,
                 api_key:str=None,
                 env_key:str=None):
        self.apiCallDesc = {'multiTopic': {'description': 'searchtopics', 'example': 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=12878196&toBlock=12879196&topic0=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef&topic0_1_opr=and&topic1=0x0000000000000000000000000000000000000000000000000000000000000000&page=1&offset=1000&apikey=YourApiKeyToken', 'pieces': {'module': ['logs'], 'action': ['getLogs'], 'fromBlock': [], 'toBlock': [], 'topic0': [], 'topic0_1_opr': ['and'], 'topic1': [], 'page': [], 'offset': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['fromBlock', 'toBlock', 'topic0', 'topic1', 'page', 'offset'], 'title': 'multitopic'},
               'topicSearch': {'description': 'getbytopic', 'title': 'topicsearch', 'pieces': {'module': ['logs'], 'action': ['getLogs'], 'fromBlock': [], 'toBlock': ['latest'], 'address': [], 'topic0': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['fromBlock', 'address', 'topic0'], 'example': 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0x33990122638b9132ca29c723bdf037f1a891a70c&topic0=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545&apikey=YourApiKeyToken'},
               'EthBalForSnglAddrs': {'description': 'GetEtherBalanceforasingleAddress\nexample:\n/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest&apikey=YourApiKeyToken', 'title': 'GetEtherBalanceforasingleAddress', 'pieces': {'module': ['account'], 'action': ['balance'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=account&action=balance&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&tag=latest&apikey=YourApiKeyToken'}, 'HistEthBalForSnglAddrsByBlkno': {'description': 'GetHistoricalEtherBalanceforasingleAddressByBlockNo\nexample:\n/api?module=account&action=balancehistory&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&blockno=8000000&apikey=YourApiKeyToken', 'title': 'GetHistoricalEtherBalanceforasingleAddressByBlockNo', 'pieces': {'module': ['account'], 'action': ['balancehistory'], 'address': [], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'blockno'], 'example': '/api?module=account&action=balancehistory&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&blockno=8000000&apikey=YourApiKeyToken'}, 'EthBalForMulAddrsesInSnglCall': {'description': 'GetEtherBalanceformultipleAddressesinasinglecall\nexample:\n/api?module=account&action=balancemulti&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a,0x63a9975ba31b0b9626b34300f7f627147df1f526,0x198ef1ec325a96cc354c7266a038be8b5c558f67&tag=latest&apikey=YourApiKeyToken', 'title': 'GetEtherBalanceformultipleAddressesinasinglecall', 'pieces': {'module': ['account'], 'action': ['balancemulti'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=account&action=balancemulti&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a,0x63a9975ba31b0b9626b34300f7f627147df1f526,0x198ef1ec325a96cc354c7266a038be8b5c558f67&tag=latest&apikey=YourApiKeyToken'}, 'LstOfNrmlTxnsByAddrs': {'description': 'GetalistofNormalTransactionsByAddress\nexample:\n/api?module=account&action=txlist&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken', 'title': 'GetalistofNormalTransactionsByAddress', 'pieces': {'module': ['account'], 'action': ['txlist'], 'address': [], 'startblock': [], 'endblock': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'startblock', 'endblock'], 'example': '/api?module=account&action=txlist&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken'}, 'LstOfIntlTxnsByAddrs': {'description': 'GetalistofInternalTransactionsbyAddress\nexample:\n/api?module=account&action=txlistinternal&address=0x2c1ba59d6f58433fb1eaee7d20b26ed83bda51a3&startblock=0&endblock=2702578&sort=asc&apikey=YourApiKeyToken', 'title': 'GetalistofInternalTransactionsbyAddress', 'pieces': {'module': ['account'], 'action': ['txlistinternal'], 'address': [], 'startblock': [], 'endblock': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'startblock', 'endblock'], 'example': '/api?module=account&action=txlistinternal&address=0x2c1ba59d6f58433fb1eaee7d20b26ed83bda51a3&startblock=0&endblock=2702578&sort=asc&apikey=YourApiKeyToken'}, 'IntlTxnsByTxnHash': {'description': 'GetInternalTransactionsbyTransactionHash\nexample:\n/api?module=account&action=txlistinternal&txhash=0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170&apikey=YourApiKeyToken', 'title': 'GetInternalTransactionsbyTransactionHash', 'pieces': {'module': ['account'], 'action': ['txlistinternal'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=account&action=txlistinternal&txhash=0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170&apikey=YourApiKeyToken'}, 'IntlTxnsByBlkRng': {'description': 'GetInternalTransactionsbyBlockRange\nexample:\n/api?module=account&action=txlistinternal&startblock=0&endblock=2702578&page=1&offset=10&sort=asc&apikey=YourApiKeyToken', 'title': 'GetInternalTransactionsbyBlockRange', 'pieces': {'module': ['account'], 'action': ['txlistinternal'], 'startblock': [], 'endblock': [], 'page': [], 'offset': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startblock', 'endblock', 'page', 'offset'], 'example': '/api?module=account&action=txlistinternal&startblock=0&endblock=2702578&page=1&offset=10&sort=asc&apikey=YourApiKeyToken'}, 'LstOfErc20-TknTransferEventsByAddrs': {'description': 'GetalistofERC20-TokenTransferEventsbyAddress\nexample:\n/api?module=account&action=tokentx&address=0x4e83362442b8d1bec281594cea3050c8eb01311c&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken', 'title': 'GetalistofERC20-TokenTransferEventsbyAddress', 'pieces': {'module': ['account'], 'action': ['tokentx'], 'address': [], 'startblock': [], 'endblock': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'startblock', 'endblock'], 'example': '/api?module=account&action=tokentx&address=0x4e83362442b8d1bec281594cea3050c8eb01311c&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken'}, 'LstOfErc721-TknTransferEventsByAddrs': {'description': 'GetalistofERC721-TokenTransferEventsbyAddress\nexample:\n/api?module=account&action=tokennfttx&address=0x6975be450864c02b4613023c2152ee0743572325&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken', 'title': 'GetalistofERC721-TokenTransferEventsbyAddress', 'pieces': {'module': ['account'], 'action': ['tokennfttx'], 'address': [], 'startblock': [], 'endblock': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'startblock', 'endblock'], 'example': '/api?module=account&action=tokennfttx&address=0x6975be450864c02b4613023c2152ee0743572325&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken'}, 'LstOfBlksMinedByAddrs': {'description': 'GetlistofBlocksMinedbyAddress\nexample:\n/api?module=account&action=getminedblocks&address=0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b&blocktype=blocks&apikey=YourApiKeyToken', 'title': 'GetlistofBlocksMinedbyAddress', 'pieces': {'module': ['account'], 'action': ['getminedblocks'], 'address': [], 'blocktype': ['blocks'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=account&action=getminedblocks&address=0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b&blocktype=blocks&apikey=YourApiKeyToken'}, 'CntrctAbiForVerifiedCntrctSrcCodes': {'description': 'GetContractABIforVerifiedContractSourceCodes\nexample:\n/api?module=contract&action=getabi&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken', 'title': 'GetContractABIforVerifiedContractSourceCodes', 'pieces': {'module': ['contract'], 'action': ['getabi'], 'address': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=contract&action=getabi&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken'}, 'CntrctSrcCodeForVerifiedCntrctSrcCodes': {'description': 'GetContractSourceCodeforVerifiedContractSourceCodes\nexample:\n/api?module=contract&action=getsourcecode&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken', 'title': 'GetContractSourceCodeforVerifiedContractSourceCodes', 'pieces': {'module': ['contract'], 'action': ['getsourcecode'], 'address': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=contract&action=getsourcecode&address=0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413&apikey=YourApiKeyToken'}, 'HeckCntrctExecutionStatus': {'description': 'CheckContractExecutionStatus(iftherewasanerrorduringcontractexecution)\nexample:\n/api?module=transaction&action=getstatus&txhash=0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a&apikey=YourApiKeyToken', 'title': 'CheckContractExecutionStatus(iftherewasanerrorduringcontractexecution)', 'pieces': {'module': ['transaction'], 'action': ['getstatus'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=transaction&action=getstatus&txhash=0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a&apikey=YourApiKeyToken'}, 'HeckTxnReceiptStatus': {'description': 'CheckTransactionReceiptStatus(OnlyapplicableforPostByzantiumforktransactions)\nexample:\n/api?module=transaction&action=gettxreceiptstatus&txhash=0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76&apikey=YourApiKeyToken', 'title': 'CheckTransactionReceiptStatus(OnlyapplicableforPostByzantiumforktransactions)', 'pieces': {'module': ['transaction'], 'action': ['gettxreceiptstatus'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=transaction&action=gettxreceiptstatus&txhash=0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76&apikey=YourApiKeyToken'},
 'Blk&UncleRewByBlkno': {'description': 'GetBlockAndUncleRewardsbyBlockNo\nexample:\n/api?module=block&action=getblockreward&blockno=2165403&apikey=YourApiKeyToken', 'title': 'GetBlockAndUncleRewardsbyBlockNo', 'pieces': {'module': ['block'], 'action': ['getblockreward'], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['blockno'], 'example': '/api?module=block&action=getblockreward&blockno=2165403&apikey=YourApiKeyToken'}, 'EstBlkCountdownTimeByBlkno': {'description': 'GetEstimatedBlockCountdownTimebyBlockNo\nexample:\n/api?module=block&action=getblockcountdown&blockno=9100000&apikey=YourApiKeyToken', 'title': 'GetEstimatedBlockCountdownTimebyBlockNo', 'pieces': {'module': ['block'], 'action': ['getblockcountdown'], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['blockno'], 'example': '/api?module=block&action=getblockcountdown&blockno=9100000&apikey=YourApiKeyToken'}, 'BlkNumByTimestamp': {'description': 'GetBlockNumberbyTimestamp\nexample:\n/api?module=block&action=getblocknobytime&timestamp=1578638524&closest=before&apikey=YourApiKeyToken', 'title': 'GetBlockNumberbyTimestamp', 'pieces': {'module': ['block'], 'action': ['getblocknobytime'], 'timestamp': [], 'closest': ['before'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['timestamp'], 'example': '/api?module=block&action=getblocknobytime&timestamp=1578638524&closest=before&apikey=YourApiKeyToken'}, 'EventLogsFromBlkNum': {'description': 'GetEventLogsfromblocknumber379224tolatestBlock,wherelogaddress=0x33990122638b9132ca29c723bdf037f1a891a70candtopic[0]=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545\nexample:\n/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0x33990122638b9132ca29c723bdf037f1a891a70c&topic0=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545&apikey=YourApiKeyToken', 'title': 'GetEventLogsfromblocknumber379224tolatestBlock,wherelogaddress=0x33990122638b9132ca29c723bdf037f1a891a70candtopic[0]=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545', 'pieces': {'module': ['logs'], 'action': ['getLogs'], 'fromBlock': [], 'toBlock': ['latest'], 'address': [], 'topic0': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['fromBlock', 'address', 'topic0'], 'example': '/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0x33990122638b9132ca29c723bdf037f1a891a70c&topic0=0xf63780e752c6a54a94fc52715dbc5518a3b4c3c2833d301a204226548a2a8545&apikey=YourApiKeyToken'}, 'Th_blknum': {'description': 'eth_blockNumber\nexample:\n/api?module=proxy&action=eth_blockNumber&apikey=YourApiKeyToken', 'title': 'eth_blockNumber', 'pieces': {'module': ['proxy'], 'action': ['eth_blockNumber'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=proxy&action=eth_blockNumber&apikey=YourApiKeyToken'}, 'Th_getblkbynum': {'description': 'eth_getBlockByNumber\nexample:\n/api?module=proxy&action=eth_getBlockByNumber&tag=0x10d4f&boolean=true&apikey=YourApiKeyToken', 'title': 'eth_getBlockByNumber', 'pieces': {'module': ['proxy'], 'action': ['eth_getBlockByNumber'], 'tag': [], 'boolean': ['true'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['tag'], 'example': '/api?module=proxy&action=eth_getBlockByNumber&tag=0x10d4f&boolean=true&apikey=YourApiKeyToken'}, 'Th_getunclebyblknum&index': {'description': 'eth_getUncleByBlockNumberAndIndex\nexample:\n/api?module=proxy&action=eth_getUncleByBlockNumberAndIndex&tag=0x210A9B&index=0x0&apikey=YourApiKeyToken', 'title': 'eth_getUncleByBlockNumberAndIndex', 'pieces': {'module': ['proxy'], 'action': ['eth_getUncleByBlockNumberAndIndex'], 'tag': [], 'index': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['tag', 'index'], 'example': '/api?module=proxy&action=eth_getUncleByBlockNumberAndIndex&tag=0x210A9B&index=0x0&apikey=YourApiKeyToken'}, 'Th_getblktxncountbynum': {'description': 'eth_getBlockTransactionCountByNumber\nexample:\n/api?module=proxy&action=eth_getBlockTransactionCountByNumber&tag=0x10FB78&apikey=YourApiKeyToken', 'title': 'eth_getBlockTransactionCountByNumber', 'pieces': {'module': ['proxy'], 'action': ['eth_getBlockTransactionCountByNumber'], 'tag': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['tag'], 'example': '/api?module=proxy&action=eth_getBlockTransactionCountByNumber&tag=0x10FB78&apikey=YourApiKeyToken'}, 'Th_gettxnbyhash': {'description': 'eth_getTransactionByHash\nexample:\n/api?module=proxy&action=eth_getTransactionByHash&txhash=0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1&apikey=YourApiKeyToken', 'title': 'eth_getTransactionByHash', 'pieces': {'module': ['proxy'], 'action': ['eth_getTransactionByHash'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=proxy&action=eth_getTransactionByHash&txhash=0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1&apikey=YourApiKeyToken'}, 'Th_gettxnbyblknum&index': {'description': 'eth_getTransactionByBlockNumberAndIndex\nexample:\n/api?module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag=0x10d4f&index=0x0&apikey=YourApiKeyToken', 'title': 'eth_getTransactionByBlockNumberAndIndex', 'pieces': {'module': ['proxy'], 'action': ['eth_getTransactionByBlockNumberAndIndex'], 'tag': [], 'index': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['tag', 'index'], 'example': '/api?module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag=0x10d4f&index=0x0&apikey=YourApiKeyToken'}, 'Th_gettxncount': {'description': 'eth_getTransactionCount\nexample:\n/api?module=proxy&action=eth_getTransactionCount&address=0x2910543af39aba0cd09dbb2d50200b3e800a63d2&tag=latest&apikey=YourApiKeyToken', 'title': 'eth_getTransactionCount', 'pieces': {'module': ['proxy'], 'action': ['eth_getTransactionCount'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=proxy&action=eth_getTransactionCount&address=0x2910543af39aba0cd09dbb2d50200b3e800a63d2&tag=latest&apikey=YourApiKeyToken'}, 'Th_sendrawtxn': {'description': 'eth_sendRawTransaction\nexample:\n/api?module=proxy&action=eth_sendRawTransaction&hex=0xf904808000831cfde080&apikey=YourApiKeyToken', 'title': 'eth_sendRawTransaction', 'pieces': {'module': ['proxy'], 'action': ['eth_sendRawTransaction'], 'hex': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['hex'], 'example': '/api?module=proxy&action=eth_sendRawTransaction&hex=0xf904808000831cfde080&apikey=YourApiKeyToken'}, 'Th_gettxnreceipt': {'description': 'eth_getTransactionReceipt\nexample:\n/api?module=proxy&action=eth_getTransactionReceipt&txhash=0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1&apikey=YourApiKeyToken', 'title': 'eth_getTransactionReceipt', 'pieces': {'module': ['proxy'], 'action': ['eth_getTransactionReceipt'], 'txhash': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['txhash'], 'example': '/api?module=proxy&action=eth_getTransactionReceipt&txhash=0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1&apikey=YourApiKeyToken'}, 'Th_call': {'description': 'eth_call\nexample:\n/api?module=proxy&action=eth_call&to=0xAEEF46DB4855E25702F8237E8f403FddcaF931C0&data=0x70a08231000000000000000000000000e16359506c028e51f16be38986ec5746251e9724&tag=latest&apikey=YourApiKeyToken', 'title': 'eth_call', 'pieces': {'module': ['proxy'], 'action': ['eth_call'], 'to': [], 'data': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['to', 'data'], 'example': '/api?module=proxy&action=eth_call&to=0xAEEF46DB4855E25702F8237E8f403FddcaF931C0&data=0x70a08231000000000000000000000000e16359506c028e51f16be38986ec5746251e9724&tag=latest&apikey=YourApiKeyToken'}, 'Th_getcode': {'description': 'eth_getCode\nexample:\n/api?module=proxy&action=eth_getCode&address=0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c&tag=latest&apikey=YourApiKeyToken', 'title': 'eth_getCode', 'pieces': {'module': ['proxy'], 'action': ['eth_getCode'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=proxy&action=eth_getCode&address=0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c&tag=latest&apikey=YourApiKeyToken'}, 'Th_getstorageat': {'description': 'eth_getStorageAt\nexample:\n/api?module=proxy&action=eth_getStorageAt&address=0x6e03d9cce9d60f3e9f2597e13cd4c54c55330cfd&position=0x0&tag=latest&apikey=YourApiKeyToken', 'title': 'eth_getStorageAt', 'pieces': {'module': ['proxy'], 'action': ['eth_getStorageAt'], 'address': [], 'position': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address', 'position'], 'example': '/api?module=proxy&action=eth_getStorageAt&address=0x6e03d9cce9d60f3e9f2597e13cd4c54c55330cfd&position=0x0&tag=latest&apikey=YourApiKeyToken'}, 'Th_gasprice': {'description': 'eth_gasPrice\nexample:\n/api?module=proxy&action=eth_gasPrice&apikey=YourApiKeyToken', 'title': 'eth_gasPrice', 'pieces': {'module': ['proxy'], 'action': ['eth_gasPrice'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=proxy&action=eth_gasPrice&apikey=YourApiKeyToken'}, 'Th_estimategas': {'description': 'eth_estimateGas\nexample:\n/api?module=proxy&action=eth_estimateGas&to=0xf0160428a8552ac9bb7e050d90eeade4ddd52843&value=0xff22&gasPrice=0x051da038cc&gas=0xffffff&apikey=YourApiKeyToken', 'title': 'eth_estimateGas', 'pieces': {'module': ['proxy'], 'action': ['eth_estimateGas'], 'to': [], 'value': [], 'gasPrice': [], 'gas': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['to', 'value', 'gasPrice', 'gas'], 'example': '/api?module=proxy&action=eth_estimateGas&to=0xf0160428a8552ac9bb7e050d90eeade4ddd52843&value=0xff22&gasPrice=0x051da038cc&gas=0xffffff&apikey=YourApiKeyToken'}, 'Erc20-tknTotalsupplyByCntrctaddrs': {'description': 'GetERC20-TokenTotalSupplybyContractAddress\nexample:\n/api?module=stats&action=tokensupply&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&apikey=YourApiKeyToken', 'title': 'GetERC20-TokenTotalSupplybyContractAddress', 'pieces': {'module':
 ['stats'], 'action': ['tokensupply'], 'contractaddress': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress'], 'example': '/api?module=stats&action=tokensupply&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&apikey=YourApiKeyToken'}, 'HistErc20-tknTotalsupplyByCntrctaddrs&Blkno': {'description': 'GetHistoricalERC20-TokenTotalSupplybyContractAddress&BlockNo\nexample:\n/api?module=stats&action=tokensupplyhistory&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&blockno=8000000&apikey=YourApiKeyToken', 'title': 'GetHistoricalERC20-TokenTotalSupplybyContractAddress&BlockNo', 'pieces': {'module': ['stats'], 'action': ['tokensupplyhistory'], 'contractaddress': [], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress', 'blockno'], 'example': '/api?module=stats&action=tokensupplyhistory&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&blockno=8000000&apikey=YourApiKeyToken'}, 'I>[deprecated]</i>GetTknTotalsupplyByTknname': {'description': '<i>[Deprecated]</i>GetTokenTotalSupplybyTokenName(<divstyle=text-decoration:line-through>SupportedTokenNames:DGD,MKR,FirstBlood,HackerGold,ICONOMI,Pluton,REP,SNGLS</div>).Thishasfeaturebeendeprecated,insteadusetheApiabovetolookupanyERC20tokensupplybyitscontractaddress\nexample:\n/api?module=stats&action=tokensupply&tokenname=DGD&apikey=YourApiKeyToken', 'title': '<i>[Deprecated]</i>GetTokenTotalSupplybyTokenName(<divstyle=text-decoration:line-through>SupportedTokenNames:DGD,MKR,FirstBlood,HackerGold,ICONOMI,Pluton,REP,SNGLS</div>).Thishasfeaturebeendeprecated,insteadusetheApiabovetolookupanyERC20tokensupplybyitscontractaddress', 'pieces': {'module': ['stats'], 'action': ['tokensupply'], 'tokenname': ['DGD'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=stats&action=tokensupply&tokenname=DGD&apikey=YourApiKeyToken'}, 'Erc20-tknAccountBalForTkncntrctaddrs': {'description': 'GetERC20-TokenAccountBalanceforTokenContractAddress\nexample:\n/api?module=account&action=tokenbalance&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&tag=latest&apikey=YourApiKeyToken', 'title': 'GetERC20-TokenAccountBalanceforTokenContractAddress', 'pieces': {'module': ['account'], 'action': ['tokenbalance'], 'contractaddress': [], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress', 'address'], 'example': '/api?module=account&action=tokenbalance&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&tag=latest&apikey=YourApiKeyToken'}, 'HistErc20-tknAccountBalForTkncntrctaddrsByBlkno': {'description': 'GetHistoricalERC20-TokenAccountBalanceforTokenContractAddressbyBlockNo\nexample:\n/api?module=account&action=tokenbalancehistory&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&blockno=8000000&apikey=YourApiKeyToken', 'title': 'GetHistoricalERC20-TokenAccountBalanceforTokenContractAddressbyBlockNo', 'pieces': {'module': ['account'], 'action': ['tokenbalancehistory'], 'contractaddress': [], 'address': [], 'blockno': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress', 'address', 'blockno'], 'example': '/api?module=account&action=tokenbalancehistory&contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055&address=0xe04f27eb70e025b78871a2ad7eabe85e61212761&blockno=8000000&apikey=YourApiKeyToken'}, 'I>[deprecated]</i>GetTknAccountBalByKnownTknname': {'description': '<i>[Deprecated]</i>GetTokenAccountBalancebyknownTokenName(<divstyle=text-decoration:line-through>SupportedTokenNames:DGD,MKR,FirstBlood,ICONOMI,Pluton,REP,SNGLS</div>).Thisfeaturehasbeendeprecated,insteadusetheApiabovetolookupanyERC20tokenbalancebyitscontractaddress\nexample:\n/api?module=account&action=tokenbalance&tokenname=DGD&address=0x4366ddc115d8cf213c564da36e64c8ebaa30cdbd&tag=latest&apikey=YourApiKeyToken', 'title': '<i>[Deprecated]</i>GetTokenAccountBalancebyknownTokenName(<divstyle=text-decoration:line-through>SupportedTokenNames:DGD,MKR,FirstBlood,ICONOMI,Pluton,REP,SNGLS</div>).Thisfeaturehasbeendeprecated,insteadusetheApiabovetolookupanyERC20tokenbalancebyitscontractaddress', 'pieces': {'module': ['account'], 'action': ['tokenbalance'], 'tokenname': ['DGD'], 'address': [], 'tag': ['latest'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['address'], 'example': '/api?module=account&action=tokenbalance&tokenname=DGD&address=0x4366ddc115d8cf213c564da36e64c8ebaa30cdbd&tag=latest&apikey=YourApiKeyToken'}, 'TknInfoByCntrctaddrs': {'description': 'GetTokenInfobyContractAddress\nexample:\n/api?module=token&action=tokeninfo&contractaddress=0x0e3a2a1f2146d86a604adc220b4967a898d7fe07&apikey=YourApiKeyToken', 'title': 'GetTokenInfobyContractAddress', 'pieces': {'module': ['token'], 'action': ['tokeninfo'], 'contractaddress': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['contractaddress'], 'example': '/api?module=token&action=tokeninfo&contractaddress=0x0e3a2a1f2146d86a604adc220b4967a898d7fe07&apikey=YourApiKeyToken'}, 'EstimationOfConfirmationTime': {'description': 'GetEstimationofConfirmationTime\nexample:\n/api?module=gastracker&action=gasestimate&gasprice=2000000000&apikey=YourApiKeyToken', 'title': 'GetEstimationofConfirmationTime', 'pieces': {'module': ['gastracker'], 'action': ['gasestimate'], 'gasprice': [], 'apikey': ['YourApiKeyToken']}, 'inputs': ['gasprice'], 'example': '/api?module=gastracker&action=gasestimate&gasprice=2000000000&apikey=YourApiKeyToken'}, 'GasOracle': {'description': 'GetGasOracle\nexample:\n/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken', 'title': 'GetGasOracle', 'pieces': {'module': ['gastracker'], 'action': ['gasoracle'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken'}, 'TotalSupplyOfEth': {'description': 'GetTotalSupplyofEther\nexample:\n/api?module=stats&action=ethsupply&apikey=YourApiKeyToken', 'title': 'GetTotalSupplyofEther', 'pieces': {'module': ['stats'], 'action': ['ethsupply'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=stats&action=ethsupply&apikey=YourApiKeyToken'}, 'EthLastPrice': {'description': 'GetETHERLastPrice\nexample:\n/api?module=stats&action=ethprice&apikey=YourApiKeyToken', 'title': 'GetETHERLastPrice', 'pieces': {'module': ['stats'], 'action': ['ethprice'], 'apikey': ['YourApiKeyToken']}, 'inputs': [], 'example': '/api?module=stats&action=ethprice&apikey=YourApiKeyToken'}, 'EtheumNodesSize': {'description': 'GetEthereumNodesSize\nexample:\n/api?module=stats&action=chainsize&startdate=2019-02-01&enddate=2019-02-28&clienttype=geth&syncmode=default&sort=asc&apikey=YourApiKeyToken', 'title': 'GetEthereumNodesSize', 'pieces': {'module': ['stats'], 'action': ['chainsize'], 'startdate': [], 'enddate': [], 'clienttype': ['geth'], 'syncmode': ['default'], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=chainsize&startdate=2019-02-01&enddate=2019-02-28&clienttype=geth&syncmode=default&sort=asc&apikey=YourApiKeyToken'}, 'EthHistPrice': {'description': 'GetETHERHistoricalPrice\nexample:\n/api?module=stats&action=ethdailyprice&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetETHERHistoricalPrice', 'pieces': {'module': ['stats'], 'action': ['ethdailyprice'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=ethdailyprice&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'EthHistDailyMarketCap': {'description': 'GetETHERHistoricalDailyMarketCap\nexample:\n/api?module=stats&action=ethdailymarketcap&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetETHERHistoricalDailyMarketCap', 'pieces': {'module': ['stats'], 'action': ['ethdailymarketcap'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=ethdailymarketcap&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyTxnCount': {'description': 'GetDailyTransactionCount\nexample:\n/api?module=stats&action=dailytx&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyTransactionCount', 'pieces': {'module': ['stats'], 'action': ['dailytx'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailytx&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyNewAddrsCount': {'description': 'GetDailyNewAddressCount\nexample:\n/api?module=stats&action=dailynewaddress&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyNewAddressCount', 'pieces': {'module': ['stats'], 'action': ['dailynewaddress'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailynewaddress&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageBlkSize': {'description': 'GetDailyAverageBlockSize\nexample:\n/api?module=stats&action=dailyavgblocksize&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageBlockSize', 'pieces': {'module': ['stats'], 'action': ['dailyavgblocksize'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavgblocksize&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageBlkTimeForBlkToBeIncludedInTheEtheumBlkchain': {'description':
 'GetDailyAverageBlockTimeforABlocktobeIncludedintheEthereumBlockchain\nexample:\n/api?module=stats&action=dailyavgblocktime&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageBlockTimeforABlocktobeIncludedintheEthereumBlockchain', 'pieces': {'module': ['stats'], 'action': ['dailyavgblocktime'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavgblocktime&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageGasPriceUsed': {'description': 'GetDailyAverageGasPriceUsed\nexample:\n/api?module=stats&action=dailyavggasprice&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageGasPriceUsed', 'pieces': {'module': ['stats'], 'action': ['dailyavggasprice'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavggasprice&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageGasLimit': {'description': 'GetDailyAverageGasLimit\nexample:\n/api?module=stats&action=dailyavggaslimit&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageGasLimit', 'pieces': {'module': ['stats'], 'action': ['dailyavggaslimit'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavggaslimit&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyTotalGasUsed': {'description': 'GetDailyTotalGasUsed\nexample:\n/api?module=stats&action=dailygasused&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyTotalGasUsed', 'pieces': {'module': ['stats'], 'action': ['dailygasused'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailygasused&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyBlkRew': {'description': 'GetDailyBlockRewards\nexample:\n/api?module=stats&action=dailyblockrewards&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyBlockRewards', 'pieces': {'module': ['stats'], 'action': ['dailyblockrewards'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyblockrewards&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyBlkCount&BlkRew': {'description': 'GetDailyBlockCountandBlockRewards\nexample:\n/api?module=stats&action=dailyblkcount&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyBlockCountandBlockRewards', 'pieces': {'module': ['stats'], 'action': ['dailyblkcount'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyblkcount&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyUncleBlkCount&UncleBlkRew': {'description': 'GetDailyUncleBlockCountandUncleBlockRewards\nexample:\n/api?module=stats&action=dailyuncleblkcount&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyUncleBlockCountandUncleBlockRewards', 'pieces': {'module': ['stats'], 'action': ['dailyuncleblkcount'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyuncleblkcount&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageNetworkHashRate': {'description': 'GetDailyAverageNetworkHashRate\nexample:\n/api?module=stats&action=dailyavghashrate&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageNetworkHashRate', 'pieces': {'module': ['stats'], 'action': ['dailyavghashrate'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavghashrate&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyAverageNetworkDifficulty': {'description': 'GetDailyAverageNetworkDifficulty\nexample:\n/api?module=stats&action=dailyavgnetdifficulty&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyAverageNetworkDifficulty', 'pieces': {'module': ['stats'], 'action': ['dailyavgnetdifficulty'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyavgnetdifficulty&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyTotalTxnFee': {'description': 'GetDailyTotalTransactionFee\nexample:\n/api?module=stats&action=dailytxnfee&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyTotalTransactionFee', 'pieces': {'module': ['stats'], 'action': ['dailytxnfee'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailytxnfee&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyNetworkUtilization': {'description': 'GetDailyNetworkUtilization\nexample:\n/api?module=stats&action=dailynetutilization&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyNetworkUtilization', 'pieces': {'module': ['stats'], 'action': ['dailynetutilization'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailynetutilization&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}, 'DailyEnsRegistrationCount': {'description': 'GetDailyENSRegistrationCount\nexample:\n/api?module=stats&action=dailyensregister&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken', 'title': 'GetDailyENSRegistrationCount', 'pieces': {'module': ['stats'], 'action': ['dailyensregister'], 'startdate': [], 'enddate': [], 'sort': ['asc'], 'apikey': ['YourApiKeyToken']}, 'inputs': ['startdate', 'enddate'], 'example': '/api?module=stats&action=dailyensregister&startdate=2019-02-01&enddate=2019-02-28&sort=asc&apikey=YourApiKeyToken'}}
        self.options = {'module': ['logs', 'account', 'contract', 'transaction', 'block', 'proxy', 'stats', 'token', 'gastracker'], 'action': ['getLogs', 'balance', 'balancehistory', 'balancemulti', 'txlist', 'txlistinternal', 'tokentx', 'tokennfttx', 'getminedblocks', 'getabi', 'getsourcecode', 'getstatus', 'gettxreceiptstatus', 'getblockreward', 'getblockcountdown', 'getblocknobytime', 'eth_blockNumber', 'eth_getBlockByNumber', 'eth_getUncleByBlockNumberAndIndex', 'eth_getBlockTransactionCountByNumber', 'eth_getTransactionByHash', 'eth_getTransactionByBlockNumberAndIndex', 'eth_getTransactionCount', 'eth_sendRawTransaction', 'eth_getTransactionReceipt', 'eth_call', 'eth_getCode', 'eth_getStorageAt', 'eth_gasPrice', 'eth_estimateGas', 'tokensupply', 'tokensupplyhistory', 'tokenbalance', 'tokenbalancehistory', 'tokeninfo', 'gasestimate', 'gasoracle', 'ethsupply', 'ethprice', 'chainsize', 'ethdailyprice', 'ethdailymarketcap', 'dailytx', 'dailynewaddress', 'dailyavgblocksize', 'dailyavgblocktime', 'dailyavggasprice', 'dailyavggaslimit', 'dailygasused', 'dailyblockrewards', 'dailyblkcount', 'dailyuncleblkcount', 'dailyavghashrate', 'dailyavgnetdifficulty', 'dailytxnfee', 'dailynetutilization', 'dailyensregister']}
        self.inputs = ['fromBlock', 'toBlock', 'topic0', 'topic1', 'page', 'offset', 'address', 'blockno', 'startblock', 'endblock', 'txhash', 'timestamp', 'tag', 'index', 'hex', 'to', 'data', 'position', 'value', 'gasPrice', 'gas', 'contractaddress', 'gasprice', 'startdate', 'enddate','apikey']

        self.api_mgr = api_mgr
        if self.api_mgr == None:
            self.api_mgr=APIBridge(rpc_mgr=rpc_mgr,
                 rpc_js=rpc_js,
                 rpc_gui=rpc_gui,
                 address=address,
                 contract_address=contract_address,
                 start_block=start_block,
                 end_block=end_block,
                 rpc_network=rpc_network,
                 api_key=api_key,
                 env_key=env_key)
        self.rpc_mgr_gui=RPCGUIManager(rpc_mgr=self.api_mgr.rpc_mgr,gui_window=False)
        self.rpc_gui_keys=[]
        self.section='APIMGR'
        for key in self.rpc_mgr_gui.all_keys:
            self.rpc_gui_keys.append(text_to_key(key,section=self.section))
        api_keys = list(self.apiCallDesc.keys())
        # Main Window Layout
        output = ensure_nested_list(make_component("Multiline",'',key='-API_OUTPUT-', disabled=True,**expandable()))
        rpc_layout = self.rpc_mgr_gui.get_rpc_layout(section=self.section)
        self.layout = [[rpc_layout],
            [[make_component("Frame","api output",layout=output,**expandable(size=(None,180)))],sg.Text('Select API Call Type:'), sg.Combo(values=api_keys,default_value=api_keys[0], key='API_SELECT', enable_events=True)],
            [sg.Frame('Parameters:', [[sg.Column(self.generate_api_gui(self.apiCallDesc[api_keys[0]]), key='API_GUI')]])]
        ]
        
        self.windows_mgr=AbstractWindowManager()
        self.window_name = self.windows_mgr.add_window(title='API Call GUI', layout=self.layout,close_events=['Exit',"OK"],event_handlers=[self.while_window])
        self.windows_mgr.while_window(window_name=self.window_name)
        self.api_url = self.windows_mgr.search_closed_windows(window_name=self.window_name)['values']['API_URL']
    def generate_api_gui(self,api_desc):
        """
        Function to generate GUI layout based on the selected API description.
        """
        layout = []
        # Add an "Execute" button
        
        layout.append([sg.Column(ensure_nested_list([[sg.Button('Generate URL')],
                                                     [sg.Button("Get Output")]])),
                       sg.Column(ensure_nested_list([[sg.Button("OK")],
                                                     [sg.Exit()]
                                                     ]
                                                    )),
                       sg.Column(ensure_nested_list([
                           [sg.Checkbox(text="input api key",key="-API_KEY_TOGGLE-",default=False,enable_events=True)],
                           [sg.Checkbox(text="select api url",key="-SCANNER_TOGGLE-",default=False,enable_events=True)]
                           ]))])
        # Add a multi-line input box to display the generated API URL
        layout.append([sg.Multiline(size=(50, 5), key='API_URL', disabled=True)])
        # Generate input fields
        for key in self.options:
            layout.append([sg.Text(f'{key}:'), sg.Input(default_text='',key=f'-{key.upper()}_SELECT-',disabled=True,enable_events=True)])
        for i,each in enumerate(self.inputs):
            layout.append([sg.T(text=f':',key=f"-{i}_TEXT-",visible=False),sg.Push(),
                           sg.Input(size=(45,1),key=f'-{i}_INPUT-',visible=False),
                           sg.T(text='example:',key=f"-{i}_EXAMPLE_TEXT-",visible=False),
                           sg.Input(size=(45,1),key=f'-{i}_EXAMPLE_INPUT-',disabled=True,visible=False)])

        return layout
    def get_defaults(self,each):
            each_inp =''
            
            if each == 'address':
                each_inp = self.api_mgr.address or ''
            elif each == 'contract_address':
                each_inp = self.api_mgr.contract_address or ''
            elif each == 'end_block':
                each_inp = self.api_mgr.end_block or ''
            elif each == 'start_block':
                each_inp = self.api_mgr.start_block or ''
            elif each == 'apikey':
                each_inp = self.api_mgr.api_key or ''
            elif each == 'env_key':
                each_inp = self.api_mgr.env_key or ''

            return each_inp
    def get_revised_dict(self,desired_keys):
        js_ls = []
        for topic,data in self.apiCallDesc.items():
            js_ls.append(data["pieces"])
        recursive_list = recursive_json_list(js_ls,desired_keys)
        filtered_list = filter_json_list_values(recursive_list,recursive_list[0].keys())
        for each in filtered_list.keys():
            filtered_list[each] = filtered_list[each][0]
        return filtered_list
    def generate_api_variables(self,values):
        selected_api = values['API_SELECT']
        api_data = self.apiCallDesc[selected_api]
        generated_url = api_data['example']
        js_all={}
        for each in generated_url.split('?')[-1].split('&'):
            api_key = each.split('=')[0]
            api_val = each.split('=')[1]
            if api_key not in js_all:
                js_all[api_key]= []
            if api_val not in js_all[api_key]:
                js_all[api_key].append(api_val)
        return js_all
    def make_invisible_unless(self,example):
        highest = 0
        for each in self.visible_list:
            if len(each)>highest:
                highest=len(each)
        for i,each in enumerate(self.visible_list):
            extra = highest-len(each)
            self.window[f'-{i}_TEXT-'].update(value=each,visible=True)
            self.window[f'-{i}_INPUT-'].update(visible=True)
            self.window[f'-{i}_EXAMPLE_TEXT-'].update(visible=True)
            self.window[f'-{i}_EXAMPLE_INPUT-'].update(value=example[each][0],visible=True)
        for each in self.values.keys():
            if '_INPUT-' in each:
                num_each = each[1:].split('_')[0]
                if int(num_each) >i:    
                    self.window[f'-{num_each}_TEXT-'].update(visible=False)
                    self.window[f'-{num_each}_INPUT-'].update(visible=False)
                    self.window[f'-{num_each}_EXAMPLE_TEXT-'].update(visible=False)
                    self.window[f'-{num_each}_EXAMPLE_INPUT-'].update(visible=False)
    def get_input_key(self,values,text_value):
        for key,value in values.items():
            if value == text_value:
                return f"-{key[1:-1].split('_')[0]}_INPUT-"
    def get_generated_url_output(self):
        selected_api = self.values['API_SELECT']
        api_data = self.apiCallDesc[selected_api]
        module = self.values["-MODULE_SELECT-"]
        action = self.values["-ACTION_SELECT-"]
        text='module'+'='+f'{module}'+'&action='+f'{action}'
        js_all=self.generate_api_variables(self.values)
        js_all_keys = list(js_all.keys())
        js_all_keys = js_all_keys[2:] 
        for i,each in enumerate(js_all_keys):
            inputs = self.values['-'+str(i)+'_INPUT-']
            if inputs == '':
                inputs = self.values['-'+str(i)+'_EXAMPLE_INPUT-']
            text+="&"+f"{each}"+"="+f"{inputs}"
        text = text.split('apikey=')[0]+'apikey='
        if self.values["-API_KEY_TOGGLE-"]:
            key = self.get_input_key(self.values,'YourApiKeyToken')
            if key:
                text+=self.values[key]
        if self.values['-SCANNER_TOGGLE-']:
            scanner = self.api_mgr.rpc_mgr.scanner
            if scanner:
                scanner_protocol = f"https://{('api.' if 'api' != scanner else '')}{scanner}/api?"
                text=scanner_protocol+text
        # Here's where you would combine the base URL with the user's inputs 
        # to generate the full API URL. I'm just simulating this step.
        return text
    def toggle_scanner(self):
        output=None
        generated_url= self.values['API_URL']
        value  = self.values['-SCANNER_TOGGLE-']
        scanner,scanner_protocol = self.api_mgr.rpc_mgr.scanner,None
        if scanner:
            scanner_protocol = f"https://{('api.' if 'api' != scanner else '')}{scanner}/api?"
        if value:
            if scanner_protocol:
                if '/api?' in generated_url:
                    generated_url=generated_url.split('/api?')[-1]
                output=f"{scanner_protocol}{generated_url}"
        else:
            if '/api?' in generated_url:
                output=generated_url.split('/api?')[-1]
        return output
    def toggle_api_key(self):
        output=None
        generated_url = self.values['API_URL']
        if generated_url:
            key = self.get_input_key(self.values,'YourApiKeyToken')
            if key:
                value = self.values[key]
                if value:
                    if self.values["-API_KEY_TOGGLE-"]:
                        if generated_url.endswith('apikey='):
                            output=self.values['API_URL']+value
                    else:
                        if generated_url.endswith(value):
                            output=generated_url[:-len(value)]
        return output
    def while_window(self,event,values,window):
        self.event,self.values,self.window=event,values,window

        # If user selects a different API from the dropdown
        if event == "Get Output":
            scanner_toggle,api_key_toggle=self.values['-SCANNER_TOGGLE-'],self.values["-API_KEY_TOGGLE-"]
            self.values['-SCANNER_TOGGLE-'],self.values["-API_KEY_TOGGLE-"]=True,True
            generated_url = self.get_generated_url_output()
            self.values['-SCANNER_TOGGLE-'],self.values["-API_KEY_TOGGLE-"]=scanner_toggle,api_key_toggle
            window['-API_OUTPUT-'].update(self.api_mgr.make_request(generated_url))
        elif event == 'API_SELECT':
            selected_api = values['API_SELECT']
            window['API_GUI'].update(self.generate_api_gui(self.apiCallDesc[selected_api]))
            js_all=self.generate_api_variables(values)
            self.visible_list = []
            for each in js_all.keys():
                if each not in ['action','module']:
                   self.visible_list.append(each)
            self.window['-MODULE_SELECT-'].update(value=js_all["module"][0])
            self.window['-ACTION_SELECT-'].update(value=js_all["action"][0])
            self.make_invisible_unless(js_all)
            js_all=self.generate_api_variables(values)
            js_all_keys = list(js_all.keys())
            js_all_keys = js_all_keys[2:]
            for i,each in enumerate(js_all_keys):
                inputs = window['-'+str(i)+'_INPUT-'].update(self.get_defaults(each))
        elif "_SELECT-" in event:
            desired_keys = {event[1:-len("_SELECT-")].lower():[values[event]]}
            filtered_list = self.get_revised_dict(desired_keys)
            self.window['-ACTION_SELECT-'].update(values=filtered_list["action"],value=filtered_list["action"][0])
            self.visible_list = []
            text=''
            for each in filtered_list.keys():
                if each in self.inputs:
                    self.visible_list.append(each)
                else:
                    value = filtered_list[each]
                    if isinstance(value,list):
                        if len(value)>0:
                            value = value[0]
                    text+=("&" if text != '' else '')+each+"="+value
            self.window['API_URL'].update(value=text)
            self.make_invisible_unless(self.visible_list)
        # Generate the API URL based on the inputs
        elif event == "-API_KEY_TOGGLE-":
            toggle=self.toggle_api_key()
            if toggle:
                window['API_URL'].update(toggle)
        elif event == '-SCANNER_TOGGLE-':
            toggle=self.toggle_scanner()
            if toggle:
                window['API_URL'].update(toggle)
        elif event == 'Generate URL':
            generated_url=self.get_generated_url_output()
            if generated_url:
                self.window['API_URL'].update(generated_url)
        elif event in self.rpc_gui_keys:
           self.rpc_mgr_gui.rpc_win_while(self.event,self.values,self.window)
           rpc_js = self.rpc_mgr_gui.get_rpc_values(values)
           self.api_mgr.rpc_mgr.setup_rpc_attributes(rpc_js)
           self.api_mgr.get_api_key()
class APIBridge:
    def __init__(self,rpc_mgr:str=None,
                 api_data_type:str=None,
                 rpc_network:str=None,
                 api_key:str=None,
                 env_key:str=None,
                 service_name:str=None,
                 api_url_data:str=None,
                 rpc_js:dict=None,
                 address:str=None,
                 contract_address:str=None,
                 start_block:str=None,
                 end_block:str=None,
                 low_limit:int=10,
                 high_limit:int=30,
                 rpc_gui:bool=False,
                 api_gui:bool=False):
        
        self.get_api_key_network=[]
        self.rate_limiter = DynamicRateLimiterManager()
        
        
        self.rpc_mgr=rpc_mgr
        self.rpc_js=rpc_js
        self.rpc_gui=rpc_gui
        self.update_rpc(rpc_mgr=rpc_mgr,rpc_js=rpc_js,rpc_gui=rpc_gui)
        
        self.env_key=env_key
        self.rpc_network=rpc_network
        self.api_key=self.get_api_key(rpc_network=rpc_network,api_key=api_key,env_key=env_key)

        self.api_service_tracker={}
        self.update_service_name(service_name=service_name, low_limit=low_limit, high_limit=high_limit)
        
        self.contract_address=contract_address
        self.address=address
        self.update_address(address=address,contract_address=contract_address)
        
        self.start_block=start_block
        self.api_data_type = api_data_type
        self.api_url_data = api_url_data
        self.start_block=start_block
        self.end_block=end_block
        self.update_api_call_partameters(address=self.address,contract_address=self.contract_address,start_block=self.start_block,end_block=self.end_block,api_data_type=self.api_data_type,api_gui=api_gui)
    def update_rpc(self,rpc_mgr=None,rpc_js=None,rpc_gui=False):
        if rpc_gui:
            self.rpc_gui_mgr = RPCGUIManager(rpc_mgr=rpc_mgr)
            self.rpc_mgr = self.rpc_gui_mgr.rpc_mgr
        if self.rpc_mgr == None:
            if rpc_mgr:
                self.rpc_mgr = rpc_mgr
            else:
                self.rpc_mgr = RPCBridge(rpc_js=rpc_js)
        elif rpc_mgr or rpc_js:
            if rpc_mgr and self.rpc_mgr != rpc_mgr:
                self.rpc_mgr = rpc_mgr
            else:
                if rpc_js != self.rpc_mgr.rpc_js:
                   self.rpc_mgr.update_rpc_js(rpc_js=rpc_js)
                   
    def update_service_name(self, service_name=None, low_limit=10, high_limit=30):
        self.service_name = service_name
        if self.service_name == None:
            api_key_identifier = hash(self.api_key)  # or some other unique identifier
            self.service_name = f"{self.rpc_mgr.scanner}_{api_key_identifier}"
        # Register service name and API key
        self.api_service_tracker[self.service_name] = self.api_key
        # Configure rate limiter for the service
        self.rate_limiter.add_service(service_name=self.service_name, low_limit=low_limit, high_limit=high_limit)

    def update_address(self,address=None,contract_address=None):
        if address == False:
            self.address=None
        else:
            self.address=address or self.address
            if self.address:
                self.address=self.rpc_mgr.w3.to_checksum_address(self.address)
            
        if contract_address == False:
            self.contract_address=None
        else:
            self.contract_address = contract_address or self.contract_address
            if self.contract_address:
                self.contract_address = self.rpc_mgr.w3.to_checksum_address(self.contract_address)
    def update_api_call_partameters(self,rpc_mgr=None,rpc_js=None,address=None,contract_address=None,start_block=None,end_block=None,api_data_type=None,api_gui=None):
        if rpc_mgr or rpc_js:
            self.update_rpc(rpc_mgr=rpc_mgr,rpc_js=rpc_js)
            self.get_api_key()
        self.update_address(address=address,contract_address=contract_address)
        self.api_data_type = None if api_data_type == False else api_data_type or self.api_data_type
        self.start_block =  None if start_block == False else start_block or self.start_block
        self.end_block = None if end_block == False else end_block or self.end_block
        self.api_data_type =  None if api_data_type == False else api_data_type or self.api_data_type
        if self.address or self.contract_address:

            if self.api_data_type and self.api_data_type.lower() in ['sourcecode', 'abi'] and self.contract_address:
                self.api_url_data = f"module=contract&action=get{self.api_data_type.lower()}&address={self.contract_address}"
            elif self.start_block and self.end_block:
                self.api_url_data = f"module=account&action=tokentx&address={self.address}&startblock={self.start_block}&endblock={self.end_block}&sort=asc"
            elif self.contract_address:
                self.api_url_data = f"module=account&action=tokenbalance&contractaddress={self.contract_address}&address={self.address}&tag=latest"
        elif self.contract_address:
            self.api_url_data = f"module=module=stats&action=tokensupply&contractaddress={self.contract_address}"
        self.make_api_call(self,api_gui=api_gui,api_url_data=self.api_url_data)
    def get_api_key(self,rpc_network=None,api_key=None,env_key=None):
        if rpc_network == None and self.rpc_mgr.scanner:
            rpc_network = os.path.splitext(self.rpc_mgr.scanner)[0]
        self.rpc_network = rpc_network
        if api_key:
             self.api_key = api_key
             return self.api_key
        if env_key:
            env_value = get_env_value(key=env_key)
            if env_value:
                self.api_key=env_value
                return self.api_key
        
        for network in [self.rpc_network,'etherscan']:
            self.api_key = get_env_value(key = f"{network}_api",deep_scan=True)
            if self.api_key:
                return self.api_key
    def get_response(self,response):
        get_response,count = None,0
        while get_response == None and count <3:
            try:
                if count ==2:
                    get_response = response.text
                if count ==1:
                    get_response = response.json()
                if count == 0:
                    self.status_code = response.status_code
            except Exception as e:
                print(e)
            count+=1
        response = get_response or response
        if isinstance(response,dict):
            response = response.get('result',response)
        return safe_json_loads(response)
    def make_request(self,url):
        response = None
        try:
            response = self.get_response(requests.get(url))
            return response
        except:
            pass
        return response
    def make_api_call(self,api_url=None,api_gui=False,api_url_data=None):
        self.api_url_data = api_url_data or self.api_url_data
        if api_gui:
            self.api_gui_mgr = ApiGUI(api_mgr=self)#choose_api_gui(address=address,contract_address=contract_address,start_block=start_block,end_block=end_block)
            self.api_url=f"https://{('api.' if 'api' != self.rpc_mgr.scanner[:len('api')] else '')}{self.rpc_mgr.scanner}/api?{self.api_gui_mgr.api_url}"
        try:
            if self.api_url == None:
                self.api_url = f"https://{('api.' if 'api' != self.rpc_mgr.scanner[:len('api')] else '')}{self.rpc_mgr.scanner}/api?{self.api_url_data}&apikey={self.api_key}"
            self.response = self.make_request(url=self.api_url)
            #self.response = self.request_manager.get_limited_request(request_url=self.api_url,service_name=self.service_name)               
            if self.response == "Invalid API Key":
                self.get_api_key_network.append(self.rpc_mgr.rpc_js)
            return self.response
        except Exception as e:
            print(e)
    def _make_request(self, url):
            # Utilize the rate limiter manager to make the request
            try:
                return self.rate_limiter.get_limited_request(self.rate_limiter.services[self.service_name], url, self.service_name)
            except Exception as e:
                logging.error(f"Error in making request: {e}")
                return None
    def derive_network(self,contract_address=None,api_data_type='sourcecode',multiple=False,initial_network=None):
        networks_found = []
        rpc_mgr_reference = RPCBridge()
        rpc_list,common_chains = rpc_mgr_reference.get_default_rpc_list(),rpc_mgr_reference.common_chains
        initial_network = initial_network or common_chains[0]
        self.contract_address = contract_address or self.contract_address
        self.api_data_type = 'sourcecode' if api_data_type in ['sourcecode','abi'] else api_data_type
        for list_itteration,list_obj in enumerate([make_list(initial_network),common_chains,rpc_list]):
            for network in list_obj:
                found = False
                
                if network:
                    rpc_js=network
                    if list_itteration != 2:
                        rpc_js = [network]
                    
                    
                    self.update_api_call_partameters(rpc_js=rpc_js,address=False,contract_address=self.contract_address,api_data_type=self.api_data_type)
                    
                    if self.response and isinstance(self.response,list):
                        if api_data_type in ['sourcecode','abi'] and self.response[0] and isinstance(self.response[0],dict):
                            if "ContractName" in self.response[0].keys() and self.response[0].get("ContractName") not in [None,'',' ']:
                                found = True 
                    if found:
                        if multiple:
                            networks_found.append({"network":self.rpc_mgr.rpc_js,"contract_data":self.response})
                        else:
                            return {"network":self.rpc_mgr.rpc_js,"contract_data":self.response}
                    rpc_list = remove_from_list(rpc_list,'name',self.rpc_mgr.rpc_js['name'])
        return networks_found
