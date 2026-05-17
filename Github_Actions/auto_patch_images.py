import os

def patch_markdown_images(vault_dir):
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')

    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            # 1. 先判讀是否為 md 檔
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 偵測內容，尋找所有符合 ![...] (...) 的區塊
                    idx = 0
                    modified = False
                    
                    while True:
                        # 尋找驚嘆號
                        start_excl = content.find('![', idx)
                        if start_excl == -1:
                            break
                        
                        # 尋找對應的中括號結尾
                        end_bracket = content.find(']', start_excl)
                        if end_bracket == -1:
                            idx = start_excl + 2
                            continue
                            
                        # 尋找緊接在後的小括號開頭
                        start_paren = content.find('(', end_bracket)
                        # 確保中括號與小括號之間沒有隔太遠（通常是相連的）
                        if start_paren == -1 or start_paren != end_bracket + 1:
                            idx = end_bracket + 1
                            continue
                            
                        # 尋找小括號結尾
                        end_paren = content.find(')', start_paren)
                        if end_paren == -1:
                            idx = start_paren + 1
                            continue

                        # 完全符合格式後，直接以括號當作首尾索引，截取 (...) 裡面的內容
                        path_content = content[start_paren + 1:end_paren].strip()
                        
                        # 判斷截取出來的字串結尾是否為圖片格式
                        lower_path = path_content.lower()
                        is_image = any(lower_path.endswith(ext) or (ext + '?') in lower_path for ext in valid_extensions)
                        
                        if is_image:
                            # 拿到原本完整的 ![...](...) 字串
                            full_match_str = content[start_excl:end_paren + 1]
                            
                            # 提取 alt 內容來解析寬度
                            alt_text = content[start_excl + 2:end_bracket].strip()
                            
                            # 整理圖片路徑中的空白字元與 %20
                            img_path = path_content.replace('%20', ' ').replace(' ', '%20')
                            
                            width_attr = ''
                            if alt_text:
                                if '|' in alt_text:
                                    width = alt_text.split('|')[-1].strip()
                                    if width.isdigit():
                                        width_attr = f'width="{width}"'
                                elif alt_text.isdigit():
                                    width_attr = f'width="{alt_text}"'
                            
                            # 組合成白底圓角 <img> 標籤
                            img_tag = f'<img src="{img_path}" {width_attr} style="background-color:#ffffff; padding:12px; border-radius:8px;" alt="Image">'
                            
                            # 直接替換內容
                            content = content.replace(full_match_str, img_tag)
                            modified = True
                            
                            # 因為長度改變，將索引重設回該段落之後繼續尋找
                            idx = start_excl + len(img_tag)
                        else:
                            idx = end_paren + 1

                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Successfully patched: {file}")
                        
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, ".."))
    patch_markdown_images(vault_root)