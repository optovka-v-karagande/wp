import re

def generate_html_from_text(input_file, output_html):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_html, 'w', encoding='utf-8') as html_file:
        html_file.write('<!DOCTYPE html>\n<html lang="ru">\n<head>\n')
        html_file.write('<meta charset="UTF-8">\n')
        html_file.write('<meta name="robots" content="noindex, nofollow">\n')
        html_file.write('<title>Оптовка на Саркыте +77022881777</title>\n')
        html_file.write('<link rel="stylesheet" href="styles.css">\n')
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
                    html_file.write(f'  <img src="{current_image}" alt="{current_image}">\n')

                    if description_lines:
                        html_file.write('  <div class="description">\n')

                        first_line = description_lines[0]
                        # Удаляем ": (file attached)"
                        first_line_clean = re.sub(r'\s*:\s*\(file\s+attached\)\s*', '', first_line, flags=re.IGNORECASE).strip()

                        processed_lines = []
                        for i, desc_line in enumerate(description_lines):
                            if i == 0:
                                text = first_line_clean
                            else:
                                text = desc_line

                            # Поддержка нескольких пар *текст*
                            def bold_replace(m):
                                return '<b>' + m.group(1) + '</b>'

                            text = re.sub(r'\*([^*]+?)\*', bold_replace, text)

                            processed_lines.append(text)

                        # Первая строка с номером публикации
                        if processed_lines[0]:
                            html_file.write(f'    <p><span class="pub-number">№ {item_number}</span>{processed_lines[0]}</p>\n')
                        else:
                            html_file.write(f'    <p><span class="pub-number">№ {item_number}</span></p>\n')

                        # Остальные строки описания
                        for pl in processed_lines[1:]:
                            html_file.write(f'    <p>{pl}</p>\n')

                        html_file.write('  </div>\n')

                    html_file.write('</div>\n')

                # Начинаем новый блок
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
            html_file.write(f'  <img src="{current_image}" alt="{current_image}">\n')

            if description_lines:
                html_file.write('  <div class="description">\n')

                first_line = description_lines[0]
                first_line_clean = re.sub(r'\s*:\s*\(file\s+attached\)\s*', '', first_line, flags=re.IGNORECASE).strip()

                processed_lines = []
                for i, desc_line in enumerate(description_lines):
                    if i == 0:
                        text = first_line_clean
                    else:
                        text = desc_line

                    def bold_replace(m):
                        return '<b>' + m.group(1) + '</b>'

                    text = re.sub(r'\*([^*]+?)\*', bold_replace, text)

                    processed_lines.append(text)

                if processed_lines[0]:
                    html_file.write(f'    <p><span class="pub-number">№ {item_number}</span>{processed_lines[0]}</p>\n')
                else:
                    html_file.write(f'    <p><span class="pub-number">№ {item_number}</span></p>\n')

                for pl in processed_lines[1:]:
                    html_file.write(f'    <p>{pl}</p>\n')

                html_file.write('  </div>\n')

            html_file.write('</div>\n')

        html_file.write('</div>\n</body>\n</html>\n')

    print(f"Готово! Создан файл: {output_html}")
    print(f"Обработано сообщений: {item_number}")


# Пример использования:
generate_html_from_text("chat.txt", "index.html")