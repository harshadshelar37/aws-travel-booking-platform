with open('src/frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

admin_logic = '''
// ========================
// ADMIN LOGIN
// ========================
function handleAdminLogin(e) {
    e.preventDefault();
    const user = document.getElementById('admin-user').value;
    const pwd = document.getElementById('admin-pwd').value;
    
    if (user === 'admin' && pwd === 'admin123') {
        alert('Welcome to Admin Portal! Dashboard loading...');
        closeModal('admin-login');
        // In a real app, this would redirect to /admin-dashboard.html
        document.body.innerHTML = '<div style="padding:50px; text-align:center; font-family:sans-serif;"><h2>Admin Dashboard</h2><p>Overview, Users, and Bookings would appear here.</p><button onclick="location.reload()" style="padding:10px 20px; background:#1a56db; color:white; border:none; border-radius:5px; cursor:pointer;">Logout</button></div>';
    } else {
        alert('Invalid Admin Credentials!');
    }
}
'''
if 'handleAdminLogin' not in content:
    with open('src/frontend/app.js', 'a', encoding='utf-8') as f:
        f.write('\n' + admin_logic)
    print('Added admin logic')
else:
    print('Admin logic already present')
