import argparse
import random
import time
from tqdm import tqdm


def convert_to_array(num: int, wordsize: int, s: int) -> list[int]:
    '''
    Converts a decimal number to a binary number that is split in to words.
    Each binary word is then converted back to decimal.

    :param num: decimal number to be converted
    :type num: int
    :param wordsize: length of the bitstring of a single word
    :type wordsize: int
    :param s: amount of words in the modulus n
    :type s: int
    :return: converted array
    :rtype: list[int]

    >>> convert_to_array(17, 2, 3)
    [1, 0, 1]
    >>> convert_to_array(17, 2, 4)
    [1, 0, 1, 0]
    >>> convert_to_array(17, 3, 3)
    [1, 2, 0]
    '''
    bin_str = bin(num)[2:]
    padding = (-len(bin_str)) % wordsize
    bin_str = "0" * padding + bin_str
    res_withoud_padding = [int(bin_str[i:i + wordsize], 2) for i in range(0, len(bin_str), wordsize)][::-1]
    if s != 0:
        return res_withoud_padding + [0 for i in range(s - len(res_withoud_padding))]
    return res_withoud_padding


def array_to_int(arr: list[int], wordsize: int) -> int:
    '''
    Converts the array generated in convert_to_array back to a decimal number.

    :param arr: number in array form
    :type arr: list[int]
    :param wordsize: length of the bitstring of a single word
    :type wordsize: int
    :return: converted decimal number
    :rtype: int
    >>> array_to_int([1, 0, 1], 2)
    17
    >>> array_to_int([1, 0, 1, 0], 2)
    17
    >>> array_to_int([1, 2, 0], 3)
    17
    '''
    bin_str = "".join(format(w, f"0{wordsize}b") for w in arr[::-1])
    return int(bin_str, 2)


def compute_n0_prime(n: list[int], wordsize: int) -> int:
    w = 1 << wordsize
    return (-pow(n[0], -1, w)) & (w - 1)


def add(num: list[int], idx: int, wordsize: int, c: int):
    base = 1 << wordsize
    i = idx
    while c != 0:
        if i >= len(num):
            num.append(0)
        tmp = num[i] + c
        num[i] = tmp & (base - 1)
        c = tmp >> wordsize
        i += 1


def sub(u: list[int], n: list[int], verbose: bool, extra: bool) -> list[int]:
    s = len(n)
    t = [0] * (s + 1)
    if verbose or extra:
        print(f"u: {u[::-1]}\nfinal substraction:\nt': {t}")

    B = 0
    for i in range(s):
        x = u[i] - n[i] - B
        if x < 0:
            x += w
            B = 1
        else:
            B = 0
        t[i] = x
        if extra:
            print(f"t': {t[::-1]}, B: {B}")
        elif verbose:
            print(f"t': {t[::-1]}")
    x = u[s] - B
    if x < 0:
        x += w
        B = 1
    else:
        B = 0
    t[s] = x
    if extra:
        print(f"t': {t[::-1]} B: {B}")
    elif verbose:
        print(f"t': {t[::-1]}")
    if B == 0:
        if verbose or extra:
            print(f"-> {t[:s][::-1]}")
        return t[:s]
    else:
        if verbose or extra:
            print(f"-> {u[:s][::-1]}")
        return u[:s]


def sos(a: list[int], b: list[int], n: list[int], wordsize: int, n0_prime: int, verbose: bool, extra: bool) -> list[int]:
    w = 1 << wordsize
    s = len(n)
    t = [0] * (2 * s + 1)
    if extra:
        print(f"a: {a[::-1]}, b: {b[::-1]}, n: {n[::-1]}, wordsize: {wordsize}, n0_prime: {n0_prime}, w: {w}, s: {s}")

    if verbose or extra:
        print(f"multiplication:\nt: {t}")
    for i in range(s):
        c = 0
        for j in range(s):
            tmp = t[i + j] + a[j] * b[i] + c
            t[i + j] = tmp & (w - 1)
            c = tmp >> wordsize
            if extra:
                print(f"t: {t[::-1]}, S: {t[i + j]}, C: {c}")
        t[i + s] = c
        if verbose or extra:
            print(f"t: {t[::-1]}")

    if verbose or extra:
        print("reduction:")
    for i in range(s):
        c = 0
        m = (t[i] * n0_prime) & (w - 1)
        if extra:
            print(f"t: {t[::-1]}, m: {m}")
        elif verbose:
            print(f"t: {t[::-1]}")
        for j in range(s):
            tmp = t[i + j] + m * n[j] + c
            t[i + j] = tmp & (w - 1)
            c = tmp >> wordsize
            if extra:
                print(f"t: {t[::-1]}, S: {t[i + j]}, C: {c}")
        add(t, i + s, wordsize, c)

    if verbose or extra:
        print(f"t: {t[::-1]}")
    u = t[s:]

    return sub(u, n, verbose, extra)


def cios(a: list[int], b: list[int], n: list[int], wordsize: int, n0_prime: int, verbose: bool, extra: bool) -> list[int]:
    w = 1 << wordsize
    s = len(n)
    t = [0] * (s + 2)
    if extra:
        print(f"a: {a[::-1]}, b: {b[::-1]}, n: {n[::-1]}, wordsize: {wordsize}, n0_prime: {n0_prime}, w: {w}, s: {s}")
    elif verbose:
        print(f"t: {t}")
    for i in range(s):
        if verbose or extra:
            print("multiplication:")
        c = 0
        for j in range(s):
            tmp = t[j] + a[j] * b[i] + c
            t[j] = tmp & (w - 1)
            c = tmp >> wordsize
            if extra:
                print(f"t: {t[::-1]}, S: {t[j]}, C: {c}")
        tmp = t[s] + c
        t[s] = tmp & (w - 1)
        t[s + 1] = tmp >> wordsize
        if extra:
            print(f"t: {t[::-1]}, S: {t[s]}, C: {t[s + 1]}\nreduction:")
        elif verbose:
            print(f"t: {t[::-1]}\nreduction:")

        c = 0
        m = (t[0] * n0_prime) & (w - 1)
        tmp = t[0] + m * n[0]
        c = tmp >> wordsize
        if extra:
            print(f"t: {t[::-1]}, m: {m}, C: {c}")
        for j in range(1, s):
            tmp = t[j] + m * n[j] + c
            t[j - 1] = tmp & (w - 1)
            c = tmp >> wordsize
            if extra:
                print(f"t: {t[::-1]}, S: {t[j - 1]}, C: {c}")
        tmp = t[s] + c
        t[s - 1] = tmp & (w - 1)
        c = tmp >> wordsize
        t[s] = t[s + 1] + c
        if extra:
            print(f"t: {t[::-1]}, S: {t[s - 1]}, C: {c}")
        elif verbose:
            print(f"t: {t[::-1]}")

    u = t[:(s + 1)]

    return sub(u, n, verbose, extra)


def fios(a: list[int], b: list[int], n: list[int], wordsize: int, n0_prime: int, verbose: bool, extra: bool) -> list[int]:
    w = 1 << wordsize
    s = len(n)
    t = [0] * (s + 2)
    if extra:
        print(f"a: {a[::-1]}, b: {b[::-1]}, n: {n[::-1]}, wordsize: {wordsize}, n0_prime: {n0_prime}, w: {w}, s: {s}")
    elif verbose:
        print(f"t: {t}")

    for i in range(s):
        tmp = t[0] + a[0] * b[i]
        S = tmp & (w - 1)
        c = tmp >> wordsize
        add(t, 1, wordsize, c)
        if extra:
            print(f"t: {t}, S: {S}, C: {c}")
        elif verbose:
            print(f"t: {t}")
        m = S * n0_prime & (w - 1)
        tmp = S + m * n[0]
        c = tmp >> wordsize
        if extra:
            print(f"m: {m}, C: {c}")
        elif verbose:
            print(f"m: {m}")
        for j in range(1, s):
            tmp = t[j] + a[j] * b[i] + c
            S = tmp & (w - 1)
            c = tmp >> wordsize
            add(t, j + 1, wordsize, c)
            if extra:
                print(f"1. t: {t}, S: {S}, C: {c}")
            tmp = S + m * n[j]
            c = tmp >> wordsize
            t[j - 1] = tmp & (w - 1)
            if extra:
                print(f"2. t: {t}, S: {S}, C: {c}")
        tmp = t[s] + c
        c = tmp >> wordsize
        t[s - 1] = tmp & (w - 1)
        t[s] = t[s + 1] + c
        t[s + 1] = 0
        if extra:
            print(f"t: {t}, S: {t[s - 1]}, C: {c}")
        elif verbose:
            print(f"t: {t}")

    return sub(t, n, verbose, extra)


def fips(a: list[int], b: list[int], n: list[int], wordsize: int, n0_prime: int, verbose: bool, extra: bool) -> list[int]:
    w = 1 << wordsize
    s = len(n)
    assert s < w
    t = [0] * 3
    m = [0] * s

    for i in range(s):
        for j in range(i):
            tmp = t[0] + a[j] * b[i - j]
            S = tmp & (w - 1)
            c = tmp >> wordsize
            add(t, 1, wordsize, c)
            tmp = S + m[j] * n[i - j]
            t[0] = tmp & (w - 1)
            c = tmp >> wordsize
            add(t, 1, wordsize, c)
        tmp = t[0] + a[i] * b[0]
        S = tmp & (w - 1)
        c = tmp >> wordsize
        add(t, 1, wordsize, c)
        m[i] = S * n0_prime & (w - 1)
        tmp = S + m[i] * n[0]
        S = tmp & (w - 1)
        c = tmp >> wordsize
        add(t, 1, wordsize, c)
        t[0] = t[1]
        t[1] = t[2]
        t[2] = 0

    for i in range(s, 2 * s):
        for j in range(i - s + 1, s):
            tmp = t[0] + a[j] * b[i - j]
            S = tmp & (w - 1)
            c = tmp >> wordsize
            add(t, 1, wordsize, c)
            tmp = S + m[j] * n[i - j]
            t[0] = tmp & (w - 1)
            c = tmp >> wordsize
            add(t, 1, wordsize, c)
        m[i - s] = t[0]
        t[0] = t[1]
        t[1] = t[2]
        t[2] = 0

    return m


def cihs(a: list[int], b: list[int], n: list[int], wordsize: int, n0_prime: int, verbose: bool, extra: bool) -> list[int]:
    w = 1 << wordsize
    s = len(n)
    t = [0] * (s + 2)

    for i in range(s):
        c = 0
        for j in range(s - i):
            tmp = t[i + j] + a[j] * b[i] + c
            c = tmp >> wordsize
            t[i + j] = tmp & (w - 1)
        tmp = t[s] + c
        t[s] = tmp & (w - 1)
        t[s + 1] = tmp >> wordsize

    for i in range(s):
        m = t[0] * n0_prime & (w - 1)
        tmp = t[0] + m * n[0]
        c = tmp >> wordsize
        for j in range(1, s):
            tmp = t[j] + m * n[j] + c
            c = tmp >> wordsize
            t[j - 1] = tmp & (w - 1)
        tmp = t[s] + c
        c = tmp >> wordsize
        t[s - 1] = tmp & (w - 1)
        t[s] = t[s + 1] + c
        t[s + 1] = 0

        for j in range(i + 1, s):
            tmp = t[s - 1] + b[j] * a[s - j + i]
            c2 = tmp >> wordsize
            t[s - 1] = tmp & (w - 1)
            tmp = t[s] + c2
            t[s] = tmp & (w - 1)
            t[s + 1] = tmp >> wordsize

    return sub(t, n, verbose, extra)


def modexp(a: int, e: int, n: int) -> int:
    x = 1
    a = a % n
    while e > 0:
        if e & 1:
            x = (x * a) % n
        a = (a * a) % n
        e >>= 1
    return x


def montgomery_modexp(a: int, e: int, n: int) -> int:
    wordsize = 64
    na = convert_to_array(n, wordsize, 0)
    s = len(na)
    r = 2 ** (wordsize * s)
    a_mont = a * r % n
    aa = convert_to_array(a_mont, wordsize, s)
    x_mont = r % n
    xa = convert_to_array(x_mont, wordsize, s)
    n0_prime = compute_n0_prime(na, wordsize)
    one = [1] + [0] * (s - 1)

    while e > 0:
        xa = cios(xa, xa, na, wordsize, n0_prime, False, False)
        if e & 1:
            xa = cios(xa, aa, na, wordsize, n0_prime, False, False)
        e >>= 1
    return array_to_int(cios(xa, one, na, wordsize, n0_prime, False, False), wordsize)


def benchmark(epochs: int):
    times = [[0.0] * 5 for _ in range(4)]
    for i in range(4):

        for _ in tqdm(range(epochs)):
            a, b, n = sorted([random.getrandbits((i + 1) * 512) for j in range(3)])
            a = convert_to_array(a, 64, (i + 1) * 8)
            b = convert_to_array(b, 64, (i + 1) * 8)
            n = convert_to_array(n, 64, (i + 1) * 8)
            if (n[0] & 1) == 0:
                n[0] |= 1
            n0_prime = compute_n0_prime(n, 64)

            start_time = time.time()
            _ = sos(a, b, n, 64, n0_prime, False, False)
            times[i][0] += time.time() - start_time

            start_time = time.time()
            _ = cios(a, b, n, 64, n0_prime, False, False)
            times[i][1] += time.time() - start_time

            start_time = time.time()
            _ = fios(a, b, n, 64, n0_prime, False, False)
            times[i][2] += time.time() - start_time

            start_time = time.time()
            _ = fips(a, b, n, 64, n0_prime, False, False)
            times[i][3] += time.time() - start_time

            start_time = time.time()
            _ = cihs(a, b, n, 64, n0_prime, False, False)
            times[i][4] += time.time() - start_time

    avg_times = [[times[j][i] / epochs * 1000 for i in range(len(times[j]))] for j in range(len(times))]

    methods = ["SOS", "CIOS", "FIOS", "FIPS", "CIHS"]
    print("\t512bit: \t1024bit:\t1536bit:\t2048bit:")
    for i in range(5):
        print(f"{methods[i]}:\t{avg_times[0][i]:.3f}ms \t{avg_times[1][i]:.3f}ms \t{avg_times[2][i]:.3f}ms \t{avg_times[3][i]:.3f}ms")


def benchmark_modexp(epochs: int, bits: int):
    time_regular = 0.0
    time_montgomery = 0.0
    for _ in tqdm(range(epochs)):
        a, e, n = sorted([random.getrandbits(bits) for j in range(3)])
        if (n & 1) == 0:
            n |= 1

        start_time = time.time()
        _ = modexp(a, e, n)
        time_regular += time.time() - start_time

        start_time = time.time()
        _ = montgomery_modexp(a, e, n)
        time_montgomery += time.time() - start_time

    avg_time_regular = time_regular / epochs
    avg_time_montgomery = time_montgomery / epochs

    print(f"Regular Modular Exponentiation:\t{avg_time_regular:.5f}s\n Montgomery Modular Exponentiation:\t{avg_time_montgomery:.5f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='some_script.py', description='TODO')
    group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument("a", type=int, help="first number")
    parser.add_argument("b", type=int, help="second number")
    parser.add_argument("n", type=int, help="modul")
    parser.add_argument("w", type=int, help="word size")
    parser.add_argument('-v', '--verbose', action="store_true", help='enable extra output')
    parser.add_argument('-e', '--extra', action="store_true", help='enable extra extra output')
    group.add_argument('--sos', action="store_true", help='use the Separated Operand Scannig Method')
    group.add_argument('--cios', action="store_true", help='use the Coarsley Integrated Operand Scanning')
    group.add_argument('--fios', action="store_true", help='use the Finely Integrated Operand Scanning')
    group.add_argument('--fips', action="store_true", help='use the Finely Integrated Product Scanning')
    group.add_argument('--cihs', action="store_true", help='use the Coarsley Integrated Hybrid Scanning')
    group.add_argument('-b', '--benchmark', action="store_true",
                       help='prints the avg executiontime over e epochs for different bit lengths of a, b and n for each implementation of Montgomery modulo multiplivation')
    group.add_argument('--modexpbench', action="store_true", help='prints the avg executiontime over e epochs for bits bit lengths of a, e and n for the two versions of modular exponentiation')
    parser.add_argument('--epochs', type=int, help='amount of time messuring epochs in the benchmark function')
    parser.add_argument('--bits', type=int, help='number of bits to generate a, e and n for the modular exponentiation benchmark')
    args = parser.parse_args()

    verbose = False
    if args.verbose:
        verbose = True

    extra = False
    if args.extra:
        extra = True

    w = args.w
    n = convert_to_array(args.n, w, 0)
    a = convert_to_array(args.a, w, len(n))
    b = convert_to_array(args.b, w, len(n))
    r = 2 ** (w * len(n))
    n0_prime = compute_n0_prime(n, w)

    epochs = 1
    if args.epochs and args.epochs > 1:
        epochs = args.epochs

    bits = 512
    if args.bits and args.bits > 1:
        bits = args.bits

    if args.sos:
        print(f"-> {array_to_int(sos(a, b, n, w, n0_prime, verbose, extra), w)}")

    elif args.cios:
        print(f"-> {array_to_int(cios(a, b, n, w, n0_prime, verbose, extra), w)}")

    elif args.fios:
        print(f"-> {array_to_int(fios(a, b, n, w, n0_prime, verbose, extra), w)}")

    elif args.fips:
        print(f"-> {array_to_int(fips(a, b, n, w, n0_prime, verbose, extra), w)}")

    elif args.cihs:
        print(f"-> {array_to_int(cihs(a, b, n, w, n0_prime, verbose, extra), w)}")

    elif args.benchmark:
        benchmark(epochs)

    elif args.modexpbench:
        benchmark_modexp(epochs, bits)
