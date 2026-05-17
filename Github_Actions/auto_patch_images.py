import os
import re

def patch_markdown_images(vault_dir):
    # 強大萬用正則：精確捕捉標準 Markdown、Obsidian 混血網頁語法
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
                            
                            # 統一處理路徑中的空白字元與網頁編碼
                            img_path = img_path.strip().replace('%20', ' ').replace(' ', '%20')
                            
                            width_attr = ''
                            # 解析 Obsidian 各種 | 寬高組合 (例如: 394|375, |425, image_name|310)
                            if alt_text and '|' in alt_text:
                                parts = [p.strip() for p in alt_text.split('|')]
                                # 優先檢查第一部分是不是純數字寬度 (如 394|375)
                                if parts[0].isdigit():
                                    width_attr = f'width="{parts[0]}"'
                                # 再檢查最後一部分是不是純數字寬度 (如 image_name|310)
                                elif parts[-1].isdigit():
                                    width_attr = f'width="{parts[-1]}"'
                            elif alt_text and alt_text.isdigit():
                                width_attr = f'width="{alt_text}"'
                            
                            # 回傳完美的圓角白底標籤，並維持原本的寬度縮放
                            return f'<img src="{img_path}" {width_attr} style="background-color:#ffffff; padding:12px; border-radius:8px;" alt="Image">'

                        new_content = pattern.sub(replacer, content)

                        if new_content != content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"Successfully patched images in: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, ".."))
    patch_markdown_images(vault_root)