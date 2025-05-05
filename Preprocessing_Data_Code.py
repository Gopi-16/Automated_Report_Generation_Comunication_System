import pandas as pd
from pathlib import Path

def preprocess(path):
    """Loads and processes the dataset, handling multi-index and missing values."""
    try:
        compulsory_fields = ["Name", "gmail"]
        suffix = path.suffix

        # Read the file based on its extension
        if suffix == ".csv":
            data_read = pd.read_csv(path, header=[0, 1] if check_multiindex(path) else 0)
        elif suffix in [".xlsx", ".ods"]:
            data_read = pd.read_excel(path, header=[0, 1] if check_multiindex(path) else 0)
        elif suffix == ".json":
            data_read = pd.read_json(path)
        else:
            return "Unsupported file format", 0

        # Fix MultiIndex columns
        if isinstance(data_read.columns, pd.MultiIndex):
            data_read = fix_multiindex(data_read)

        # Remove the first column if it's an unnamed index
        if data_read.columns[0].lower().startswith("unnamed"):
            data_read = data_read.iloc[:, 1:]

        # Ensure it's a clean DataFrame
        data_read = pd.DataFrame(data_read)

        # Ensure "Status" column exists
        if "Status" not in data_read.columns:
            data_read["Status"] = 0

        # Check for missing compulsory fields
        missing = [field for field in compulsory_fields if field not in data_read.columns]
        if len(missing) > 0:
            return f"{missing} fields are missing in dataset", 0

        return data_read, 1

    except FileNotFoundError:
        return "File Not Found", 0
    except pd.errors.EmptyDataError:
        return "Error: File is empty", 0
    except pd.errors.ParserError:
        return "Error: File is corrupted or has formatting issues", 0
    except Exception as e:
        return f"Unexpected error: {e}", 0

def check_multiindex(file_path):
    try:
        sample_df = pd.read_csv(file_path, nrows=2)
        return sample_df.iloc[0].astype(str).str.contains("Marks").any()
    except:
        return False

def fix_multiindex(df):
    df.columns = pd.MultiIndex.from_tuples([
        (col[0], col[1] if "Unnamed" not in col[1] else '') for col in df.columns
    ])
    return df
#dataa=preprocess(Path("testing_data.csv"))
#print(dataa)
