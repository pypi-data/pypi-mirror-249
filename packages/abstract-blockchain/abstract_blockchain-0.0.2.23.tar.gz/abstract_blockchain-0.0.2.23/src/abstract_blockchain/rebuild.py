abstract_contract_console_main()
script_rebuild=''
change=False
for i,char in enumerate(script):
    
    if len(script_rebuild) >= len('**{"') and script_rebuild[i-len('**{"'):]=='**{"':
        change = True
        change_i =i
        script_rebuild=script_rebuild[:-len('**{"')]
        brackets_js = {'{':1,'}':0,"change_text":'**{"',"i_change":i-len('**{"')}
    if change:
        if char in brackets_js:
            brackets_js[char]+=1
        if brackets_js['{'] - brackets_js['}'] == 0:
            change = False
            brackets_js["i_change"]
            for each in brackets_js["change_text"].split(','):
                split_each = each.split(':')
                script_rebuild += f"{split_each[0][1:-1]}={split_each[1]}"
        else:
            brackets_js["change_text"]+=char
            input(brackets_js["change_text"])
    else:
        script_rebuild += char
input(script_rebuild)
