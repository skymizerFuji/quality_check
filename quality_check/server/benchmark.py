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

def main(model, input_col, output_col, csv_path):
    df = pd.read_csv(csv_path)
    save_every = 5
    # if df does not have output_col, create it with NaN values
    if output_col not in df.columns:
        df[output_col] = pd.NA
    for index, row in tqdm(df.iterrows()):
        if not pd.isnull(row[output_col]):
            print(f"Skipping index {index} as it already has a value.")
            continue
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. When answering, unless requested otherwise, give the answer directly without explaining your thought process."},
                {"role": "user", "content": row[input_col]}
            ]
        )
        output = completion.choices[0].message.content
        df.at[index, output_col] = output
        if index % save_every == 0:
            df.to_csv(csv_path, index=False)
    df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OpenAI completions on a CSV file.")
    parser.add_argument("-m","--model", default="Qwen/Qwen2.5-1.5B-Instruct", help="The model to use for completions.")
    parser.add_argument("-i", "--input_col", required=True, help="The column name for prompts.")
    parser.add_argument("-o", "--output_col", required=True, help="The column name for outputs.")
    parser.add_argument("-c", "--csv_path", default="./dataset/skymizer_chat.csv", help="The path to the CSV file.")

    args = parser.parse_args()

    main(args.model, args.input_col, args.output_col, args.csv_path)