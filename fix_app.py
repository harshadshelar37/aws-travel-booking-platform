with open('src/frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix literal \? 
content = content.replace('\\?', '?')

# Let's ensure there are no backticks missing. Wait, let me check the file carefully for <option> or anything.
# Wait, I noticed I also appended the Admin Modal Javascript.
# Let's fix the \? first.

with open('src/frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed literal \? in app.js")
