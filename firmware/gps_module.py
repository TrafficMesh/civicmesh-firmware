"""u-blox NEO-M9N GPS module."""

class GPSModule:
    def get_fix(self) -> dict:
        """Return lat, lon, accuracy."""
        pass
    
    def wait_for_fix(self, timeout: int = 60) -> bool:
        """Wait for GPS lock."""
        pass
