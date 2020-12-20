from argparse import ArgumentParser

from . import main

parser = ArgumentParser(description=̈́'Hijacked-Node\'s CLI')

parser.add('pull', help='Pull messages from configured targets and exit', type=bool, action='store_true')
parser.add('debug', help='TODO: Implement this feature', type=bool, action='store_true')
parser.add('server' help='postgresql database TODO' type=str, default='localhost')
parser.add('user' help='database\'s user TODO' type=str, default='postgre')
parser.add('pass' help='user\'s password TODO' type=str, default='postgre')


def pcla() -> bool:
	return (parser.parse_args())


if __name__=='__main__':
	main(cla=pcla())
