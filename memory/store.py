memory = []

def add_memory(text: str):
    memory.append(text)

def recall_memory():
    return "\n".join(memory[-5:])
