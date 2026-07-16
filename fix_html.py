import re

with open('src/frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

datalist = '''
    <datalist id="cities-list">
        <option value="Delhi">
        <option value="Mumbai">
        <option value="Bangalore">
        <option value="Hyderabad">
        <option value="Chennai">
        <option value="Kolkata">
        <option value="Pune">
        <option value="Ahmedabad">
        <option value="Goa">
        <option value="Manali">
        <option value="Jaipur">
        <option value="Shimla">
    </datalist>
'''

if 'id="cities-list"' not in html:
    html = html.replace('</body>', datalist + '\n</body>')
    with open('src/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added datalist to index.html")
else:
    print("Datalist already present")
