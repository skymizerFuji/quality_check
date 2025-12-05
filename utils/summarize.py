import sys
import json
from pathlib import Path


results = [
    {
        "hw": "vp1902",
        "test": "test"
    }
]
summary_header = f'''\
| Hardware | Test |
| :-: | :-: |\
'''
print(summary_header)

for result in results:
    print(
        f"| {result['hw'].upper()} "
        f"| {result['hw'].upper()} "
    )
