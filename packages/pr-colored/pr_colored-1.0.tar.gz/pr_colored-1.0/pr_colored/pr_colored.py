from termcolor import colored

def pr(value, color='blue'):
    if isinstance(value, set):
        value_str = '{\n'
        for item in value:
            value_str += f'    {item},\n'
        value_str += '}'
        value_str = colored(value_str, color)
    elif isinstance(value, dict):
        value_str = '{\n'
        for key, val in value.items():
            value_str += f'    {key}: {val},\n'
        value_str += '}'
        value_str = colored(value_str, color)
    elif isinstance(value, list):
        value_str = '[\n'
        for item in value:
            value_str += f'    {item},\n'
        value_str += ']'
        value_str = colored(value_str, color)
    else:
        value_str = colored(value, color)

    print(value_str)

print('---------------------------------------------------')
