import os

VALID_EXTENSIONS = (
    '.py',
    '.yaml',
    '.yml',
    '.toml',
    '.ini',
    '.sh',
    '.mako',
    'Dockerfile',
    '.css',
    '.html',
    '.ipynb',
)
EXCLUDED_DIRS = (
    '\\venv',
    '\\bin',
    '\\obj',
    '\\.pytest_cache',
    '\\__pycache__',
    '\\.git',
    '\\Properties',
    '\\docs',
    '\\images',
    '\\log',
    '\\input',
    '\\output',
    '\\checkpoints',
)

def extract_code_from_directory(project_dir, output_txt_path):
    collected_code = ""
    for root, _, files in os.walk(project_dir):
        if any(excl in root.lower() for excl in EXCLUDED_DIRS):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(VALID_EXTENSIONS):
                try:
                    # Получаем относительный путь
                    relative_path = os.path.relpath(file_path, project_dir)
                    collected_code += f'\n# Файл "{relative_path}":\n\n'
                    with open(file_path, 'r', encoding='utf-8') as f:
                        collected_code += f.read() + "\n\n"
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    with open(output_txt_path, 'w', encoding='utf-8') as out_file:
        out_file.write(collected_code)

while True:
    dirr = input("Dir: ")
    extract_code_from_directory(dirr, dirr + "-code.txt")