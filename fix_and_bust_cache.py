with open('src/frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the last remaining question mark in the checkout modal
content = content.replace('>?${parseFloat', '>&#8377;${parseFloat')

with open('src/frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

# Update index.html to cache-bust app.js
with open('src/frontend/index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

import re
index_content = re.sub(r'app\.js\?v=\d*', 'app.js?v=6', index_content)
if 'app.js?v=' not in index_content:
    index_content = index_content.replace('app.js', 'app.js?v=6')

with open('src/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)
