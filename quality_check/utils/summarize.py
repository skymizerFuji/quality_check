import pandas as pd
import re
from quality_check.config import PROJECT_ROOT
def escape_markdown_cell(value):
    """
    Escape characters that are special in markdown tables so that
    raw cell content (e.g. '**Title**', 'a|b') does not break the table.
    """
    if pd.isna(value):
        return ""
    text = str(value)

    # Escape backslash first
    text = text.replace("\\", "\\\\")

    # Escape pipes so they don't create extra columns
    text = text.replace("|", "\\|")

    # Escape markdown formatting characters: *, _, ~, `
    text = re.sub(r"([*`_~])", r"\\\1", text)

    # Replace newlines inside cells so they don't split rows
    text = text.replace("\n", "<br>")

    return text

def df_to_markdown_table(df, align="center"):
    """
    Convert a pandas DataFrame to a Markdown table string with safe, escaped cells.
    """
    # Map alignment to Markdown syntax
    if align == "left":
        align_token = ":--"
    elif align == "right":
        align_token = "--:"
    else:  # default "center"
        align_token = ":-:"

    # Header row (header names usually safe, but escape anyway)
    header = "| " + " | ".join(escape_markdown_cell(c) for c in df.columns) + " |"

    # Alignment row
    align_row = "| " + " | ".join([align_token] * len(df.columns)) + " |"

    # Data rows
    data_rows = []
    for _, row in df.iterrows():
        values = [escape_markdown_cell(v) for v in row.tolist()]
        data_rows.append("| " + " | ".join(values) + " |")

    return "\n".join([header, align_row] + data_rows)

if __name__ == "__main__":
    # Example DataFrame
    df = pd.read_csv( PROJECT_ROOT / "dataset/skymizer_chat.csv")
    md = df_to_markdown_table(df)
    print(md)