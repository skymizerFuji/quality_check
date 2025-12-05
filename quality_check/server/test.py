"""
python benchmark.py -m Qwen/Qwen2.5-1.5B-Instruct -i zh -o unquantized
python benchmark.py -m Qwen/Qwen2.5-1.5B-Instruct -c ./dataset/OpenSafetyMini.csv -i prompt -o unquantized
python benchmark.py -m Qwen/Qwen2.5-1.5B-Instruct -c ./dataset/OpenSafetyMini.csv -i prompt -o quantized
python benchmark.py -m Qwen/Qwen2.5-1.5B-Instruct -c ./dataset/skymizer_chat.csv -i zh -o fp16
"""
import argparse
from openai import OpenAI
import pandas as pd
from tqdm import tqdm

# Initialize the OpenAI client with your API key
custom_endpoint_url = "http://localhost:8010"
client = OpenAI(base_url=custom_endpoint_url)
completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-1.5B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. When answering, unless requested otherwise, give the answer directly without explaining your thought process."},
        {"role": "user", "content": "hello"}
    ]
)
output = completion.choices[0].message.content
print(output)