import re

def generate_html_from_text(input_file, output_html):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_html, 'w', encoding='utf-8') as html_file:
        html_file.write('<!DOCTYPE html>\n<html lang="ru">\n<head>\n')
        html_file.write('<meta charset="UTF-8">\n')
        html_file.write('<title>Галерея сообщений</title>\n')
        html_file.write('<style>\n')
        html_file.write('  body {\n')
        html_file.write('    background-color: #e5ddd5;\n')
        html_file.write('    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;\n')
        html_file.write('    margin: 0;\n')
        html_file.write('    padding: 20px;\n')
        html_file.write('    color: #111;\n')
        html_file.write('  }\n')
        html_file.write('  .container {\n')
        html_file.write('    max-width: 600px;\n')
        html_file.write('    margin: 0 auto;\n')
        html_file.write('  }\n')
        html_file.write('  .item {\n')
        html_file.write('    background-color: #ffffff;\n')
        html_file.write('    border-radius: 8px;\n')
        html_file.write('    padding: 16px;\n')
        html_file.write('    margin-bottom: 24px;\n')
        html_file.write('    box-shadow: 0 1px 3px rgba(0,0,0,0.12);\n')
        html_file.write('  }\n')
        html_file.write('  .item img {\n')
        html_file.write('    max-width: 560px;\n')
        html_file.write('    height: auto;\n')
        html_file.write('    display: block;\n')
        html_file.write('    margin: 0 auto 12px;\n')
        html_file.write('    border-radius: 6px;\n')
        html_file.write('  }\n')
        html_file.write('  .number {\n')
        html_file.write('    font-weight: bold;\n')
        html_file.write('    color: #0066cc;\n')
        html_file.write('    margin-bottom: 10px;\n')
        html_file.write('  }\n')
        html_file.write('  .description p:first-child {\n')
        html_file.write('    font-size: 0.75em;\n')
        html_file.write('    color: #777;\n')
        html_file.write('    margin: 0 0 8px 0;\n')
        html_file.write('    line-height: 1.4;\n')
        html_file.write('  }\n')
        html_file.write('  .description p {\n')
        html_file.write('    margin: 0 0 2px 0;\n')
        html_file.write('    line-height: 1.3;\n')
        html_file.write('  }\n')
        html_file.write('</style>\n')
        html_file.write('</head>\n<body>\n')
        html_file.write('<div class="container">\n')

        current_image = None
        description_lines = []
        item_number = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = re.search(r'([^\s<>"\'\\]+\.jpg)', line, re.IGNORECASE)
            if match:
                # Сохраняем предыдущий блок
                if current_image is not None:
                    item_number += 1
                    html_file.write('<div class="item">\n')
                    html_file.write(f'  <div class="number">№ {item_number}</div>\n')
                    html_file.write(f'  <img src="{current_image}" alt="{current_image}">\n')
                    
                    if description_lines:
                        # Очищаем первую строку от "(file attached)"
                        first_line = description_lines[0]
                        first_line_clean = re.sub(r'\s*\(file\s+attached\)\s*', '', first_line, flags=re.IGNORECASE).strip()
                        if first_line_clean:  # если после очистки что-то осталось
                            html_file.write('  <div class="description">\n')
                            html_file.write(f'    <p>{first_line_clean}</p>\n')
                            for desc_line in description_lines[1:]:
                                html_file.write(f'    <p>{desc_line}</p>\n')
                            html_file.write('  </div>\n')
                        elif len(description_lines) > 1:
                            # если первая строка исчезла полностью — выводим со второй как первую
                            html_file.write('  <div class="description">\n')
                            html_file.write(f'    <p>{description_lines[1]}</p>\n')
                            for desc_line in description_lines[2:]:
                                html_file.write(f'    <p>{desc_line}</p>\n')
                            html_file.write('  </div>\n')

                    html_file.write('</div>\n')

                # Новый блок
                current_image = match.group(1)
                description_lines = []

                remaining = line.replace(current_image, '', 1).strip()
                if remaining:
                    description_lines.append(remaining)

            else:
                if current_image is not None:
                    description_lines.append(line)

        # Последний блок
        if current_image is not None:
            item_number += 1
            html_file.write('<div class="item">\n')
            html_file.write(f'  <div class="number">№ {item_number}</div>\n')
            html_file.write(f'  <img src="{current_image}" alt="{current_image}">\n')
            
            if description_lines:
                first_line = description_lines[0]
                first_line_clean = re.sub(r'\s*\(file\s+attached\)\s*', '', first_line, flags=re.IGNORECASE).strip()
                
                html_file.write('  <div class="description">\n')
                if first_line_clean:
                    html_file.write(f'    <p>{first_line_clean}</p>\n')
                    start_idx = 1
                else:
                    start_idx = 2 if len(description_lines) > 1 else 0
                
                for desc_line in description_lines[start_idx:]:
                    html_file.write(f'    <p>{desc_line}</p>\n')
                html_file.write('  </div>\n')
            
            html_file.write('</div>\n')

        html_file.write('</div>\n</body>\n</html>\n')

    print(f"Готово! Создан файл: {output_html}")
    print(f"Обработано сообщений: {item_number}")


# Пример запуска:
generate_html_from_text("chat.txt", "output.html")