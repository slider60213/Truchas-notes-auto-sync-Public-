import os
import re

def patch_markdown_images(vault_dir):
    # Match both standard MD syntax and Obsidian WikiLinks syntax
    pattern = re.compile(r'!\[(\d*)\]\(\s*(pics/[^)]+)\s*\)|!\[\[\s*(pics/[^\]]+)\s*\]\]')

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
                            width = match.group(1) or ''
                            img_path = match.group(2) or match.group(3)
                            
                            # Replace spaces with %20 for HTML compatibility
                            img_path = img_path.strip().replace(' ', '%20')
                            
                            width_attr = f'width="{width}"' if width else ''
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