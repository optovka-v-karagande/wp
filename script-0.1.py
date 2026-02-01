import re

def generate_html_from_text(input_file, output_html):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_html, 'w', encoding='utf-8') as html_file:
        html_file.write('<!DOCTYPE html>\n<html lang="ru">\n<head>\n')
        html_file.write('<meta charset="UTF-8">\n')
        html_file.write('<title>Галерея изображений</title>\n')
        html_file.write('<style>\n')
        html_file.write('  .item { margin-bottom: 2.5em; }\n')
        html_file.write('  .item img { max-width: 400px; height: auto; display: block; margin-bottom: 0.8em; }\n')
        html_file.write('  .number { font-weight: bold; font-size: 1.2em; margin-bottom: 0.4em; }\n')
        html_file.write('  hr { border: 0; border-top: 1px solid #ddd; margin: 2em 0; }\n')
        html_file.write('</style>\n')
        html_file.write('</head>\n<body style="font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px;">\n')

        current_image = None
        description_lines = []
        item_number = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue  # пропускаем пустые строки

            # Ищем имя файла .jpg (берём последнее вхождение в строке)
            match = re.search(r'([^\s<>"\'\\]+\.jpg)', line, re.IGNORECASE)
            if match:
                # Сохраняем предыдущий блок, если он был
                if current_image is not None:
                    item_number += 1
                    html_file.write('<div class="item">\n')
                    html_file.write(f'  <div class="number">№ {item_number}</div>\n')
                    html_file.write(f'  <img src="{current_image}" alt="{current_image}">\n')
                    if description_lines:
                        html_file.write('  <p>' + '<br>'.join(description_lines) + '</p>\n')
                    html_file.write('</div>\n')
                    html_file.write('<hr>\n')

                # Начинаем новый блок
                current_image = match.group(1)
                description_lines = []

                # Если в этой же строке есть текст после имени файла
                remaining = line.replace(current_image, '', 1).strip()
                if remaining:
                    description_lines.append(remaining)

            else:
                # Обычная строка описания
                if current_image is not None:
                    description_lines.append(line)

        # Не забываем последний блок
        if current_image is not None:
            item_number += 1
            html_file.write('<div class="item">\n')
            html_file.write(f'  <div class="number">№ {item_number}</div>\n')
            html_file.write(f'  <img src="{current_image}" alt="{current_image}">\n')
            if description_lines:
                html_file.write('  <p>' + '<br>'.join(description_lines) + '</p>\n')
            html_file.write('</div>\n')

        html_file.write('</body>\n</html>\n')

    print(f"Готово! Создан файл: {output_html}")
    print(f"Обработано блоков: {item_number}")


# Пример запуска:
generate_html_from_text("chat.txt", "gallery.html")