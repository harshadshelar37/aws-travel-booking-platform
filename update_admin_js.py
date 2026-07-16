with open('src/frontend/app.js', 'r', encoding='utf-8') as f:
    app_content = f.read()

new_admin_logic = """
        document.getElementById('admin-error').style.display = 'none';
        
        // Fetch Admin Data
        fetch('/api/admin/stats')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error loading dashboard: ' + data.error);
                    return;
                }
                
                closeModal('admin-login');
                
                let recentBookingsHtml = '';
                if (data.recent_bookings && data.recent_bookings.length > 0) {
                    data.recent_bookings.forEach(b => {
                        const dateObj = new Date(b.booking_date);
                        const dateStr = dateObj.toLocaleDateString('en-IN') + ' ' + dateObj.toLocaleTimeString('en-IN', {hour: '2-digit', minute:'2-digit'});
                        recentBookingsHtml += `
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <td style="padding: 15px;">#${b.booking_id}</td>
                                <td style="padding: 15px;">${b.user_name}</td>
                                <td style="padding: 15px;">
                                    <span style="background: rgba(37, 99, 235, 0.2); color: #60a5fa; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem;">${b.booking_type}</span>
                                </td>
                                <td style="padding: 15px;">&#8377;${parseFloat(b.amount).toLocaleString('en-IN')}</td>
                                <td style="padding: 15px; color: #94a3b8;">${dateStr}</td>
                            </tr>
                        `;
                    });
                } else {
                    recentBookingsHtml = '<tr><td colspan="5" style="padding: 15px; text-align: center; color: #94a3b8;">No recent bookings found.</td></tr>';
                }

                document.body.innerHTML = `
                    <div style="min-height: 100vh; background: linear-gradient(135deg, #0f172a, #1e293b); color: white; font-family: 'Inter', sans-serif; padding: 40px;">
                        
                        <div style="max-width: 1200px; margin: 0 auto;">
                            <!-- Header -->
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
                                <div>
                                    <h1 style="font-size: 2.5rem; font-weight: 700; margin: 0; background: linear-gradient(90deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Admin Dashboard</h1>
                                    <p style="color: #94a3b8; margin-top: 5px;">Welcome back, Admin.</p>
                                </div>
                                <button onclick="location.reload()" style="padding: 12px 24px; background: rgba(255, 255, 255, 0.1); color: white; border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 8px; cursor: pointer; font-weight: 600; backdrop-filter: blur(10px); transition: all 0.3s ease;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                    <i class="fa-solid fa-right-from-bracket"></i> Logout
                                </button>
                            </div>

                            <!-- Stat Cards -->
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 40px;">
                                <!-- Total Users -->
                                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px);">
                                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                        <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(59, 130, 246, 0.2); color: #3b82f6; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-right: 15px;">
                                            <i class="fa-solid fa-users"></i>
                                        </div>
                                        <h3 style="margin: 0; color: #94a3b8; font-weight: 500; font-size: 1.1rem;">Total Users</h3>
                                    </div>
                                    <div style="font-size: 2.5rem; font-weight: 700;">${data.total_users}</div>
                                </div>
                                
                                <!-- Total Bookings -->
                                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px);">
                                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                        <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(16, 185, 129, 0.2); color: #10b981; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-right: 15px;">
                                            <i class="fa-solid fa-ticket"></i>
                                        </div>
                                        <h3 style="margin: 0; color: #94a3b8; font-weight: 500; font-size: 1.1rem;">Total Bookings</h3>
                                    </div>
                                    <div style="font-size: 2.5rem; font-weight: 700;">${data.total_bookings}</div>
                                </div>

                                <!-- Total Revenue -->
                                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px);">
                                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                        <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(139, 92, 246, 0.2); color: #8b5cf6; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-right: 15px;">
                                            <i class="fa-solid fa-wallet"></i>
                                        </div>
                                        <h3 style="margin: 0; color: #94a3b8; font-weight: 500; font-size: 1.1rem;">Total Revenue</h3>
                                    </div>
                                    <div style="font-size: 2.5rem; font-weight: 700;">&#8377;${data.total_revenue.toLocaleString('en-IN')}</div>
                                </div>
                            </div>

                            <!-- Recent Bookings Table -->
                            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px);">
                                <h3 style="margin: 0 0 20px 0; font-size: 1.4rem; font-weight: 600;">Recent Transactions</h3>
                                <div style="overflow-x: auto;">
                                    <table style="width: 100%; border-collapse: collapse; text-align: left;">
                                        <thead>
                                            <tr style="border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8;">
                                                <th style="padding: 15px; font-weight: 600;">Booking ID</th>
                                                <th style="padding: 15px; font-weight: 600;">User Name</th>
                                                <th style="padding: 15px; font-weight: 600;">Service Type</th>
                                                <th style="padding: 15px; font-weight: 600;">Amount</th>
                                                <th style="padding: 15px; font-weight: 600;">Date</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${recentBookingsHtml}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            })
            .catch(err => {
                console.error(err);
                alert('Failed to load dashboard data.');
            });
"""

# We need to replace the old mock dashboard logic
old_logic = """
        document.getElementById('admin-error').style.display = 'none';
        alert('Welcome to Admin Portal! Dashboard loading...');
        closeModal('admin-login');
        // In a real app, this would redirect to /admin-dashboard.html
        document.body.innerHTML = '<div style="padding:50px; text-align:center; font-family:sans-serif;"><h2>Admin Dashboard</h2><p>Overview, Users, and Bookings would appear here.</p><button onclick="location.reload()" style="padding:10px 20px; background:#1a56db; color:white; border:none; border-radius:5px; cursor:pointer;">Logout</button></div>';
"""

if old_logic in app_content:
    app_content = app_content.replace(old_logic, new_admin_logic)
    with open('src/frontend/app.js', 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("Dashboard logic updated in app.js")
else:
    print("Could not find the old mock logic in app.js. Check the file content.")
