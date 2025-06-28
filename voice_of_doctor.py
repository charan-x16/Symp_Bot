from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

# For Testing purpose 
def text_to_speech_with_gtts_test(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )

    audioobj.save(output_filepath)

input_text = "Hi this side Sridhar Charan!, how are you!"

# text_to_speech_with_gtts_test(input_text=input_text, output_filepath="audio/gtts_testing.mp3")

import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_test(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Alice",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

# text_to_speech_with_elevenlabs_test(input_text=input_text, output_filepath="audio/elevenlabs_testing.mp3")

import subprocess
import platform
from pydub import AudioSegment
import tempfile


def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    os_name = platform.system()

    # For Windows, use a temporary WAV file for playback
    if os_name == "Windows":
        # Save as MP3 first (to the specified path)
        audioobj.save(output_filepath)
        # Convert to WAV in a temporary file
        sound = AudioSegment.from_mp3(output_filepath)
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sound.export(temp_wav.name, format="wav")
        temp_wav.close()
        # Play the WAV file
        try:
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{temp_wav.name}").PlaySync();'])
        except Exception as e:
            print(f"An error occurred while trying to play the audio: {e}")
        finally:
            # Clean up the temporary file
            os.unlink(temp_wav.name)
    else:
        # For other OS, proceed as before
        audioobj.save(output_filepath)
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', output_filepath])
            elif os_name == "Linux":  # Linux
                subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
            else:
                raise OSError("Unsupported operating system")
        except Exception as e:
            print(f"An error occurred while trying to play the audio: {e}")


# text_to_speech_with_gtts(input_text, output_filepath="audio/gtts_testing_new.mp3")


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Alice",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Convert MP3 to WAV for playback
            sound = AudioSegment.from_mp3(output_filepath)
            temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            sound.export(temp_wav.name, format="wav")
            temp_wav.close()
            # Play the WAV file
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{temp_wav.name}").PlaySync();'])
            # Clean up the temporary file
            os.unlink(temp_wav.name)
        elif os_name == "Linux":  # Linux
            # Use 'mpg123' for MP3 playback (install if needed: sudo apt-get install mpg123)
            subprocess.run(['mpg123', output_filepath])
            # Or use 'aplay' for WAV: subprocess.run(['aplay', output_filepath])  # Only for WAV files
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# text_to_speech_with_elevenlabs(input_text, output_filepath="audio/elevenlabs_testing_new.mp3")
