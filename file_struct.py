import os

# Define the directories and files you need
dirs = [
    "input_layer", 
    "nlp_engine", 
    "verification_layer", 
    "static", 
    "tests"
]

files = {
    "app.py": "",
    "requirements.txt": "",
    "README.md": "",
    "input_layer/__init__.py": "",
    "input_layer/input_handler.py": "",
    "nlp_engine/__init__.py": "",
    "nlp_engine/claim_extractor.py": "",
    "verification_layer/__init__.py": "",
    "verification_layer/verifier.py": "",
    "tests/test_input_layer.py": "",
    "tests/test_nlp_engine.py": ""
}

# Create directories
for dir in dirs:
    os.makedirs(dir, exist_ok=True)

# Create files with optional initial content
for file_path, content in files.items():
    with open(file_path, 'w') as file:
        file.write(content)

print("File structure created successfully!")
