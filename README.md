# convert audio files to text
# source mp3 files should be in "audio"

python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/openai/whisper.git
pip install torch
pip install nltk

python app.py
