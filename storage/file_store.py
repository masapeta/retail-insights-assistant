
def save_local(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)

def load_local(path: str) -> str:
    with open(path, "r") as f:
        return f.read()
