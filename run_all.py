import subprocess
import time
import os
import sys

def main():
    python_exe = sys.executable

    print("Starting Web Server (Flask)...")
    app_process = subprocess.Popen([python_exe, "app.py"])

    print("Starting Central Server...")
    central_process = subprocess.Popen([python_exe, "sensors/central_server.py"])

    print("Starting Sensor Simulator (All zones, Normal scenario)...")
    time.sleep(2)
    client_process = subprocess.Popen([python_exe, "sensors/zone_client.py", "--scenario", "normal"])

    db_backend = os.environ.get('DB_BACKEND', 'sqlite').lower()
    sb_process = None
    ng_process = None
    
    if db_backend == 'mysql':
        print("Starting Spring Boot Backend...")
        sb_process = subprocess.Popen(["cmd", "/c", "mvnw.cmd spring-boot:run"], cwd="springboot-backend")
        print("Starting Angular Frontend...")
        ng_process = subprocess.Popen(["cmd", "/c", "npm start"], cwd="angular-frontend")

    print("\n" + "="*50)
    print("All systems are now running in this single window!")
    print("Web Dashboard (Flask): http://127.0.0.1:5000")
    if db_backend == 'mysql':
        print("Spring API: http://127.0.0.1:8080")
        print("Angular UI: http://localhost:4200")
    print("Press Ctrl+C here at any time to shut everything down.")
    print("="*50 + "\n")

    try:
        app_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down all processes...")
        app_process.terminate()
        central_process.terminate()
        client_process.terminate()
        if sb_process:
            subprocess.Popen(["taskkill", "/F", "/T", "/PID", str(sb_process.pid)])
        if ng_process:
            subprocess.Popen(["taskkill", "/F", "/T", "/PID", str(ng_process.pid)])
        print("Done!")

if __name__ == '__main__':
    main()
