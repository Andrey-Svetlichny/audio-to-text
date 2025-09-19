# Audio to Text converter

import os
from pathlib import Path
import whisper
import nltk

# run next 2 lines once

# nltk.download("punkt")  # download tokenizer models
# nltk.download("punkt_tab")


dir_audio = "audio"
dir_txt = "text"
dir_tmp = "tmp"

# list of models to run
# to my surprise, medium produce better result than large on audiobooks
models = ["medium"] # tiny, base, small, medium, large


def audio_to_text(dir_src, dir_dst):
    """
    Convert audio to text.
    For each .mp3 file in dir_src produce .txt file in dir_dst
    (or list of .txt file, if multiple models selected to run)
    """

    for m in models:
        print(f"\nUse model: {m}\n--------")
        model = whisper.load_model(m)

        for path_audio in sorted(Path(dir_src).glob("*.mp3")):
            ext = ".txt" if len(models) == 1 else f"__{m}.txt"
            path_txt = Path(dir_dst) / (path_audio.stem + ext)
            print(f"\n{path_audio} => {path_txt}")

            result = model.transcribe(str(path_audio), language="en", verbose=True)
            with open(path_txt, "w", encoding="utf-8") as f:
                f.write(str(result["text"]))


def split_sentences(dir_src, dir_dst):
    # split text into sentences
    for src in sorted(Path(dir_src).glob("*.txt")):
        dst = Path(dir_dst) / src.name
        print(f"{src} => {dst}")

        with open(src, "r", encoding="utf-8") as f:
            text_src = f.read()

        sentences = nltk.sent_tokenize(text_src)
        text_dst = "\n".join(sentences)

        with open(dst, "w", encoding="utf-8") as f:
            f.write(text_dst)


os.makedirs(dir_tmp, exist_ok=True)
os.makedirs(dir_txt, exist_ok=True)
audio_to_text(dir_audio, dir_tmp)
split_sentences(dir_tmp, dir_txt)
