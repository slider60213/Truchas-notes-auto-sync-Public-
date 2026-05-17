import os

def patch_markdown_images(vault_dir):
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')
    
    print(f"=== [DEBUG] GitHub Actions Python Script Started ===")
    print(f"=== [DEBUG] Target Directory: {vault_dir}")

    # 檢查目標目錄是否存在
    if not os.path.exists(vault_dir):
        print(f"=== [DEBUG] ERROR: Target directory does not exist! ===")
        return

    md_file_count = 0
    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                md_file_count += 1
                file_path = os.path.join(root, file)
                # 列印出腳本在雲端實際上揪出的每一篇 MD 檔名與相對路徑
                print(f"=== [DEBUG] Found MD file: {os.path.relpath(file_path, vault_dir)}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    idx = 0
                    modified = False
                    
                    while True:
                        start_excl = content.find('![', idx)
                        if start_excl == -1:
                            break
                        
                        end_bracket = content.find(']', start_excl)
                        if end_bracket == -1:
                            idx = start_excl + 2
                            continue
                            
                        start_paren = content.find('(', end_bracket)
                        if start_paren == -1 or start_paren != end_bracket + 1:
                            idx = end_bracket + 1
                            continue
                            
                        end_paren = content.find(')', start_paren)
                        if end_paren == -1:
                            idx = start_paren + 1
                            continue

                        path_content = content[start_paren + 1:end_paren].strip()
                        alt_text = content[start_excl + 2:end_bracket].strip()
                        full_match_str = content[start_excl:end_paren + 1]
                        
                        lower_path = path_content.lower()
                        is_image = any(lower_path.endswith(ext) or (ext + '?') in lower_path for ext in valid_extensions)
                        
                        if is_image:
                            img_path = path_content.replace('%20', ' ').replace(' ', '%20')
                            width_attr = ''
                            if alt_text:
                                if '|' in alt_text:
                                    width = alt_text.split('|')[-1].strip()
                                    if width.isdigit():
                                        width_attr = f'width="{width}"'
                                elif alt_text.isdigit():
                                    width_attr = f'width="{alt_text}"'
                            
                            img_tag = f'<img src="{img_path}" {width_attr} style="background-color:#ffffff; padding:12px; border-radius:8px;" alt="Image">\n'
                            content = content.replace(full_match_str, img_tag)
                            idx = start_excl + len(img_tag)
                            print(f"    -> [MATCH SUCCESS] Replaced image: {path_content}")
                        else:
                            no_tag = f'{full_match_str}\n'
                            content = content.replace(full_match_str, no_tag)
                            idx = start_excl + len(no_tag)
                            print(f"    -> [MATCH FAILED] Not an image extension: {path_content}")
                            
                        modified = True

                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"    -> [FILE WRITE] Successfully saved modifications to {file}")
                        
                except Exception as e:
                    print(f"    -> [ERROR] Failed to process {file}: {str(e)}")

    print(f"=== [DEBUG] Scan Finished. Total MD files scanned: {md_file_count} ===")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, ".."))
    patch_markdown_images(vault_root)