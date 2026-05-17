import os
import re

def patch_markdown_images(vault_dir):
    # 萬用匹配：尋找 Markdown 圖片語法 ![[...]] 或 ![寬度](路徑)
    # 捕捉標準 MD 語法：![寬度](路徑)
    md_pattern = re.compile(r'!\[(\d*)\]\((pics/[^)]+)\)')

    for root, dirs, files in os.walk(vault_dir):
        # 排除隱藏資料夾（如 .git, .obsidian）
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 如果有點擊 PPT 貼上的圖片，進行萬用替換
                if 'pics/' in content:
                    # 替換成自帶圓角白底、保持原有寬度的標準 HTML 標籤
                    def replacer(match):
                        width = match.group(1)
                        img_path = match.group(2)
                        width_attr = f'width="{width}"' if width else ''
                        return f'<img src="{img_path}" {width_attr} style="background-color:#ffffff; padding:10px; border-radius:8px;" alt="Image">'

                    new_content = md_pattern.sub(replacer, content)

                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"成功自動優化圖片樣式: {file}")

if __name__ == "__main__":
    # 使用相對路徑，自動偵測當前執行目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))
    patch_markdown_images(current_dir)