import re

def parse_aramco():
    path = r"C:\Users\zahran\.gemini\antigravity\brain\9d5b7203-2c83-46ac-b812-473d2adac47e\.system_generated\steps\1473\content.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Let's extract any HTML matching logo-preview-card or similar classes
    import re
    indices = [m.start() for m in re.finditer("logo-preview-card", content)]
    print(f"Indices of logo-preview-card: {indices}")
    for idx in indices:
        print(f"\n--- Occurrence at {idx} ---")
        print(content[idx:idx+1500])

parse_aramco()
