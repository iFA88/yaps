import json
import re
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_SPEC_PATH = os.path.join(BASE_PATH, 'etc', 'api.json')
API_PY_PATH = os.path.join(BASE_PATH, 'yaps', 'src', 'api', 'protocol.py')
API_JS_PATH = '/home/victor/coding/projects/vqtt/ui/src/components/'\
              'models/vqtt_api.js'

PATTERN_START_PY = 'class Commands:\n'
PATTERN_START_JS = 'const Commands = {\n'
PATTERN_END_PY = '    # End of commands\n'
PATTERN_END_JS = '    // End of commands\n'


def build_py_fil2e(spec):
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


def build_py_file(spec):
    fmt = '    {} = {}\n'
    build_file(API_PY_PATH, spec, PATTERN_START_PY, PATTERN_END_PY, fmt)


def build_js_file(spec):
    fmt = '    {}: {},\n'
    build_file(API_JS_PATH, spec, PATTERN_START_JS, PATTERN_END_JS, fmt)


def build_file(filepath, spec, pattern_start, pattern_end, fmt):
    with open(filepath) as f:
        file_data = f.read()

    COMMAND_STRING = f'{pattern_start}.*?{pattern_end}'

    new_class = pattern_start
    for cmd, value in spec['commands'].items():
        new_class += fmt.format(cmd.upper(), value)
        #new_class += f'    {cmd.upper()} = {value}\n'
    new_class += pattern_end

    file_data = re.sub(COMMAND_STRING, new_class, file_data, flags=re.DOTALL)

    with open(filepath, 'w') as f:
        f.write(file_data)

    if re.search(COMMAND_STRING, file_data, flags=re.DOTALL):
        print(f'Build {filepath}')


if __name__ == '__main__':
    with open(API_SPEC_PATH) as f:
        spec = json.load(f)

    build_py_file(spec)
    build_js_file(spec)
