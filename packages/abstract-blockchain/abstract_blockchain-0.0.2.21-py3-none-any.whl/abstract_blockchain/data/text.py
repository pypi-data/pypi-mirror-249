from abstract_utilities.json_utils import get_dict_from_string,find_matching_dicts
from abstract_utilities import read_from_file,safe_json_loads,safe_dump_to_file,safe_read_from_json,make_list
rpc_list = read_from_file('rpc_list.txt')
key_list = """networkId,name,chain,shortName,nativeCurrency,chainId,explorers,rpc""".split(',')
for item in safe_read_from_json('rpc_list.json')['chains']:
    for key in key_list:
        if key in item:
            if key == 'rpc':
                input(find_matching_dicts(dict_objs=item[key],keys=['tracking'],values=['none']))
            else:
                print(item[key])
