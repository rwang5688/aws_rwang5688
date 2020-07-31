import sys

def main(argv):
    print('Hello, Sum!')
    print('The sum of 2 and 3 is 5.')
    sum = int(argv[1]) + int(argv[2])
    print('The sum of {0} and {1} is {2}.'.format(argv[1], argv[2], sum))

main(sys.argv)

