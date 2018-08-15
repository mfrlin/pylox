import sys

import scanner


def run(source):
    tokens  = scanner.Scanner(source).scan_tokens()
    for token in tokens:
        print(token)

def run_file(filename):
    with open(filename, 'r') as f:
        run(f.read())

def run_prompt():
    while True:
        run(raw_input('> '))

def error(line_num, message, where=''):
    print('[line {}] Error {}: {}'.format(line_num, where, msg))


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('Usage: pylox [script]')
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()
