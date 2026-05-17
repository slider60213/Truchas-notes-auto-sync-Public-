import os

def test_github_actions(vault_dir):
    for root, dirs, files in os.walk(vault_dir):
        # 排除隱藏資料夾
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            # 只針對測試用的 MD 檔案，或你指定的那篇筆記，確保不影響其他重要檔案
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 為了安全且不重複附加，檢查是否已經有測試文字
                    if "SHANE TEST" not in content:
                        new_content = content + "\n\nSHANE TEST\n"
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Successfully added test text to: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, ".."))
    test_github_actions(vault_root)