import smtplib
import pandas as pd
import re
import dns.resolver
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email sender details
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "mocharlavarsha@gmail.com"
SENDER_PASSWORD = "azvf eqhu fngm twoq"  # App Password

# ------------------- Email Validation -------------------

def is_valid_email_format(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def verify_email_domain(email):
    try:
        domain = email.split("@")[-1]
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False

# ------------------- Email Sender -------------------

def send_email_with_audio(to_email, message, audio_path):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Student Report with Audio By Friend 😀"

        msg.attach(MIMEText(message, "plain"))

        if audio_path and os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                part = MIMEBase("audio", "mpeg")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(audio_path)}"')
                msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False

# ------------------- Main Function -------------------

def run_mailing(csv_path, audio_folder):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return [], []

    required_columns = {"gmail", "Generated_Report"}
    if not required_columns.issubset(df.columns):
        print(f"❌ Missing required columns: {required_columns}")
        return [], []

    sent, failed = [], []

    for idx, row in df.iterrows():
        recipient = row["gmail"]
        refining = re.sub(r"[*#-()]", "", row["Generated_Report"])
        refining=refining.replace("\\n","\n")
        message = refining
        audio_path = os.path.join(audio_folder, f"student_{idx}.mp3")

        # Email validations
        is_format_valid = is_valid_email_format(recipient)
        is_domain_valid = verify_email_domain(recipient)

        print(f"\n📨 Sending to: {recipient}")
        print(f"   ➤ Format Valid: {is_format_valid}")
        print(f"   ➤ Domain Valid: {is_domain_valid}")

        if is_format_valid and is_domain_valid:
            if send_email_with_audio(recipient, message, audio_path):
                print(f"✅ Sent to {recipient}")
                sent.append(recipient)
            else:
                failed.append(recipient)
        else:
            print(f"⚠️ Invalid email skipped: {recipient}")
            failed.append(recipient)

    return sent, failed

# ------------------- Standalone Test -------------------

#if __name__ == "__main__":
    #sent, failed = run_mailing("student_reports.csv", "audio_files")
    #print("\n🎯 Summary")
    #print(f"✅ Sent: {len(sent)}")
    #print(f"❌ Failed: {len(failed)}")

