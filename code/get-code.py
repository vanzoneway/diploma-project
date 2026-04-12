import os
import re

# Оставляем ТОЛЬКО Java-файлы
VALID_EXTENSIONS = ('.java',)

# Папки, которые полностью исключаем
EXCLUDED_DIRS = {
    '.git', '.idea', '.gradle', 'build', 'out', 'target', 'logs', 'gradle',
    'db', 'changelog', 'hoppscotch-collection', 'test',
    'dto',         # Исключаем пакеты с DTO
    'model',       # Исключаем JPA сущности
    'constants',   # Исключаем константы
    'configuration',# Исключаем конфигурации бинов и Swagger
    'mapper',      # Исключаем мапперы (это интерфейсы для MapStruct)
}

# Конкретные файлы, которые исключаем
EXCLUDED_FILES = {
    'cab-aggregator-app-realm.json', 'gradlew', 'gradlew.bat'
}

def process_file_content(content):
    """
    Очистка файла от импортов, пакетов, пустых строк и интерфейсов.
    """
    lines = content.split('\n')
    filtered_lines = []
    
    # Флаг, указывающий, что файл является интерфейсом
    is_interface = False
    
    for line in lines:
        stripped_line = line.strip()
        
        if not stripped_line:
            continue
            
        if stripped_line.startswith('import '):
            continue
            
        if stripped_line.startswith('package '):
            continue
            
        # Если в файле объявляется интерфейс (или record), мы его пропускаем полностью
        # Исключаем "public interface ...", "public record ..."
        if stripped_line.startswith('public interface ') or stripped_line.startswith('public record '):
            is_interface = True
            break # Прерываем обработку этого файла
            
        filtered_lines.append(line)
        
    if is_interface:
        return None # Возвращаем None, чтобы скрипт проигнорировал этот файл
        
    return '\n'.join(filtered_lines)

def extract_code_from_directory(project_dir, output_txt_path):
    collected_code = ""
    
    for root, _, files in os.walk(project_dir):
        path_parts = set(root.replace('\\', '/').split('/'))
        
        # Если папка в списке исключений
        if EXCLUDED_DIRS.intersection(path_parts):
            continue
            
        for file in files:
            if file in EXCLUDED_FILES:
                continue
                
            # Пропускаем основной класс Application.java
            if file.endswith('Application.java'):
                continue
                
            file_path = os.path.join(root, file)
            
            is_valid_file = any(file.endswith(ext) for ext in VALID_EXTENSIONS)
            
            if is_valid_file:
                try:
                    relative_path = os.path.relpath(file_path, project_dir).replace('\\', '/')
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        raw_content = f.read()
                        
                    clean_content = process_file_content(raw_content)
                    
                    # Если файл не пустой и не интерфейс
                    if clean_content:
                        collected_code += f"// Файл: {relative_path}\n"
                        collected_code += clean_content + "\n\n"
                        
                except Exception as e:
                    print(f"Ошибка при чтении файла {file_path}: {e}")

    collected_code = collected_code.strip()

    with open(output_txt_path, 'w', encoding='utf-8') as out_file:
        out_file.write(collected_code)
    
    print(f"✅ Готово! СУПЕР-СЖАТЫЙ код (только бизнес-логика) успешно собран в файл: {output_txt_path}")

if __name__ == "__main__":
    print("--- Генератор листинга (только бизнес-логика) ---")
    while True:
        dirr = input("Введите полный путь к папке с проектом (или 'q' для выхода): ").strip()
        
        if dirr.lower() == 'q':
            break
            
        if not os.path.exists(dirr):
            print("❌ Ошибка: Указанный путь не существует. Попробуйте еще раз.")
            continue
            
        output_file = os.path.join(os.path.dirname(dirr), "diploma_code_listing.txt")
        extract_code_from_directory(dirr, output_file)