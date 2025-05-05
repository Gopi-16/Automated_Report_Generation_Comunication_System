import fitz  # PyMuPDF
from TTS.api import TTS

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return None

def convert_text_to_speech(text, output_file, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
    try:
        tts = TTS(model_name=model_name)
        tts.tts_to_file(text=text, file_path=output_file)
        print(f"✅ Audio saved as: {output_file}")
    except Exception as e:
        print(f"❌ Error converting text to speech: {e}")

# === Usage ===
pdf_path = "EPI Unit-2.pdf"            # 🔄 Replace with your PDF file
output_audio = "output_audio.wav"      # 🔈 Output audio filename

extracted_text = extract_text_from_pdf(pdf_path)

if extracted_text:
    print("📄 Text extracted successfully.")
    convert_text_to_speech(extracted_text, output_audio)
else:
    print("⚠️ No text found in PDF.")

