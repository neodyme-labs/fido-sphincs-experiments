import sys
import os
from pathlib import Path
from subprocess import check_output

SPHINCS_DIR = "OpenSK/third_party/sphincsplus/ref/"
OPENSK_DIR = "OpenSK"

SPHINCS_PARAM_REL = "spx-few/parameters/current.txt"
SPHINCS_PARAM_TMP = SPHINCS_DIR + SPHINCS_PARAM_REL
RUN_DIR = os.getcwd()


def configure_header(param_file):
    os.chdir(SPHINCS_DIR)
    print(check_output(f"python3 test_params.py {param_file} --no-bench", shell=True))
    os.chdir(RUN_DIR)


def run_speed_bench(param_name, subfolder):
    os.system(f"bash scripts/run_speed.sh {param_name} {subfolder}")

def run_stack_bench(param_name, subfolder):
    os.system(f"bash scripts/run_stack.sh {param_name} {subfolder}")

def run_benchmark(param_name, subfolder):
    os.system(f"bash scripts/run_benchmark.sh {param_name} {subfolder}")


def main():
    if len(sys.argv) < 3:
        print(f"Call with: {sys.argv[0]} PARAMS_FILE RESULT_SUB_FOLDER")
        sys.exit(1)
    
    params_file = Path(sys.argv[1])
    if not params_file.is_file:
        print(f"{params_file.absolute()} is not a file.")
        sys.exit(2)
    
    for line in params_file.read_text().split("\n"):
        open(SPHINCS_PARAM_TMP, "w").write(line)
        configure_header(SPHINCS_PARAM_REL)
        subfolder = sys.argv[2]

        param_name = line.replace(" ", "_")

        run_speed_bench(param_name, subfolder)

#        run_stack_bench(param_name, subfolder)

        run_benchmark(param_name, subfolder)

        



if __name__ == "__main__":
    main()
