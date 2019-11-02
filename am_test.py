# V1.4 2019/11/02 Jason Haenlin

# Changelog
# V1.0 : Init
# V1.1 : Add some comments
# V1.2 : Change functions names (bad namming)
# V1.3 : Add an other solution in the parse_output
# V1.4 : add an other solution and add a try/catch to be notified in case of error

import re
import subprocess
from math import floor, log2

import matplotlib.pyplot as plt
import numpy as np

am_path = 'am'

# Change this file
file = 'minip1.txt'
# Adjust the tapes
tapes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
         15, 16, 17, 18, 19, 20, 40, 80, 160, 320, 640,
         1280, 2560, 5120, 10240, 20480]

# Go to the main function (go down !)


def median_validation(result_tape, median_label='A'):
    '''get the position of the median and compare with the result tape'''
    result_tape = list("".join(re.split('<|>|_', result_tape)))
    median_pos = floor(len(result_tape)/2) - \
        (0 if len(result_tape) % 2 == 1 else 1)
    return True if result_tape[median_pos] == median_label else False


def slicing_validation(result_tape, median_label='A', log=False):
    '''build the slicing word and compare with the result tape'''
    result_tape = "".join(re.split('<|>|_', result_tape))
    l = len(result_tape)
    separator = 1
    tape = []

    if l <= 4:
        separator = 4
        for i in reversed(range(l)):
            tape.insert(0, str(separator))
            separator = separator - 1
        if log:
            print("".join(tape))
        return "".join(tape) == result_tape

    tape = ['X' for i in range(l)]
    tape[floor(l/2)-1-(1 if ((l-2) % 4) == 0 else 0)] = median_label
    tape[floor(l/4)-1] = median_label
    tape[floor(l/2 + l/4)-1] = median_label
    if log:
        print("".join(tape))
    i = 0
    separator = 1
    while i < l:
        nexti = tape[i]
        tape[i] = str(separator)
        if (nexti == median_label):
            separator = separator + 1
        i = i + 1
    strp = "".join(tape)
    st = strp == result_tape
    return "".join(tape) == result_tape


def parse_output(output):
    try:
        parser = {
            'result': output.split(' ')[0].split('\n')[2],
            'step': int(output.split(' ')[2])
            # If it bugs, try this maybe :)
            # 'result': output.split('\n')[0],
            # 'step': int(output.split('\n')[1].split(' ')[2])
            # or this maybe ^^"
            # 'result': output.split('\n')[0],
            # 'step': int(output.split(' ')[2])
        }
    except IndexError:
        print('bad output : ', output)
        exit(0)

    return parser


def plot_test(results):
    """ Plot a list of results
    Parameters
    ----------
    results
        lists of result appended from
        nsquare_plot, nlogn_plot, median_test or slicing_test
    """
    plt.style.use('ggplot')
    plt.title('Complexity')
    for r in results:
        plt.plot(r['word'], r['step'], label=r['name'])
    plt.xlabel('Words')
    plt.ylabel('Steps')
    plt.legend()
    plt.show()


def nsquare_plot(plot_label=None):
    result = {}
    result['word'] = []
    result['step'] = []
    result['name'] = plot_label if plot_label != None else 'n**2'
    for t in tapes:
        result['word'].append(t)
        result['step'].append(t**2)

    return result


def nlogn_plot(plot_label=None):
    result = {}
    result['word'] = []
    result['step'] = []
    result['name'] = plot_label if plot_label != None else 'nlogn'
    for t in tapes:
        result['word'].append(t)
        result['step'].append(t * log2(t))

    return result


def median_test(name, median_label='A', plot_label=None):
    """Check the median
    print T as True and F as False with the lenght to validate the entry
    Parameters
    ----------
    name : str
        The name of the turing machine
    median_label : str (default is A)
         the label of the median
    plot_label : int, optional
        the label to plot after the test (default is None)
    """
    result = {}
    result['history'] = []
    result['word'] = []
    result['step'] = []
    result['validity'] = []
    result['name'] = plot_label if plot_label != None else name

    for t in tapes:
        tape = []
        for c in range(0, t):
            tape.append('X')
        process = subprocess.run(
            ['python', '-m', am_path, 'simulation', '-t',
                "".join(tape), '-n', name, '-r', file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        parser = parse_output(process.stdout)
        testRes = median_validation(parser['result'],
                                    median_label=median_label)
        print('T' if testRes else 'F', end='', flush=True)
        print('[' + str(t) + ']', end=' ', flush=True)
        result['word'].append(t)
        result['step'].append(parser['step'])
        result['validity'].append(testRes)
        result['history'].append((t, parser['step'], testRes))

    print()
    return result


def slicing_test(name, median_label='A', plot_label=None):
    """Test the slicing with a≤b≤c≤d≤a+1
    with a, b, c and d respectively 1, 2, 3 and 4

    print T as True and F as False with the lenght to validate the entry
    Parameters
    ----------
    name : str
        The name of the turing machine
    median_label : str (default is A)
         the label of the median
    plot_label : int, optional
        the label to plot after the test (default is None)
    """
    result = {}
    result['history'] = []
    result['word'] = []
    result['step'] = []
    result['validity'] = []
    result['name'] = plot_label if plot_label != None else name

    for t in tapes:
        tape = []
        for c in range(0, t):
            tape.append('X')
        process = subprocess.run(
            ['python', '-m', am_path, 'simulation', '-t',
                "".join(tape), '-n', name, '-r', file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        parser = parse_output(process.stdout)
        testRes = slicing_validation(
            parser['result'],
            median_label=median_label)
        print('T' if testRes else 'F', end='', flush=True)
        print('[' + str(t) + ']', end=' ', flush=True)
        result['word'].append(t)
        result['step'].append(parser['step'])
        result['validity'].append(testRes)
        result['history'].append((t, parser['step'], testRes))

    print()
    return result


if __name__ == "__main__":
    results = []

    # results.append(nsquare_plot())
    results.append(nlogn_plot())

    # results.append(median_test('E1', plot_label='E1 O(n**2)'))
    # results.append(median_test('E2.1', plot_label='E2.1 O(~n**2?)'))
    # results.append(median_test('E2.2', plot_label='E2.2 O(nlogn)'))

    results.append(slicing_test('E3.1', plot_label='E3.1 O(nlogn)'))

    plot_test(results)
