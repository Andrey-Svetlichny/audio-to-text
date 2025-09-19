import subprocess


def chunk_text(text, max_chars=3000):
    """Split transcript into chunks for LLM processing"""
    chunks = []
    current = []
    length = 0
    for word in text.split():
        if length + len(word) + 1 > max_chars:
            chunks.append(" ".join(current))
            current = []
            length = 0
        current.append(word)
        length += len(word) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks


src = "text/02.txt"
with open(src, "r", encoding="utf-8") as f:
    text_src = f.read()
chunks = chunk_text(text_src)
print(f"Transcript split into {len(chunks)} chunks")


def ollama_generate(prompt, model="mistral"):
    """Send a prompt to a local Ollama model and return response text"""
    result = subprocess.run(
        ["ollama", "run", model], input=prompt.encode("utf-8"), stdout=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")


formatted_chunks = []

for i, chunk in enumerate(chunks, 1):
    prompt = f"""
Reformat the following audiobook transcript into readable paragraphs.
Do not summarize or change meaning — just add paragraph breaks and punctuation.

Transcript chunk {i}:
{chunk}
"""
    print(f"🔹 Processing chunk {i}/{len(chunks)}...")
    formatted = ollama_generate(prompt, model="mistral")
    formatted_chunks.append(formatted.strip())


with open("audiobook_paragraphs.txt", "w", encoding="utf-8") as f:
    for chunk in formatted_chunks:
        f.write(chunk + "\n\n")
