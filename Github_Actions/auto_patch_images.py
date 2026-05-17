import os
import re

def patch_markdown_images(vault_dir):
    # Regex pattern to match standard Markdown image format: ![width](pics/path)
    md_pattern = re.compile(r'!\[(\d*)\]\((pics/[^)]+)\)')

    for root, dirs, files in os.walk(vault_dir):
        # Exclude hidden folders
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            # 確保只處理標準筆記，跳過外掛產生的衝突暫存檔
            if file.endswith('.md') and 'conflict-files' not in file:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'pics/' in content:
                        def replacer(match):
                            width = match.group(1)
                            img_path = match.group(2)
                            width_attr = f'width="{width}"' if width else ''
                            return f'<img src="{img_path}" {width_attr} style="background-color:#ffffff; padding:10px; border-radius:8px;" alt="Image">'

                        new_content = md_pattern.sub(replacer, content)

                        if new_content != content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"Successfully patched: {file}")
                except Exception as e:
                    print(f"Skipped file due to error: {file}, {str(e)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, ".."))
    patch_markdown_images(vault_root)