import argparse, time, datetime

DEFAULT_PATTERN = '%Y-%m-%d %H:%M:%S'
EPOCH = "epoch"
DATETIME = "datetime"

def datetimeToEpoch(datetimeString, pattern=DEFAULT_PATTERN):
    return int(time.mktime(time.strptime(datetimeString, pattern)))

def epochToDatetime(epochString, pattern=DEFAULT_PATTERN):
    return time.strftime(pattern, time.localtime(float(epochString)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", help="a datetime string pattern", required=False)


    action_parsers = parser.add_subparsers(dest="action")
    epoch_parser = action_parsers.add_parser("epoch", help="datetime to epoch command")
    epoch_parser.add_argument("-d", "--datetime", help="a datetime string", required=True)
    datetime_parser = action_parsers.add_parser("datetime", help="epoch to datetime command")
    datetime_parser.add_argument("-s", "--string", help="an epoch string", required=True)

    args = parser.parse_args()
    if args.action == EPOCH:
        func = datetimeToEpoch
        arg = args.datetime
    elif args.action == DATETIME:
        func = epochToDatetime
        arg = args.string
    if args.pattern:
        string = func(arg, args.pattern)
    else:
        string = func(arg)

    print(string)
