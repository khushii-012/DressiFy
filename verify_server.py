import subprocess
import time
import urllib.request
import urllib.error
import json
import sys

def test_endpoints():
    print("Launching Flask server in background...")
    proc = subprocess.Popen([sys.executable, "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to boot
    time.sleep(3)
    
    try:
        # Test 1: Fetch profile
        print("Testing GET /api/profile...")
        req = urllib.request.Request("http://127.0.0.1:5000/api/profile")
        with urllib.request.urlopen(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            assert "name" in data
            print(f"  Success! Profile returned for user: {data['name']}")

        # Test 2: Fetch wardrobe
        print("Testing GET /api/wardrobe...")
        req = urllib.request.Request("http://127.0.0.1:5000/api/wardrobe")
        with urllib.request.urlopen(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            assert isinstance(data, list)
            print(f"  Success! Wardrobe retrieved with {len(data)} items.")

        # Test 3: Generate suggestion
        print("Testing POST /api/generate...")
        payload = json.dumps({
            "gender": "Female",
            "age": 22,
            "style": "Casual",
            "weather": "Sunny",
            "occasion": "Casual"
        }).encode('utf-8')
        req = urllib.request.Request(
            "http://127.0.0.1:5000/api/generate",
            data=payload,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            assert "category" in data
            assert "items" in data
            print(f"  Success! Generated category: {data['category']}")
            
        print("\nAll automated endpoint checks passed successfully! [OK]")
        return True
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return False
    except AssertionError as e:
        print(f"Assertion failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        print("Terminating server...")
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    success = test_endpoints()
    sys.exit(0 if success else 1)
