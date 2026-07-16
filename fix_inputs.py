with open('src/frontend/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = app_js.replace('<input type="text" id="flight-from" placeholder="Delhi, DEL" value="Delhi">', '<input type="text" id="flight-from" placeholder="Delhi" value="Delhi" list="cities-list" autocomplete="off">')
app_js = app_js.replace('<input type="text" id="flight-to" placeholder="Mumbai, BOM" value="Mumbai">', '<input type="text" id="flight-to" placeholder="Mumbai" value="Mumbai" list="cities-list" autocomplete="off">')

app_js = app_js.replace('<input type="text" id="bus-from" placeholder="Delhi" value="Delhi">', '<input type="text" id="bus-from" placeholder="Delhi" value="Delhi" list="cities-list" autocomplete="off">')
app_js = app_js.replace('<input type="text" id="bus-to" placeholder="Manali" value="Manali">', '<input type="text" id="bus-to" placeholder="Manali" value="Manali" list="cities-list" autocomplete="off">')

app_js = app_js.replace('<input type="text" id="hotel-city" placeholder="Goa, India" value="Goa">', '<input type="text" id="hotel-city" placeholder="Goa" value="Goa" list="cities-list" autocomplete="off">')

with open('src/frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
print('Updated app.js inputs')
