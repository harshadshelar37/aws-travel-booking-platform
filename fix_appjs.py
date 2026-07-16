with open('src/frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add buses form template
bus_template = '''    buses: 
        <div class="search-form" style="grid-template-columns: 1.5fr 1.5fr 1fr 1fr auto;">
            <div class="input-group">
                <label>From</label>
                <input type="text" id="bus-origin" required placeholder="Select City" list="locations-list" autocomplete="off">
            </div>
            <div class="input-group">
                <label>To</label>
                <input type="text" id="bus-dest" required placeholder="Select City" list="locations-list" autocomplete="off">
            </div>
            <div class="input-group">
                <label>Date</label>
                <input type="date" required id="bus-date">
            </div>
            <div class="input-group">
                <label>Pickup / Drop</label>
                <input type="text" id="bus-pickup" placeholder="Street or Area (Optional)" autocomplete="off">
            </div>
            <button type="button" class="btn btn-primary btn-search" onclick="searchData('buses')">Search Buses</button>
        </div>
    ,
    packages: '''
content = content.replace('    packages: ', bus_template)

# 2. Update searchData params
buses_fetch = '''    } else if (type === 'hotels') {
        let loc = document.getElementById('hotel-loc').value;
        if(loc) url += '&location=' + encodeURIComponent(loc);
    } else if (type === 'buses') {
        let orig = document.getElementById('bus-origin').value;
        let dest = document.getElementById('bus-dest').value;
        if(orig) url += '&origin=' + encodeURIComponent(orig);
        if(dest) url += '&destination=' + encodeURIComponent(dest);
    }'''
content = content.replace("    } else if (type === 'hotels') {\n        let loc = document.getElementById('hotel-loc').value;\n        if(loc) url += '&location=' + encodeURIComponent(loc);\n    }", buses_fetch)

# 3. Update createCard logic
buses_card = '''    } else if (type === 'buses') {
        price = item.price;
        html = 
            <div class="card-header">
                <h3></h3>
                <div class="price">?</div>
            </div>
            <div class="card-body">
                <p><strong>From:</strong>  ()</p>
                <p><strong>To:</strong>  ()</p>
                <p><strong>Type:</strong> </p>
                <p><strong>Duration:</strong> </p>
            </div>
        ;
    } else if (type === 'cabs') {'''
content = content.replace("    } else if (type === 'cabs') {", buses_card)

with open('src/frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
