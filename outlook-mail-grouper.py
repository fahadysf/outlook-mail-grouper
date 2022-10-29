import argparse
from exchangelib import Credentials, Account

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--credentials',
                    help='Credentials file with username in first line and password in second line.')
parser.add_argument('-f', '--folder-name',
                    help='Folder to search (top level only)')
parser.add_argument('-p', '--similarity-percentage',
                    help='Percentage similarity required for subjects to be considered same group')
parser.add_argument('-a', '--action', help='Action to take')
args = vars(parser.parse_args())


def setup_config():
    try:
        with open(args['credentials'], 'r') as cfd:
            data = cfd.readlines()
            username = data[0].strip()
            password = data[1].strip()
            return {
                'username': username,
                'password': password,
                'args': args
            }
    except Exception:
        raise


if __name__ == '__main__':
    config = setup_config()
    credentials = Credentials(
        username=config['username'],
        password=config['password'])
    a = Account(config['username'],
                credentials=credentials,
                autodiscover=True)
    folder = a.inbox / 'Apple'
    for item in folder.all().order_by('-datetime_received')[:100]:
        print(
            f'{item.sender.name} <{item.sender.email_address}> | {item.subject} | {item.datetime_received}')
