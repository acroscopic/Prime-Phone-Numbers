"""
Prime Phone Numbers
This program generates valid phone numbers and checks if they are prime.
If the numbers are prime, it will save them in a .dat file.
We are only checking numbers with country code: +1
"""

"""
North American Numbering Plan (NANP)

For a phone number: NPA-NXX-XXXX

NPA = [2-9][0-9][0-9]
NXX = [2-9][0-9][0-9]
NXX ≠ {211,311,411,511,611,711,811,911}
XXXX = [0-9][0-9][0-9][0-9]
"""

import json
from multiprocessing import Pool, cpu_count


# ------------------------------------------------------------
# Import all of the area codes
# ------------------------------------------------------------

with open("area_codes.json", "r") as f:
    codes = set(json.load(f))

# Reserved N11 exchange codes
reservedN11 = set([211, 311, 411, 511, 611, 711, 811, 911])


# ------------------------------------------------------------
# Deterministic Miller-Rabin primality test
# Valid for all 10-digit integers
# ------------------------------------------------------------

def is_prime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 5 == 0:
        return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # https://en.wikipedia.org/wiki/Strong_pseudoprime
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            return True
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        skip = False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                skip = True
                break
        if not skip:
            return False

    return True


# ------------------------------------------------------------
# Check if number is valid prime phone number
# ------------------------------------------------------------

def valid_prime_phone(n):

    # Remove numbers divisible by 2 or 5 (cheap safety)
    if n % 2 == 0 or n % 5 == 0:
        return None

    # Extract Area Code (first 3 digits)
    npa = n // 10000000

    # Extract Exchange Code (digits 4–6)
    nxx = (n % 10000000) // 10000

    # Area code must match list
    if npa not in codes:
        return None

    # Exchange must start with digit 2–9
    if nxx < 200:
        return None

    # Exchange must not be reserved
    if nxx in reservedN11:
        return None

    # Final primality check
    if is_prime(n):
        return n

    return None


# ------------------------------------------------------------
# Main execution
# ------------------------------------------------------------

def main():

    print("Generating and filtering valid prime phone numbers...")

    minimum = 2010000000
    maximum = 9899999999

    processes = cpu_count()
    print("Using {} CPU cores".format(processes))

    chunk_size = 1000000

    with open("primes.dat", "w") as outfile:
        pool = Pool(processes)

        for start in range(minimum, maximum + 1, chunk_size):
            end = min(start + chunk_size, maximum + 1)

            numbers = range(start, end)

            results = pool.map(valid_prime_phone, numbers)

            for r in results:
                if r is not None:
                    outfile.write(str(r) + "\n")

            print("Processed up to {}".format(end))

        pool.close()
        pool.join()

    print("Done! Output written to primes.dat")


if __name__ == "__main__":
    main()
