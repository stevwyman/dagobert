from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from .models import PingCount

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@require_GET
def ping_view(request):
    """
    Handles a GET request, increments the global ping counter,
    and returns the updated count.
    """
    try:
        # Get the singleton instance (or create it if it doesn't exist)
        counter = PingCount.get_singleton()

        # Atomically increment the count in the database
        new_count = counter.increment_and_save()

        return JsonResponse({
            "status": "success",
            "message": "Ping count incremented.",
            "total_pings": new_count
        })

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred during ping_view: {e}")
        return JsonResponse({
            "status": "error",
            "message": "Could not process the ping request."
        }, status=500)
    
@require_GET
def status_view(request):
    """
    Handles a GET request to display the current total ping count.
    """
    try:
        # Retrieve the current count, ensuring the singleton exists
        counter = PingCount.get_singleton()
        
        return JsonResponse({
            "status": "ok",
            "total_pings": counter.count,
            "last_updated": counter.last_updated.isoformat() if counter.last_updated else None
        })
    except Exception as e:
        print(f"An error occurred during status_view: {e}")
        return JsonResponse({
            "status": "error",
            "message": "Could not retrieve the ping status."
        }, status=500)