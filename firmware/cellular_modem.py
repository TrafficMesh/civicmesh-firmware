"""LTE modem for evidence upload and heartbeat."""

class CellularModem:
    def upload_incident(self, incident_data: bytes) -> bool:
        """Upload incident to backend."""
        pass
    
    def send_heartbeat(self) -> bool:
        """Send periodic heartbeat."""
        pass
