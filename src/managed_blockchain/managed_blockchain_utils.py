from datetime import datetime

def format_timestamp(timestamp):
    """Converts AWS timestamp to human-readable format."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def handle_errors(error):
    """Logs errors and returns a friendly message."""
    print(f"Error: {error}")
    return {"error": str(error)}
