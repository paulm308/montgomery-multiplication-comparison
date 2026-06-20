import argparse
import math


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='some_script.py', description='TODO')

    parser.add_argument('a', type=int, help='first multiplicand')
    parser.add_argument('b', type=int, help='second multiplicand')
    parser.add_argument('n', type=int, help='modulus')
    parser.add_argument('-w', '--wordsize', type=int, help='wordlength in bits')
    parser.add_argument('-v', '--verbose', action="store_true", help='enable extra output')
    parser.add_argument('-c', '--convert', action="store_true", help='convert into montgomery representation')

    args = parser.parse_args()

    a = args.a
    b = args.b
    w = 3
    if args.wordsize:
        w = args.wordsize
    n = args.n

    bits_n = n.bit_length()
    s = math.ceil(bits_n / w)
    r = 2 ** (s * w)
    r_inv = pow(r, -1, n)
    res = (a * b * r_inv) % n

    if args.verbose:
        print(f"s: {s}, r: {r}, r_inv: {r_inv}")

    if args.convert:
        print(f"a': {(a * r) % n}, b': {(b * r) % n}")
    else:
        print(res)
