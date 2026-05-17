import os
import re

def patch_markdown_images(vault_dir):
    # 精準正則：抓取標準 Markdown 圖片語法 ! [ alt ] ( path )
    # Group 1: 欄位描述 (含寬度) , Group 2: 完整檔案路徑
    md_pattern = re.compile(r'!\[([^\]]*)\]\(\s*([^)]+)\s*\)')
    
    # 支援的圖片副檔名
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')

    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    def replacer(match):
                        alt_text = match.group(1)
                        img_path = match.group(2).strip()
                        
                        # 擷取路徑最後，轉小寫來檢查是否為圖片檔
                        lower_path = img_path.lower()
                        if lower_path.endswith(valid_extensions) or any(ext + '?' in lower_path for ext in valid_extensions):
                            # 整理路徑編碼（處理空白與 %20）
                            img_path = img_path.replace('%20', ' ').replace(' ', '%20')
                            
                            # 解析 Obsidian 的寬高設定 (例如: image|310)
                            width_attr = ''
                            if alt_text:
                                if '|' in alt_text:
                                    width = alt_text.split('|')[-1].strip()
                                    if width.isdigit():
                                        width_attr = f'width="{width}"'
                                elif alt_text.isdigit():
                                    width_attr = f'width="{alt_text}"'
                                    
                            return f'<img src="{img_path}" {width_attr} style="background-color:#ffffff; padding:12px; border-radius:8px;" alt="Image">'
                        
                        # 如果不是圖片副檔名，保持原樣不變
                        return match.group(0)

                    new_content = md_pattern.sub(replacer, content)

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