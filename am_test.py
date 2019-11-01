# V1.0 2019/11/01 Jason Haenlin

import re
import subprocess
from math import floor, log2

import matplotlib.pyplot as plt
import numpy as np

am_path = 'am'
file = 'minip1.txt'
tapes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
         15, 16, 17, 18, 19, 20, 40, 80, 160, 320, 640,
         1280, 2560, 5120, 10240, 20480]


def median_validation(result_tape, median_label='A'):
    '''get the position of the median and compare with the result tape'''
    result_tape = list("".join(re.split('<|>|_', result_tape)))
    median_pos = floor(len(result_tape)/2) - \
        (0 if len(result_tape) % 2 == 1 else 1)
    return True if result_tape[median_pos] == median_label else False


def slicing_validation(result_tape, median_label='A', log=False):
    '''build the slicing world and compare with the result tape'''
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


def parseOutput(output):
    parser = {
        'result': output.split(' ')[0].split('\n')[2],
        'step': int(output.split(' ')[2])
    }
    return parser


def plotTest(results):
    plt.style.use('ggplot')
    plt.title('Complexity')
    for r in results:
        plt.plot(r['word'], r['step'], label=r['name'])
    plt.xlabel('Words')
    plt.ylabel('Steps')
    plt.legend()
    plt.show()


def nsquarePlot(plot_label=None):
    result = {}
    result['word'] = []
    result['step'] = []
    result['name'] = plot_label if plot_label != None else 'n**2'
    for t in tapes:
        result['word'].append(t)
        result['step'].append(t**2)

    return result


def nlognPlot(plot_label=None):
    result = {}
    result['word'] = []
    result['step'] = []
    result['name'] = plot_label if plot_label != None else 'nlogn'
    for t in tapes:
        result['word'].append(t)
        result['step'].append(t * log2(t))

    return result


def MedianTest(name, median_label='A', plot_label=None):
    '''Check the median'''
    '''print T as True and F as False with the lenght to validate the entry'''
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
        parser = parseOutput(process.stdout)
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


def slicingTest(name, median_label='A', plot_label=None):
    '''Test the slicing with a≤b≤c≤d≤a+1'''
    '''respectively 1, 2, 3 and 4'''
    '''print T as True and F as False with the lenght to validate the entry'''
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
        parser = parseOutput(process.stdout)
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

    # results.append(nsquarePlot())
    results.append(nlognPlot())

    # results.append(MedianTest('E1', plot_label='E1 O(n**2)'))
    # results.append(MedianTest('E2.1', plot_label='E2.1 O(~n**2?)'))
    results.append(MedianTest('E2.2', plot_label='E2.2 O(nlogn)'))

    results.append(slicingTest('E3.1', median_label='Y',
                               plot_label='E3.1 O(nlogn)'))

    plotTest(results)
