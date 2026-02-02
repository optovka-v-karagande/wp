import re

def generate_html_from_text(input_file, output_html):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Собираем все блоки в список (для обратного порядка)
    items = []
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
                block = []
                block.append('<div class="item">\n')
                block.append(f' <img src="{current_image}" alt="{current_image}">\n')

                if description_lines:
                    block.append(' <div class="description">\n')
                    first_line = description_lines[0]
                    first_line_clean = re.sub(r'\s*:\s*\(file\s+attached\)\s*', '', first_line, flags=re.IGNORECASE).strip()

                    processed_lines = []
                    for i, desc_line in enumerate(description_lines):
                        text = first_line_clean if i == 0 else desc_line

                        # 1. Выделение через *текст*
                        text = re.sub(r'\*([^*]+?)\*', lambda m: '<b>' + m.group(1) + '</b>', text)

                        # 2. Выделение цен "число тенге"
                        text = re.sub(
                            r'(?i)([\d\s.,]+)\s*тенге\b',
                            lambda m: '<b>' + m.group(0) + '</b>',
                            text
                        )

                        processed_lines.append(text)

                    # Первая строка с номером
                    if processed_lines[0]:
                        block.append(f' <p><span class="pub-number">№ {item_number}</span>{processed_lines[0]}</p>\n')
                    else:
                        block.append(f' <p><span class="pub-number">№ {item_number}</span></p>\n')

                    for pl in processed_lines[1:]:
                        block.append(f' <p>{pl}</p>\n')

                    block.append(' </div>\n')

                block.append('</div>\n')
                items.append(''.join(block))

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
        block = []
        block.append('<div class="item">\n')
        block.append(f' <img src="{current_image}" alt="{current_image}">\n')

        if description_lines:
            block.append(' <div class="description">\n')
            first_line = description_lines[0]
            first_line_clean = re.sub(r'\s*:\s*\(file\s+attached\)\s*', '', first_line, flags=re.IGNORECASE).strip()

            processed_lines = []
            for i, desc_line in enumerate(description_lines):
                text = first_line_clean if i == 0 else desc_line

                text = re.sub(r'\*([^*]+?)\*', lambda m: '<b>' + m.group(1) + '</b>', text)
                text = re.sub(
                    r'(?i)([\d\s.,]+)\s*тенге\b',
                    lambda m: '<b>' + m.group(0) + '</b>',
                    text
                )

                processed_lines.append(text)

            if processed_lines[0]:
                block.append(f' <p><span class="pub-number">№ {item_number}</span>{processed_lines[0]}</p>\n')
            else:
                block.append(f' <p><span class="pub-number">№ {item_number}</span></p>\n')

            for pl in processed_lines[1:]:
                block.append(f' <p>{pl}</p>\n')

            block.append(' </div>\n')

        block.append('</div>\n')
        items.append(''.join(block))

    # Пишем HTML — новые сообщения сверху (обратный порядок)
    with open(output_html, 'w', encoding='utf-8') as html_file:
        html_file.write('<!DOCTYPE html>\n<html lang="ru">\n<head>\n')
        html_file.write('<meta charset="UTF-8">\n')
        html_file.write('<meta name="robots" content="noindex, nofollow">\n')
        html_file.write('<title>Оптовка на Саркыте +77022881777</title>\n')
        html_file.write('<link rel="stylesheet" href="styles.css">\n')
        html_file.write('</head>\n<body>\n')
        html_file.write('<div class="container">\n')

        # ← Самое главное: items[::-1] — новые сверху
        for block_html in items[::-1]:
            html_file.write(block_html)

        html_file.write('</div>\n</body>\n</html>\n')

    print(f"Готово! Создан файл: {output_html}")
    print(f"Обработано сообщений: {item_number}")


# Запуск (можно убрать if __name__ если запускаешь напрямую)
if __name__ == "__main__":
    generate_html_from_text("chat.txt", "index.html")