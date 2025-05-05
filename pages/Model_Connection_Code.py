from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
def generate_prompt_template(data):
    """Creates a dynamic PromptTemplate based on dataset columns."""

    # Convert column names into valid input variables
    input_variables = [col.lower().replace(" ", "_") for col in data.columns]

    # Define a template using dynamically generated variables
    template = f"""
    You are an AI assistant specialized in generating student progress reports.

    ### **Student Report**
    """ + "\n".join([f"- **{col.replace('_', ' ').title()}**: {{{col}}}" for col in input_variables]) + """

    ### **Task:**
    Generate a well-structured and professional student progress report.
    The report should include:
    1. A greeting and introduction about the student.
    2. **Academic performance** analysis.
    3. Strengths and **areas for improvement**.
    4. **Personalized recommendations**.
    5. My name is **K. Vinodh Kumar M.Tech**, and my position is **Head Of the Institution**.
    6. College Name **RGUKT RK Valley**.
    7. Remove the **date field**,don't give bold tags,defaulty give the new line not as\n.
    8. Generate reports in the **same format but with different content**.
    9. **Generate the report with a bold tag** (omit the word "report").
    10.specify the parent name correctly if not available use dear parents word at report genration.
    

    Keep the tone **professional, detailed, and encouraging**.
    """

    return PromptTemplate(input_variables=input_variables, template=template)


import requests
import time
load_dotenv()

# Fetch API key from .env securely
api_key = os.getenv("Report_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure it's set in the .env file as OPENROUTER_API_KEY")
def model_response(prompt_template, student_data, retries=3, delay=5):
    """Generates the student progress report using the DeepSeek API with error handling."""
    
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    API_KEY = api_key

    # Format the template with student data
    prompt = prompt_template.format(**student_data)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-r1-distill-llama-70b:free",  
        "messages": [
            {"role": "system", "content": "You are an expert in educational report generation."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=15)  
            response.raise_for_status()  # Raise error for bad HTTP status codes
            
            # Ensure JSON response is valid
            response_data = response.json()
            if "choices" in response_data and response_data["choices"]:
                return response_data["choices"][0]["message"]["content"]
            print("Unexpected API response format, retrying...")
            time.sleep(delay)
            delay = min(delay * 2, 30)  # Increase delay for next retry
            continue

        except requests.exceptions.Timeout:
            print(f"Request timed out. Retrying in {delay} seconds...")
        except requests.exceptions.ConnectionError:
            print(f"Network error. Retrying in {delay} seconds...")
        except requests.exceptions.HTTPError as err:
            if response.status_code == 429:  # Rate limit exceeded
                retry_after = int(response.headers.get("Retry-After", 5))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            elif response.status_code >= 500:
                print("Server error. Retrying in 10 seconds...")
                time.sleep(10)
                continue
            else:
                return f"API Error: {err}"
        except requests.exceptions.RequestException as e:
            return f"Unexpected API Request Error: {e}"

        time.sleep(delay)
        delay = min(delay * 2, 30)  # Limit max delay to 30 seconds

    return "Error: Failed to generate report after multiple attempts."

