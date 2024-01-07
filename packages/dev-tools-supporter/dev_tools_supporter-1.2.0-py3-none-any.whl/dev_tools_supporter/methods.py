import time
import os
from datetime import datetime as dt


def sout(content, color='white', **kwargs):
    """
        This function redefines the print function of python, which allow you 
        to print line with particular color (red, green, yellow)

        Note that you just can see the file change in Normal Terminal (Git Bash does not work)
    """
    if 'filename' in kwargs:
        filename = kwargs.get('filename', '')
    else:
        filename = 'general'

    if 'verbose' in kwargs:
        if kwargs['verbose'] == False:
            return

    if 'end' in kwargs:
        kwargs['end'] = kwargs.get('end') + '\033[0m'
    else:
        kwargs['end'] = '\033[0m\n'

    if color == 'green':
        line_color = '\033[92m'
    elif color == 'red':
        line_color = '\033[91m'
    elif color == 'yellow':
        line_color = '\033[93m'
    elif color == 'blue':
        line_color = '\033[94m'
    elif color == 'magenta':
        line_color = '\033[95m'
    else:
        line_color = '\033[0m'

    # Remove kwargs['filename'] or kwargs['verbose] to avoid error
    if 'filename' in kwargs:
        del kwargs['filename']

    if 'verbose' in kwargs:
        del kwargs['verbose']

    print(f'{line_color}{content}', **kwargs)

    date_today = dt.now().strftime('%Y-%m-%d')

    os.makedirs(f'logs/{date_today}', exist_ok=True)

    with open(f'logs/{date_today}/{filename}_log.log', 'a', encoding='utf-8') as f:
        f.write(f'{content}\n')


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    print(f'\r{prefix} |{bar}| {percent}% | {iteration} over {total}', end=printEnd)

    if iteration == total:
        print()
