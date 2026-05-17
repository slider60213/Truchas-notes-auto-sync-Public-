import os
import re

def patch_markdown_images(vault_dir):
    # Regex pattern to match standard Markdown image format: ![width](path)
    md_pattern = re.compile(r'!\[(\d*)\]\((pics/[^)]+)\)')

    for root, dirs, files in os.walk(vault_dir):
        # Exclude hidden folders like .git and .obsidian
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if 'pics/' in content:
                    # Replace with HTML img tag containing background styling
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

if __name__ == "__main__":
    # Locate the repository root folder (one level above this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_root = os.path.abspath(os.path.join(script_dir, ".."))
    patch_markdown_images(vault_root)