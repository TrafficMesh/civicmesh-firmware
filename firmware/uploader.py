"""Compress, encrypt, and queue incidents for upload."""

class Uploader:
    def queue_incident(self, incident: dict):
        """Add to upload queue."""
        pass
    
    def compress(self, data: bytes) -> bytes:
        """Compress incident data."""
        pass
