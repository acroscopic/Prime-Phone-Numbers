"""
This program creates area_codes.json, but it's included in the repository for redundancy.
This program serves more of a source rather than a tool to be used.
"""

import requests
import re
import json

url = "https://www.areacodelocations.info/areacodelist.html"
html = requests.get(url).text

codes = re.findall(r"\b[2-9]\d{2}\b", html)
unique_codes = sorted(set(int(c) for c in codes))

with open("area_codes.json", "w") as f:
    json.dump(unique_codes, f)
