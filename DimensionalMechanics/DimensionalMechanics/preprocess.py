import os
import argparse


EXTENSIONS = dict(
    any=['avi', 'jpg', 'mp4', 'png', 'mpeg'],
    image=['jpg', 'png'],
    video=['avi', 'mpeg'],
    audio=['mp3']
    )

EXTR_IMBALANCE_THRESH = 0.20
SIG_TRUNC_THRESH = 0.20

Statistics = namedtuple('Statistics', 'classes, total, min, max')


def main():
    params = parse_command_line()
    data, errors = validate_data(params.root, params.type)
    stats = get_overall_statistics(data)
    check_extreme_imbalance(data, stats)
    omitted = balance_data(data, stats, params.balanceLevel)
    check_significant_truncation(data, stats, omitted)
    write_csv(data, params.root)
    write_statistics(data, omitted, params.root)
    write_error_log(errors, params.root)


def parse_command_line():
    p = argparse.ArgumentParser()
    p.add_argument('root', help='the absolute path to the root directory of your training data')
    p.add_argument('-t', '--type', choices=['any', 'image', 'video', 'audio'], default='any',
                   help='specify a type for training data')
    p.add_argument('-abl', '--autobalanceLevel', default=0.0, type=float,
                   help='provide a maximum allowed percent difference from perfectly balanced')
    args = p.parse_args()
    try:
        validate_input_params(args)
    except Exception as e:
        print('input error: {0}'.format(e))
    return args


def validate_input_params(args):
    if not os.path.isdir(args.root):
        raise ValueError('root is not a directory')


def validate_data(root_path, type):
    data = {}
    errors = []
    with os.scandir(root_path) as itr:
        for entry in itr:
            if entry.is_dir():
                data[entry.name] = []
    for c in data.keys():
        with os.scandir(os.path.join(root_path, c)) as itr:
            for entry in itr:
                #existence
                if not entry.is_file():
                    errors.append((entry.path, 'path is not a file'))
                    continue
                #accessibility
                if not os.access(entry.path, os.R_OK):
                    errors.append((path, 'file is inaccessible'))
                #file size is greater than 0
                elif entry.stat().st_size == 0:
                    errors.append((entry.path, 'file size is zero'))
                #file type matches expected
                elif os.path.splitext(entry.path)[1][1:].lower() not in EXTENSIONS[type]:
                    errors.append((entry.path, 'wrong file type'))
                #file valid if control reaches here
                else:
                    data[c].append(entry.path)
    return data, errors


def get_overall_statistics(data):
    total = 0
    min = -1
    max = -1
    for c in data.keys():
        x = len(data[c])
        total += x
        if min == -1 or x < min:
            min = x
        if max == -1 or x > max:
            max = x
    return Statistics(len(data.keys()), total, min, max)


def display_overall_statistics(data, stats):



def get_continue_boolean():
    prompt = 'Do you wish to continue anyway? (y/n)'
    while True:
        try:
            return {'y':True, 'n':False}[input(prompt).lower()]
        except ValueError:
            print('invalid input')


def check_extreme_imbalance(data, stats):
    pd = percent_difference(stats.min, stats.max)
    if pd > EXTR_IMBALANCE_THRESH:
        print('WARNING: Highly imbalanced data detected.')
        print('There is a {0:.2f}% difference between the largest and smallest classifications.'.format(pd*100))
        display_overall_statistics(data, stats)
        print('This may cause a significant bias in the resultant model.')
        if not get_continue_boolean():
            exit()


def balance_data(data, stats, level):
    max = int(ceil((1 + 2*level) * stats.min))
    omitted = {}
    for c in data.keys():
        omitted[c] = []
        while len(data[c]) > max:
            omitted[c].append(data[c].pop())
    return omitted


def check_significant_truncation(data, stats, omitted):
    prop = len(omitted) / stats.total
    if prop < (1 - SIG_TRUNC_THRESH):
        print('WARNING: A significant amount of provided data will be omitted from the training dataset.')
        print('Only {0:.2f}% of provided data will be included for training.'.format(prop*100))
        display_overall_statistics(data, stats)
        print('This may produce unexpected results in the final model.')
        if not get_continue_boolean():
            exit()
    

def write_csv(data, save_loc):
    with open(os.path.join(save_loc, 'test.csv'), 'w+') as of:
        for label, c in enumerate(data.keys()):
            for path in data[c]:
                of.write(path + ',' + str(label) + '\n')


def write_statistics(data, omitted, save_loc):
    with open(os.path.join(save_loc, 'stats.txt'), 'w+') as of:
        of.write('Class Name\tLabel\tNum Files\n')
        total = 0
        for label, c in enumerate(data.keys()):
            num_files = len(data[c])
            total += num_files
            of.write(c + '\t\t' + str(label) + '\t' + str(num_files) + '\n')
        of.write('\nTotal Files: ' + str(total) + '\n')
        if omitted:
            of.write('\nOmitted Files:\n')
            for path in omitted:
                of.write(path + '\n')


def write_error_log(errors, save_loc):
    with open(os.path.join(save_loc, 'errors.txt'), 'w+') as of:
        of.write('Path\t\t\t\t\t\t\t\tError\n')
        for path, er in errors:
            of.write(path + '\t\t' + er + '\n')


def percent_difference(x, y):
    average = (x + y) / 2
    return (x - y) / average


if __name__ == '__main__':
    main()