"""OBD-II interface: read vehicle speed and diagnostics."""

class OBDInterface:
    def read_speed(self) -> float:
        """Return vehicle speed in km/h."""
        pass
    
    def read_diagnostics(self) -> dict:
        """Read engine diagnostics."""
        pass
