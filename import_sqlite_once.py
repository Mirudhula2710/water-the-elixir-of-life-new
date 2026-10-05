import sqlite3
import mysql.connector
import os
import sys

def get_mysql_connection():
    try:
        return mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            port=int(os.environ.get('DB_PORT', 3306)),
            database=os.environ.get('DB_NAME', 'water_elixir'),
            user=os.environ.get('DB_USERNAME', 'water_app_user'),
            password=os.environ.get('DB_PASSWORD')
        )
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        sys.exit(1)

def map_severity(old_severity):
    # Mapping based on D4
    mapping = {
        'Normal': 'LOW',
        'Warning': 'MEDIUM',
        'Suspected Leak': 'HIGH',
        'Critical': 'CRITICAL'
    }
    return mapping.get(old_severity, 'LOW')

def import_data():
    if not os.environ.get('DB_PASSWORD'):
        print("Error: DB_PASSWORD environment variable is required.")
        sys.exit(1)
        
    sqlite_db_path = 'instance/water_app.db'
    if not os.path.exists(sqlite_db_path):
        print(f"SQLite DB not found at {sqlite_db_path}. Skipping import.")
        return

    # Open SQLite read-only
    uri = f"file:{os.path.abspath(sqlite_db_path)}?mode=ro"
    try:
        sl_conn = sqlite3.connect(uri, uri=True)
        sl_cursor = sl_conn.cursor()
    except sqlite3.Error as e:
        print(f"Error opening SQLite DB: {e}")
        return

    my_conn = get_mysql_connection()
    my_cursor = my_conn.cursor()

    try:
        # Import Zones
        sl_cursor.execute("SELECT id, name FROM zone")
        zones = sl_cursor.fetchall()
        zone_map = {} # sqlite_id -> mysql_id
        
        for z_id, name in zones:
            my_cursor.execute("SELECT zone_id FROM zone WHERE name = %s", (name,))
            existing = my_cursor.fetchone()
            if existing:
                zone_map[z_id] = existing[0]
            else:
                # Default zone_type to 'Unknown', valve_state to 'OPEN'
                my_cursor.execute("INSERT INTO zone (name, zone_type, valve_state) VALUES (%s, %s, %s)", (name, 'Unknown', 'OPEN'))
                zone_map[z_id] = my_cursor.lastrowid
        
        # Import Readings
        sl_cursor.execute("SELECT id, zone_id, tank_level, timestamp FROM reading")
        readings = sl_cursor.fetchall()
        reading_map = {}
        for r_id, z_id, tank_level, timestamp in readings:
            new_z_id = zone_map.get(z_id)
            if not new_z_id: continue
            
            # Check if this reading already exists to make script idempotent
            my_cursor.execute("SELECT reading_id FROM reading WHERE zone_id=%s AND recorded_at=%s", (new_z_id, timestamp))
            existing = my_cursor.fetchone()
            if existing:
                reading_map[r_id] = existing[0]
            else:
                # Flow_rate not stored in sqlite, use 0.0
                my_cursor.execute(
                    "INSERT INTO reading (zone_id, water_level, flow_rate, recorded_at) VALUES (%s, %s, %s, %s)",
                    (new_z_id, tank_level, 0.0, timestamp)
                )
                reading_map[r_id] = my_cursor.lastrowid

        # Import Alerts
        sl_cursor.execute("SELECT id, zone_id, reading_id, severity, deviation, gemini_explanation, status, created_at FROM alert")
        alerts = sl_cursor.fetchall()
        alert_map = {}
        for a_id, z_id, r_id, severity, deviation, gemini_exp, status, created_at in alerts:
            new_z_id = zone_map.get(z_id)
            new_r_id = reading_map.get(r_id)
            if not new_z_id: continue
            
            mapped_severity = map_severity(severity)
            
            my_cursor.execute("SELECT alert_id FROM alert WHERE zone_id=%s AND created_at=%s", (new_z_id, created_at))
            existing = my_cursor.fetchone()
            if existing:
                alert_map[a_id] = existing[0]
            else:
                # expected_level not stored in sqlite, use 0.0
                my_cursor.execute(
                    """INSERT INTO alert (zone_id, reading_id, severity, expected_level, deviation, gemini_explanation, status, created_at)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (new_z_id, new_r_id, mapped_severity, 0.0, deviation, gemini_exp, status.upper() if status else 'OPEN', created_at)
                )
                alert_map[a_id] = my_cursor.lastrowid
                
        # Import Complaints
        # student_id maps to user, but we don't migrate users here (D12).
        # We just import the complaint details.
        try:
            sl_cursor.execute("SELECT id, zone_id, description, status, created_at FROM complaint")
            complaints = sl_cursor.fetchall()
            for c_id, z_id, desc, status, created_at in complaints:
                new_z_id = zone_map.get(z_id)
                if not new_z_id: continue
                
                my_cursor.execute("SELECT complaint_id FROM complaint WHERE zone_id=%s AND created_at=%s AND description=%s", (new_z_id, created_at, desc))
                if not my_cursor.fetchone():
                    my_cursor.execute(
                        "INSERT INTO complaint (zone_id, description, status, created_at) VALUES (%s, %s, %s, %s)",
                        (new_z_id, desc, status.upper() if status else 'NEW', created_at)
                    )
        except sqlite3.OperationalError:
            print("No complaint table or error reading it.")
            
        # Import Tickets
        try:
            sl_cursor.execute("SELECT id, alert_id, zone_id, status, worker_notes, created_at, resolved_at FROM ticket")
            tickets = sl_cursor.fetchall()
            for t_id, a_id, z_id, status, notes, created_at, resolved_at in tickets:
                new_a_id = alert_map.get(a_id)
                if not new_a_id: continue
                
                my_cursor.execute("SELECT ticket_id FROM ticket WHERE alert_id=%s AND created_at=%s", (new_a_id, created_at))
                if not my_cursor.fetchone():
                    my_cursor.execute(
                        "INSERT INTO ticket (alert_id, status, notes, created_at, resolved_at) VALUES (%s, %s, %s, %s, %s)",
                        (new_a_id, status.upper() if status else 'OPEN', notes, created_at, resolved_at)
                    )
        except sqlite3.OperationalError:
            print("No ticket table or error reading it.")

        my_conn.commit()
        print("SQLite data successfully imported to MySQL.")
        
    except Exception as e:
        print(f"Migration error: {e}")
        my_conn.rollback()
    finally:
        sl_conn.close()
        my_cursor.close()
        my_conn.close()

if __name__ == "__main__":
    import_data()
