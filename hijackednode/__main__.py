from argparse import ArgumentParser

from . import main

parser = ArgumentParser(description='Hijacked-Node\'s CLI')

parser.add_argument('pull', help='Pull messages from configured targets and exit', action='store_true')
parser.add_argument('debug', help='TODO: Implement this feature', action='store_true')
parser.add_argument('server', help='postgresql database TODO', type=str, default='localhost')
parser.add_argument('user', help='database\'s user TODO', type=str, default='postgre')
parser.add_argument('pass', help='user\'s password TODO', type=str, default='postgre')


def pcla() -> bool:
	return (parser.parse_args())


if __name__=='__main__':
	main(cla=pcla())
