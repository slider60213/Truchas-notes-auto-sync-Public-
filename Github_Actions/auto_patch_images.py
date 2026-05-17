import os
import re

def patch_markdown_images(vault_dir):
    # 究極萬用正則：同時相容所有標準 MD、混血 MD (%20)、以及 Obsidian 雙括號語法
    # 只要含有 pics/ 且符合圖片特徵，全部一網打盡
    pattern = re.compile(r'!\[([^\]]*)\]\(\s*(pics/[^)]+)\s*\)|!\[\[\s*(pics/[^\]]+)\s*\]\]')

    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'pics/' in content:
                        def replacer(match):
                            alt_text = match.group(1) or ''
                            img_path = match.group(2) or match.group(3)
                            
                            # 統一將路徑中的空白或 %20 整理乾淨，確保網頁能讀取
                            img_path = img_path.strip().replace('%20', ' ').replace(' ', '%20')
                            
                            # 檢查 alt 欄位有沒有用直線 | 寫死寬度 (例如 Pasted image|314 或純 394)
                            width_attr = ''
                            if alt_text:
                                if '|' in alt_text:
                                    width = alt_text.split('|')[-1].strip()
                                    if width.isdigit():
                                        width_attr = f'width="{width}"'
                                elif alt_text.isdigit():
                                    width_attr = f'width="{alt_text}"'
                            
                            return f'<img src="{img_path}" {width_attr} style="background-color:#ffffff; padding:10px; border-radius:8px;" alt="Image">'

                        new_content = pattern.sub(replacer, content)

                        if new_content != content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"Successfully patched: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, ".."))
    patch_markdown_images(vault_root)