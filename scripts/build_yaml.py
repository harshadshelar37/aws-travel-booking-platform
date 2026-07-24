import os

# Files to inject
files = {
    '/etc/nginx/nginx.conf': 'src/nginx/nginx.conf',
    '/etc/systemd/system/travel-backend.service': 'src/backend/travel-backend.service',
    '/home/ec2-user/app/backend/schema.sql': 'src/backend/schema.sql',
    '/home/ec2-user/app/backend/seed.py': 'src/backend/seed.py',
    '/home/ec2-user/app/backend/app.py': 'src/backend/app.py',
    '/home/ec2-user/app/backend/requirements.txt': 'src/backend/requirements.txt',
    '/home/ec2-user/app/frontend/index.html': 'src/frontend/index.html',
    '/home/ec2-user/app/frontend/style.css': 'src/frontend/style.css',
    '/home/ec2-user/app/frontend/app.js': 'src/frontend/app.js'
}

modes = {
    '/home/ec2-user/app/backend/seed.py': '000755',
    '/etc/systemd/system/travel-backend.service': '000644'
}

yaml_lines = []
yaml_lines.append("          files:\n")

for target_path, local_path in files.items():
    yaml_lines.append(f"            {target_path}:\n")
    yaml_lines.append("              content: |\n")
    with open(local_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for line in content.split('\n'):
        # For EOF empty lines we just indent 16 spaces
        yaml_lines.append(f"                {line}\n")
    
    mode = modes.get(target_path, '000644')
    owner = 'root' if ('nginx' in target_path or 'systemd' in target_path) else 'ec2-user'
    
    yaml_lines.append(f"              mode: '{mode}'\n")
    yaml_lines.append(f"              owner: '{owner}'\n")
    yaml_lines.append(f"              group: '{owner}'\n")

# Now replace the files block in cloudformation/travel_booking_platform.yaml
with open('cloudformation/travel_booking_platform.yaml', 'r', encoding='utf-8') as f:
    orig_lines = f.readlines()

out_lines = []
in_files = False
for i, line in enumerate(orig_lines):
    if line.startswith("          files:"):
        in_files = True
        out_lines.extend(yaml_lines)
        continue
    if in_files:
        if line.startswith("          commands:"):
            in_files = False
            out_lines.append(line)
        continue
    if not in_files:
        out_lines.append(line)

with open('cloudformation/travel_booking_platform.yaml', 'w', encoding='utf-8') as f:
    f.write("".join(out_lines))

print("Injected successfully!")
