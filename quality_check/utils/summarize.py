import pandas as pd
from quality_check.config import PROJECT_ROOT

def df_to_markdown_table(df, align="center"):
    """
    Convert a pandas DataFrame to a Markdown table string.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to convert.
    align : {"left", "center", "right"}, optional
        Alignment of columns in the Markdown table.

    Returns
    -------
    str
        Markdown table as a string.
    """
    # Map alignment to Markdown syntax
    if align == "left":
        align_token = ":--"
    elif align == "right":
        align_token = "--:"
    else:  # default "center"
        align_token = ":-:"

    # Header row
    header = "| " + " | ".join(df.columns.astype(str)) + " |"

    # Alignment row
    align_row = "| " + " | ".join([align_token] * len(df.columns)) + " |"

    # Data rows
    data_rows = []
    for _, row in df.iterrows():
        values = [str(v) for v in row.tolist()]
        data_rows.append("| " + " | ".join(values) + " |")

    # Join all parts
    return "\n".join([header, align_row] + data_rows)


if __name__ == "__main__":
    # Example DataFrame
    df = pd.read_csv( PROJECT_ROOT / "dataset/skymizer_chat.csv")
    md = df_to_markdown_table(df)
    print(md)