import yaml
import os

with open('cloudformation/travel_booking_platform.yaml', 'r', encoding='utf-8') as f:
    # CloudFormation yaml has tags like !Sub, which pyyaml doesn't support by default
    # So we'll just extract the files block with simple string parsing
    lines = f.readlines()

in_files = False
current_file = None
file_content = []

os.makedirs('src/backend', exist_ok=True)
os.makedirs('src/frontend', exist_ok=True)
os.makedirs('src/systemd', exist_ok=True)
os.makedirs('src/nginx', exist_ok=True)

for i, line in enumerate(lines):
    if line.startswith("          files:"):
        in_files = True
        continue
    if in_files:
        if line.startswith("          commands:"):
            break
            
        # Match file path like "            /home/ec2-user/app/backend/app.py:"
        if line.startswith("            /") and line.strip().endswith(":"):
            # Save previous file
            if current_file and file_content:
                # Get the base filename
                filename = current_file.strip().split('/')[-1][:-1]
                path = current_file.strip()[:-1]
                
                out_path = None
                if 'backend' in path: out_path = f"src/backend/{filename}"
                elif 'frontend' in path: out_path = f"src/frontend/{filename}"
                elif 'systemd' in path: out_path = f"src/systemd/{filename}"
                elif 'nginx' in path: out_path = f"src/nginx/nginx.conf"
                
                if out_path:
                    with open(out_path, 'w', encoding='utf-8') as out_f:
                        out_f.write("".join(file_content))
                
            current_file = line
            file_content = []
            continue
            
        if current_file:
            if line.startswith("              content: |"):
                continue
            elif line.startswith("              mode:") or line.startswith("              owner:") or line.startswith("              group:"):
                continue
            elif line.startswith("                "):
                # Strip the 16 spaces of indentation for content
                file_content.append(line[16:])
            elif line.strip() == "":
                file_content.append(line)

# Handle the last file
if current_file and file_content:
    filename = current_file.strip().split('/')[-1][:-1]
    path = current_file.strip()[:-1]
    out_path = None
    if 'backend' in path: out_path = f"src/backend/{filename}"
    elif 'frontend' in path: out_path = f"src/frontend/{filename}"
    elif 'systemd' in path: out_path = f"src/systemd/{filename}"
    elif 'nginx' in path: out_path = f"src/nginx/nginx.conf"
    
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write("".join(file_content))
print("Extraction complete!")
