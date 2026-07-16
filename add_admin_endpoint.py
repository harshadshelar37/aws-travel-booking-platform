with open('src/backend/app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

admin_stats_code = """
@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get total users
        cursor.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']
        
        # Get total bookings
        cursor.execute("SELECT COUNT(*) as total_bookings FROM bookings")
        total_bookings = cursor.fetchone()['total_bookings']
        
        # Get total revenue
        cursor.execute("SELECT SUM(amount) as total_revenue FROM payments WHERE status = 'Success'")
        rev_row = cursor.fetchone()
        total_revenue = float(rev_row['total_revenue']) if rev_row['total_revenue'] else 0.0
        
        # Get recent bookings
        query = '''
            SELECT b.booking_id, u.name as user_name, b.booking_type, b.booking_date, p.amount 
            FROM bookings b 
            JOIN users u ON b.user_id = u.user_id 
            LEFT JOIN payments p ON b.booking_id = p.booking_id
            ORDER BY b.booking_date DESC 
            LIMIT 5
        '''
        cursor.execute(query)
        recent_bookings = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "total_users": total_users,
            "total_bookings": total_bookings,
            "total_revenue": total_revenue,
            "recent_bookings": recent_bookings
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""

if 'def get_admin_stats' not in app_content:
    app_content = app_content.replace("if __name__ == '__main__':", admin_stats_code + "if __name__ == '__main__':")
    with open('src/backend/app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)
