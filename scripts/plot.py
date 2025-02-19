import matplotlib.pyplot as plt
import numpy as np
from sys import argv


def extract_data(data):
    siglen = []
    nhashes = []
    print(data)
    print("huso")
    for d in data.split("\n"):
        if not d:
            continue
        vals = d.split(" ")
        siglen.append(int(float(vals[0])))
        nhashes.append(int(float(vals[1]))/1000)
    
    return nhashes, siglen

# Number of points per category
num_points = 20

# Generate random data within the specified ranges
num_hashes_128, signature_size_128 = extract_data(open(argv[1]).read())

num_hashes_192, signature_size_192 = extract_data(open(argv[2]).read())

num_hashes_256, signature_size_256 = extract_data(open(argv[3]).read())

# num_hashes_x, signature_size_x = extract_data(open(argv[4]).read())

# Create scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(num_hashes_128, signature_size_128, color='blue', marker='x', label='$q = 2^8$')
plt.scatter(num_hashes_192, signature_size_192, color='green', marker='s', label='$q = 2^{10}$')
plt.scatter(num_hashes_256, signature_size_256, color='red', marker='d', label='$q = 2^{16}$')
# plt.scatter(num_hashes_x, signature_size_x, color='red', marker='d', label='x-bit')
plt.axhline(y=15161, color='black', linestyle='-', linewidth=1)
plt.text(400, 15161, "Aligned CTAP USB HID Message Limit", verticalalignment='bottom', fontsize=14, color='black')
# Labels and title with larger font size
plt.xlabel("Hash Computations ($10^3$)", fontsize=16)
plt.ylabel("Signature size (bytes)", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=16, loc='upper left', frameon=True, edgecolor='black', bbox_to_anchor=(1.05, 1))
plt.grid(True, linestyle='--', alpha=0.6)

# Save the figure for a scientific paper
plt.savefig("scatter_plot.pdf", dpi=900, bbox_inches='tight')

# Show plot
# plt.show()

