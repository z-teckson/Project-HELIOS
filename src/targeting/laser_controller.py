"""
Laser controller module for Project HELIOS.
Handles targeting and firing of high-energy laser.
"""

from .atmospheric_comp import calculate_correction_profile


class LaserController:
    def __init__(self, config):
        self.config = config
        self.beam_power = config.get('beam_power', 1.0)
        self.target_lock = False
        self.correction_profile = None
    
    def acquire_target(self, target_coords):
        """Acquire target coordinates and attempt to lock."""
        # Simulate targeting logic
        self.target_coords = target_coords
        self.target_lock = True
        return self.target_lock
    
    def compute_atmospheric_correction(self, sensor_data_path):
        """
        Compute atmospheric correction profile using sensor data.
        
        Args:
            sensor_data_path: Path to atmospheric sensor CSV file.
        """
        # Apply new atmospheric compensation logic here
        self.correction_profile = calculate_correction_profile(sensor_data_path)
        return self.correction_profile
    
    def apply_correction(self, correction_profile=None):
        """Apply atmospheric correction profile to beam steering."""
        profile = correction_profile or self.correction_profile
        if profile:
            # Adjust beam based on correction parameters
            # For now, we'll simulate by printing correction parameters
            print(f"Applying atmospheric correction: gain={profile.get('correction_gain', 1.0)}")
            # In a real system, this would adjust deformable mirrors, beam steering, etc.
        else:
            print("No correction profile available.")
    
    def fire(self):
        """Fire the laser at the locked target."""
        if not self.target_lock:
            raise RuntimeError("No target locked")
        
        # Apply atmospheric correction before firing (new integration point)
        self.apply_correction()
        
        # Simulate firing sequence
        print(f"Firing laser at {self.target_coords} with power {self.beam_power}")
        return True
