import urllib.request
url = 'http://prod-alb-600778398.eu-west-3.elb.amazonaws.com/'
content = urllib.request.urlopen(url).read().decode('utf-8')
content = content.replace('<li><a href=\"#\" data-target=\"hotels\"><i class=\"fa-solid fa-hotel\"></i> Hotels</a></li>', '<li><a href=\"#\" data-target=\"buses\"><i class=\"fa-solid fa-bus\"></i> Buses</a></li>\n                <li><a href=\"#\" data-target=\"hotels\"><i class=\"fa-solid fa-hotel\"></i> Hotels</a></li>')
content = content.replace('<button class=\"tab-btn\" data-target=\"hotels\">Hotels</button>', '<button class=\"tab-btn\" data-target=\"buses\">Buses</button>\n                    <button class=\"tab-btn\" data-target=\"hotels\">Hotels</button>')
open('src/frontend/index.html', 'w', encoding='utf-8').write(content)
