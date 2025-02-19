# FIDO SPHINCS+ Experiments

This is the meta repository for the code accompanying the paper `Stateless Hash-Based Signatures for Post-Quantum Security Keys`.
It ties together all scripts and code needed to reproduce the results.

## Structure
The relevant code is distributed amongst four repositories:

- [sphincsplus](https://github.com/rugo/sphincsplus-experiments) - The SPHINCS+ C code, with a tool instantiate and test different parameter sets.
- [sphincs_wrapper](https://github.com/rugo/sphincs_wrapper) - The Rust wrapper for SPHINCS+
- [OpenSK](https://github.com/rugo/OpenSK) - OpenSK modified to use Sphincs
- [FIDO SPHINCS+ Experiments](https://github.com/rugo/fido-sphincs-experiments) - This meta repository with benchmarking scripts

The dependencies are included as submodules.

## Reproduce

### 1. Repository and Software
Clone the repo with all submodules:

```
git clone --recurse-submodules https://github.com/rugo/fido-sphincs-experiments
```

You need the JLink software for the speed and stack benchmarks.
A recent Python version is needed for the helper scripts.

### 2. Hardware
To reproduce the results of the paper, you need an nRF52840 development kit.
Connect both USB cables to a host computer.

### 3. Parameter file
The parameter file needs to have one SPHINCS+ parameter set per line.
Each line needs to contain the following, space separated values:

1. Signature size: Given in bytes and rows are sorted by this ascending.
2. Signing speed: Number of hash calls for signing. The search is limited to < 10^9 calls, which corresponds to roughly < 1 min signing on a modern CPU.
3. Verification speed: Number of hash calls for verification.
4. Probability for FORS forgery after 2^y signatures.
5. The parameter h in SPHINCS+.
6. The parameter d in SPHINCS+.
7. The parameter b in SPHINCS+.
8. The parameter k in SPHINCS+.
9. The parameter w in SPHINCS+.
10. Security degradation: The value `z` such that after 2^z signatures, the forgery probability is still < 2^{-112, -128, -192} (for a security target of 128, 192, 256 bits)

Although (3) and (10) are not used by the tooling. This format is compatible to the one used [here](https://github.com/kste/spx-few/).
`
### 4. Benchmarking
Run the [run_benchmark.py](run_benchmark.py) script with a parameter file of your choice.

Like so:

```
python3 run_benchmarks.py params/128_10.txt 10-sig
```

The results will be stored in the `results/10-sig` folder.

Unfortunately you have to press the board's reset button before the FIDO HID benchmark (make/get) starts. Do so once the script says "Configuring device". This is not needed for the stack and speed benchmarks.

### 5. Pretty Printing
To export the results into one file, use the [print_results.py](print_results.py) script on the result folder:

```
p3 print_results.py results/10-sig
```

This will output a csv file.
