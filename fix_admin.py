with open('src/frontend/index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Add error div in admin modal
if 'admin-error' not in idx_content:
    idx_content = idx_content.replace(
        '<form onsubmit="handleAdminLogin(event)">',
        '<form onsubmit="handleAdminLogin(event)">\n<div id="admin-error" style="color: #dc2626; background: #fee2e2; border: 1px solid #f87171; padding: 10px; border-radius: 6px; margin-bottom: 16px; display: none; text-align: center; font-size: 0.9rem;">Invalid Admin Credentials!</div>'
    )

with open('src/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(idx_content)

with open('src/frontend/app.js', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Update handleAdminLogin
if "alert('Invalid Admin Credentials!');" in app_content:
    app_content = app_content.replace(
        "alert('Invalid Admin Credentials!');",
        "document.getElementById('admin-error').style.display = 'block';"
    )
    # also hide error on success
    app_content = app_content.replace(
        "alert('Welcome to Admin Portal! Dashboard loading...');",
        "document.getElementById('admin-error').style.display = 'none';\n    alert('Welcome to Admin Portal! Dashboard loading...');"
    )

with open('src/frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(app_content)
