from django.test import TestCase

from models import PingCount

# Create your tests here.

class Ping(TestCase):
    def test_ping(self) -> None:

        # Get the singleton instance (or create it if it doesn't exist)
        counter = PingCount.get_singleton()

        # Atomically increment the count in the database
        new_count = counter.increment_and_save()

        counter = PingCount.get_singleton()

        self.assertEquals(counter.count, 1)
    
        print("test completed")