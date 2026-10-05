import socket
import time
import json
import random
import argparse
import multiprocessing
import sys

HOST = '127.0.0.1'
PORT = 65432
ZONES = ['Hostel Blocks', 'Laboratories', 'Administration Building', 'Canteen']

def simulate_zone(zone_name, scenario):
    level = 100.0
    iteration = 0
    
    print(f"[{zone_name}] Starting simulation with scenario: {scenario}")
    
    while True:
        # Base expected drop over 5s is approx 1.0 to 1.5 based on physics model at level 100.
        # We will mimic the expected drop roughly, then apply the scenario deviation.
        expected_drop = 1.1 
        level -= expected_drop
        
        # Apply deterministic deviations every 3 iterations to trigger alerts clearly
        if iteration % 3 == 0 and iteration > 0:
            if scenario == 'low':
                level -= 7.0   # roughly -7% deviation -> Warning
            elif scenario == 'leak':
                level -= 15.0  # roughly -15% deviation -> Suspected Leak
            elif scenario == 'critical':
                level -= 25.0  # roughly -25% deviation -> Critical

        if level < 0:
            level = 100.0

        payload = {'zone': zone_name, 'level': level}
        
        connected = False
        retries = 0
        while not connected and retries < 3:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(json.dumps(payload).encode('utf-8'))
                    connected = True
            except ConnectionRefusedError:
                retries += 1
                time.sleep(2)
            except Exception as e:
                print(f"[{zone_name}] Error sending data: {e}")
                break
                
        if not connected:
            print(f"[{zone_name}] Server unavailable after retries.")

        iteration += 1
        time.sleep(5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Water Leak Sensor Client")
    parser.add_argument('--scenario', choices=['normal', 'low', 'leak', 'critical'], default='normal', help='Injection scenario')
    parser.add_argument('--zone', choices=ZONES, help='Specific zone to simulate')
    
    args = parser.parse_args()
    
    zones_to_run = [args.zone] if args.zone else ZONES
    processes = []
    
    for zone in zones_to_run:
        p = multiprocessing.Process(target=simulate_zone, args=(zone, args.scenario))
        p.start()
        processes.append(p)
        
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("\nShutting down clients...")
        for p in processes:
            p.terminate()
        sys.exit(0)
