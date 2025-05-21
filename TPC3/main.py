import sys
import re

def convert_headers(text):
    for i in range(6, 0, -1):
        pattern = r'^' + '#' * i + r' (.+)$'
        repl = rf'<h{i}>\1</h{i}>'
        text = re.sub(pattern, repl, text, flags=re.MULTILINE)
    return text

def convert_bold_italic(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    return text

def convert_links_images(text):
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    return text

def convert_blockquotes(text):
    pattern = r'(?:^> .+\n?)+'
    for match in re.finditer(pattern, text, re.MULTILINE):
        original = match.group(0)
        lines = re.findall(r'^> (.+)', original, re.MULTILINE)
        html = f"<blockquote>{'<br>'.join(lines)}</blockquote>"
        text = text.replace(original, html)
    return text

def convert_lists(text):
    # Ordered lists
    text = re.sub(r'(?m)(^\d+\. .+(?:\n\d+\. .+)*)',
                  lambda m: "<ol>" + "".join(f"<li>{line[3:]}</li>" for line in m.group(0).splitlines()) + "</ol>",
                  text)
    # Unordered lists
    text = re.sub(r'(?m)^([*-]) (.+)', r'<li>\2</li>', text)
    text = re.sub(r'(<li>.*?</li>\n?)+',
                  lambda m: "<ul>" + m.group(0).replace('\n', '') + "</ul>",
                  text)
    return text

def markdown_to_html(markdown_text):
    text = markdown_text
    text = convert_headers(text)
    text = convert_bold_italic(text)
    text = convert_links_images(text)
    text = convert_blockquotes(text)
    text = convert_lists(text)
    return text

def build_full_html(body_content):
    return f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>TPC3</title>
</head>
<body style="display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 0;">
    <div style="width: 100%; max-width: 800px; padding: 20px;">
        {body_content}
    </div>
    <footer>
        <hr>
        TPC3 Conversor Markdown HTML - Henrique Pereira - A97205
    </footer>
</body>
</html>"""

def main():
    if len(sys.argv) != 3:
        print("Uso: python script.py input.md output.html")
        return

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
    except FileNotFoundError:
        print(f"Erro: ficheiro '{md_file}' não encontrado.")
        return

    html_output = markdown_to_html(markdown_text)
    final_html = build_full_html(html_output)

    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"✅ HTML gerado com sucesso em '{html_file}'")
    except Exception as e:
        print(f"Erro ao escrever ficheiro HTML: {e}")

if __name__ == "__main__":
    main()
