import os
from os.path import join as joinp
from sys import argv, exit
from collections import defaultdict
import re


BENCH_MARKER = "bench::"
BENCH_MARKER_TYPO = "bech::"

FN_CRYPTO_BENCH = "crypto_bench.txt"
FN_STACK_BENCH = "measure_stack.txt"
FN_GET_BENCH = "get_durations.txt"
FN_MAKE_BENCH = "make_durations.txt"



def list_subdirectories(directory):
    """List all subdirectories within a given directory recursively."""
    subdirs = []
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            subdirs.append(os.path.join(root, dir_name))
    return subdirs


def read_crypto_bench(fname):
    results = defaultdict(lambda: list())
    for line in open(fname).readlines():
        if line.startswith(BENCH_MARKER):
            key, value = line.strip().split(",")
            results[key].append(float(value))

    return dict(results)


def read_stack_bench(fname):
    results = defaultdict(lambda: list())
    for line in open(fname).readlines():
        if line.startswith(BENCH_MARKER) or line.startswith(BENCH_MARKER_TYPO):
            key, value = line.strip().split(",")

            if " size: " in value:
                value = value.replace(" size: ", "")
            
            # Fix typo
            if key == "bech::keygen_hybrid":
                key = "bench::keygen_hybrid"

            results[key].append(int(value, 0))

    return dict(results)


def read_duration_bench(fname, name):
    return {
        name: list(map(float, [x.strip().replace(",","") for x in open(fname).readlines()]))
    }

def extract_size_hashcalls(name):
    sigsize, hashcalls, _ = name.split("_", 2)

    return int(sigsize), int(float(hashcalls))


def avg(l):
    if type(l) in (int, float):
        return l
    return sum(l)/len(l)

def intify(data):
    return int(float(data))
def main():
    if len(argv) < 2:
        print(f"Error, use: {argv[0]} TARGET_DIR")
        exit(1)

    results = {}
    
    for dir in list_subdirectories(argv[1]):
        sigsize, hashcalls = extract_size_hashcalls(os.path.basename(dir))
        
        results[dir] = {
            "sigsize": sigsize,
            "hashcalls": hashcalls
        }
        
        try:
            results[dir].update(read_crypto_bench(joinp(dir, FN_CRYPTO_BENCH)))
        except FileNotFoundError:
            pass
        try:
            results[dir].update(read_stack_bench(joinp(dir, FN_STACK_BENCH)))
        except FileNotFoundError:
            pass
        
        try:
            results[dir].update(read_duration_bench(joinp(dir, FN_GET_BENCH), "bench::get"))
        except FileNotFoundError:
            pass
        try:
            results[dir].update(read_duration_bench(joinp(dir, FN_MAKE_BENCH), "bench::make"))
        except FileNotFoundError:
            pass
        

    for result in results:
        for bench in results[result]:
            results[result][bench] = avg(results[result][bench])
    
    # print as csv
    columns = {
        "sigsize": "sigsize",
        "hashcalls": "num_hashcalls",
        "bench::hybrid::SecKey::gensk_with_pk": "time_keygen",
        "bench::hybrid::SecKey::sign": "time_sign",
        "bench::keygen_hybrid": "stack_keygen",
        "bench::sign_hybrid": "stack_sign",
        "bench::get": "time_get",
        "bench::make": "time_make",
    }

    # print("name," + ",".join([columns[c] for c in columns]))
# (sigsize, speed, 0, sec, h,d,b,k,w, 0)
    rows = []
    for result in results:
        cleared_res = result.split("/")[-1]
        params = cleared_res.split("_")
        h, d, k, t = params[4], params[5], params[7], params[6]

        h = intify(h)
        d = intify(d)
        k = intify(k)
        t = intify(t)

        row = [
            results[result]["sigsize"],
            results[result]["hashcalls"],
            h,
            d,
            k,
            t,
            round(results[result]["bench::hybrid::SecKey::gensk_with_pk"], 1),
            "X",
            round(results[result]["bench::keygen_hybrid"] / 2**10, 1),
            round(results[result]["bench::hybrid::SecKey::sign"], 1),
            "X",
            round(results[result]["bench::sign_hybrid"] / 2**10, 1)
        ]
        rows.append(row)        

    rows = sorted(rows, key=lambda x: x[0])
    for row in rows:
        print("& ".join(map(str, row)) + "\\\\")
    


if __name__ == '__main__':
    main()
