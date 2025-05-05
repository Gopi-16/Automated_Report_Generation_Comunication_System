from gtts import gTTS
import os

def convert_speech(reports_list, audio_output_dir):
    """
    Converts a list of reports into speech audio files and saves them in the specified folder.

    Args:
        reports_list (list): List of report strings to convert.
        audio_output_dir (str): Path to the folder where audio files will be stored.

    Returns:
        dict: Dictionary with two keys:
              - 'success': list of indices that succeeded
              - 'failed': list of indices that failed
    """
    os.makedirs(audio_output_dir, exist_ok=True)

    success_indices = []
    failed_indices = []

    for index, report in enumerate(reports_list):
        if not report or not isinstance(report, str):
            failed_indices.append(index)
            continue

        try:
            refining = re.sub(r"[*#-()]", "", report)
            refining=refining.replace("\\n","\n")
            tts = gTTS(text=refining, lang='en', slow=False)
            audio_path = os.path.join(audio_output_dir, f"student_{index}.mp3")
            tts.save(audio_path)
            success_indices.append(index)
        except Exception as e:
            failed_indices.append(index)

    return {
        "success": success_indices,
        "failed": failed_indices
    }

