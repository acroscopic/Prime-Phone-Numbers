# Prime Phone Numbers

Generates every valid North American phone number and filters for primes. The data is outputted to a binary `.dat` file and includes 162587428 numbers at ~1.7 GB.

Primality is checked using a deterministic Miller-Rabin test proven sufficient for all integers up to 3.3 × 10²⁴, making it exact for this domain.

## How It Works

Valid phone numbers follow the **North American Numbering Plan (NANP)** for country code `+1`:

```
+1  NPA - NXX - XXXX
```

| Segment | Constraint |
|---|---|
| `NPA` (area code) | Must be a real, active NANP area code |
| `NXX` (exchange) | First digit 2–9; not a reserved N11 code |
| `XXXX` (subscriber) | 0000–9999 |

Reserved N11 exchange codes (`211, 311, 411, 511, 611, 711, 811, 911`) are excluded. The search space runs from `2,010,000,000` to `9,899,999,999`.

## Primality Test

The Miller-Rabin implementation uses the witness set `{2, 325, 9375, 28178, 450775, 9780504, 1795265022}`, which is deterministic for all `n < 3,317,044,064,679,887,385,961,981`. 
Using this set allows us to have no probabilistic false positives.

## Files

| File | Description |
|---|---|
| `prime_phone_numbers.py` | Main script — generates and filters prime phone numbers |
| `area_code_scraper.py` | Scrapes valid NANP area codes |
| `area_code_builder.py` | Builds `area_codes.json` from scraped data |
| `area_codes.json` | Set of active NANP area codes (auto-generated) |
| `primes.dat` | Output — one prime phone number per line, approximately 1.7 GB |

## Usage

**1. Generate `area_codes.json`** (if not already present):
```bash
python area_code_scraper.py
python area_code_builder.py
```

**2. Run the main script:**
```bash
python prime_phone_numbers.py
```

Results are written to `primes.dat`, one number per line, as 10-digit integers.

## Performance

The script uses Python's `multiprocessing.Pool` and scales automatically to all available CPU cores. 
The ~7.9 billion candidate numbers are processed in chunks of 1,000,000 to keep memory usage flat.

## Requirements

- Python 3.6+
- No external dependencies (standard library only)
