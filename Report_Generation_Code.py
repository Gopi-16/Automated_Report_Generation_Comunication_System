import pandas as pd
from pathlib import Path
import nbimporter
from Model_Connection_Code import model_response
from Preprocessing_Data_Code import preprocess
from Model_Connection_Code import generate_prompt_template
from Refining_Response_Code import refine_response

from Chat_Bot.Vector_Data_Store_Embed import create_index_file

def generate_reports(path):
    """Processes student data and generates reports using DeepSeek API with robust error handling."""
    reports_list=[]
    try:
        data, error = preprocess(Path(path))

        if error != 1:
            return "Error: Issue in data preprocessing.", data

        data = pd.DataFrame(data)  # Ensure data is in DataFrame format

        # Ensure "Status" column exists
        if "Status" not in data.columns:
            data["Status"] = 0  # Initialize "Status" column if missing

        # Generate the prompt template
        prompt_template = generate_prompt_template(data)

        # Add empty column for reports if not already there
        if "Generated_Report" not in data.columns:
            data["Generated_Report"] = ""

        for index, row in data.iterrows():
            if data.at[index, "Status"] != 1:
                try:
                    student_data = {col.lower().replace(" ", "_"): row[col] for col in data.columns}

                    print(f"Processing Student: {student_data.get('id', 'Unknown')}...")  # Debugging output

                    # Generate the report
                    report = model_response(prompt_template, student_data)
                    refined_report = refine_response(report)
                    
                    if refined_report and len(refined_report) != 0:
                        data.at[index, "Generated_Report"] = refined_report
                        print("hello")  # Store report in DataFrame
                        data.at[index, "Status"] = 1
                        reports_list.append(refined_report)
                        create_index_file(reports_list)  # Mark as processed

                except Exception as e:
                    print(f"Error processing student {student_data.get('id', 'Unknown')}: {e}")

        return data  # Ensure function returns DataFrame after all processing

    except Exception as e:
        return f"Critical Error: {e}"
    

# Load Data
#df = generate_reports("Students_Data.csv")

#if isinstance(df, pd.DataFrame):
   # df.to_csv("student_reports.csv", index=False)
    #print("✅ Student reports generated and saved successfully!")
#else:
    #print(df)  # Print error message if failed

