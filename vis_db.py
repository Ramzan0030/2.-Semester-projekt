import sqlite3

db = sqlite3.connect('/home/azureuser/Bookingsystem/booking_system.db')

print('=== BRUGERE ===')
users = db.execute('SELECT * FROM users').fetchall()
for u in users:
    print(f'  ID: {u[0]} | Navn: {u[1]} | Email: {u[2]} | Password: {u[3]}')

print()
print('=== BOOKINGER ===')
bookings = db.execute('SELECT * FROM bookings').fetchall()
for b in bookings:
    print(f'  ID: {b[0]} | Bruger ID: {b[1]} | Træner: {b[2]} | Dato: {b[3]} | Tid: {b[4]}')

db.close()
