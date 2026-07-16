with open('src/frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add admin button to navbar
admin_btn = '            <a href="#" class="nav-link" onclick="showModal(\'admin-login\'); return false;" style="color:var(--primary); font-weight:600;"><i class="fa-solid fa-user-shield"></i> Admin</a>\n        </div>'
html = html.replace('        </div>\n        <div id="user-section">', admin_btn + '\n        <div id="user-section">')

# 2. Add admin modal before </body>
admin_modal = '''
<!-- Admin Login Modal -->
<div class="modal-overlay" id="admin-login-modal" onclick="closeModalOutside(event, 'admin-login')">
    <div class="modal-box">
        <button class="modal-close" onclick="closeModal('admin-login')"><i class="fa-solid fa-xmark"></i></button>
        <div style="text-align: center; margin-bottom: 20px;">
            <i class="fa-solid fa-user-shield" style="font-size: 2.5rem; color: var(--primary); margin-bottom: 12px;"></i>
            <h2 style="font-size: 1.5rem;">Admin Portal</h2>
        </div>
        <form onsubmit="handleAdminLogin(event)">
            <div class="input-group" style="margin-bottom:16px;">
                <label>Admin Username</label>
                <input type="text" id="admin-user" placeholder="admin" required style="width:100%; padding:10px; border-radius:6px; border:1px solid #ccc;">
            </div>
            <div class="input-group" style="margin-bottom:16px;">
                <label>Admin Password</label>
                <input type="password" id="admin-pwd" placeholder="Enter password" required style="width:100%; padding:10px; border-radius:6px; border:1px solid #ccc;">
            </div>
            <button type="submit" class="btn-primary" style="width: 100%; justify-content: center; background: linear-gradient(135deg, #1e293b, #0f172a);">Access Dashboard</button>
        </form>
    </div>
</div>
<script src="app.js"></script>
'''
html = html.replace('<script src="app.js"></script>', admin_modal)

with open('src/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Added admin modal safely')
