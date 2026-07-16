with open('src/frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace literal ? with HTML entity for Rupee
content = content.replace('>?${price', '>&#8377;${price')
content = content.replace('?3000', '&#8377;3000')
content = content.replace('?500 OFF', '&#8377;500 OFF')
content = content.replace('?2500', '&#8377;2500')
content = content.replace('?200', '&#8377;200')

with open('src/frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced ? with Rupee entity in app.js")
