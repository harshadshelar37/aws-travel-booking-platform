import os

with open('travel_booking_platform.yaml', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith('  AppTargetGroup:'):
        skip = True
    if skip and line.startswith('  RDSInstance:'):
        skip = False
        
    if not skip:
        new_lines.append(line)

with open('test_half.yaml', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Created test_half.yaml without AppTargetGroup, ALB, AutoScaling, EC2, IAM, etc.")
