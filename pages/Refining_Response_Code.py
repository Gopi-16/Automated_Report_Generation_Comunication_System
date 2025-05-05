import pandas as pd
import re

def refine_response(report):
    """Refines a single string report by removing unwanted characters and keeping text from 'Dear' onwards."""
    try:
        if pd.isna(report):  # Handle missing values
            return "",0

        # Remove unwanted characters (*, #, -)
        refining = re.sub(r"[*#-]", "", report)
        refining=refining.replace("\\n","\n")
        print(refining)

        # Find the first occurrence of "Dear"
        index_dear = refining.find("Dear")
        if index_dear != -1:
            refining = refining[index_dear:]  # Keep text from "Dear" onwards

        return refining,1

    except Exception as e:
        return f"Error processing a report: {e}",0



