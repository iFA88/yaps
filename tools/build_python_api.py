import json
import re
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_SPEC_PATH = os.path.join(BASE_PATH, 'src', 'api', 'api.json')
API_PY_PATH = os.path.join(BASE_PATH, 'src', 'api', 'protocol.py')


if __name__ == '__main__':
    with open(API_SPEC_PATH) as f:
        spec = json.load(f)

    with open(API_PY_PATH) as f:
        pyfile = f.read()

    PATTERN_START = 'class Commands:\n'
    PATTERN_END = '    # End of commands\n'
    COMMAND_STRING = f'{PATTERN_START}.*?{PATTERN_END}'

    new_class = PATTERN_START
    for cmd, value in spec['commands'].items():
        new_class += f'    {cmd.upper()} = {value}\n'
    new_class += PATTERN_END

    pyfile = re.sub(COMMAND_STRING, new_class, pyfile, flags=re.DOTALL)

    with open(API_PY_PATH, 'w') as f:
        f.write(pyfile)
