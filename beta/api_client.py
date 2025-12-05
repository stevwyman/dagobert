import time
import threading
import urllib3
from urllib3.util.retry import Retry
from collections import deque

class APIClient:
    _instance = None
    _lock = threading.Lock()
    _api_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(APIClient, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        # --- Rate Limit Config ---
        self.limit = 5
        self.period = 60
        self.request_timestamps = deque()

        # --- Retry Strategy Config ---
        # total=3: Stop after 3 retries
        # backoff_factor=1: Sleep {backoff factor} * (2 ^ ({number of total retries} - 1))
        # status_forcelist: Retry on these HTTP status codes
        retry_strategy = Retry(
            total=3,
            backoff_factor=1, 
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"] # Enable retries for POST too
        )
        
        # Pass the retry strategy to the PoolManager
        self.http = urllib3.PoolManager(retries=retry_strategy)
        
        self._initialized = True
        print("API Client Initialized (Singleton + Rate Limit + Auto-Retry)")

    def _wait_for_slot(self):
        """
        Enforce the 5 calls/minute limit.
        """
        with self._api_lock:
            now = time.time()
            
            # Clean up old timestamps
            while self.request_timestamps and self.request_timestamps[0] < now - self.period:
                self.request_timestamps.popleft()

            # Check limit
            if len(self.request_timestamps) >= self.limit:
                wait_time = (self.request_timestamps[0] + self.period) - now
                if wait_time > 0:
                    print(f"[Rate Limit] Sleeping for {wait_time:.2f}s...")
                    time.sleep(wait_time)
            
            # Record the attempt
            self.request_timestamps.append(time.time())

    def request(self, method, url, **kwargs):
        self._wait_for_slot()
        
        print(f"[{time.strftime('%H:%M:%S')}] {method} {url}")
        
        try:
            # urllib3 will now automatically handle the retries internally
            # before returning the response to you.
            response = self.http.request(method, url, **kwargs)
            return response
            
        except urllib3.exceptions.MaxRetryError as e:
            print(f"Max retries exceeded: {e}")
            return None
        except urllib3.exceptions.HTTPError as e:
            print(f"Network error: {e}")
            return None

# --- Testing the Retry Logic ---
if __name__ == "__main__":
    client = APIClient()

    # To test this, we need a URL that returns a 500 error.
    # httpbin.org/status/500 simulates a server failure.
    print("Attempting request to a failing endpoint (expecting retries)...")
    
    start_time = time.time()
    response = client.request('GET', 'https://httpbin.org/status/500')
    end_time = time.time()
    
    # If retries worked, this request should have taken a few seconds
    # (due to the backoff factor sleeping between attempts)
    print(f"Request took {end_time - start_time:.2f} seconds.")
    
    if response:
        print(f"Final Status Code: {response.status}")