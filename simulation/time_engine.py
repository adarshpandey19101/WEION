
# simulation/time_engine.py

class TimeEngine:
    """
    Phase 36: Time Compression Engine ⏳
    Target: 1 second real-time = 5–20 years simulated.
    """
    
    def __init__(self, start_year=2025, years_per_step=5):
        self.start_year = start_year
        self.year = start_year
        self.steps = 0
        self.years_per_step = years_per_step
        self.epoch = "INFORMATION_AGE"
    
    def advance(self):
        """
        Moves time forward.
        """
        self.steps += 1
        self.year += self.years_per_step
        self._check_epoch_shift()
        return self.year

    def _check_epoch_shift(self):
        """
        Determines if a major civilization shift occurred based on time.
        """
        if self.year > 2045 and self.epoch == "INFORMATION_AGE":
            self.epoch = "INTELLIGENCE_AGE"
        elif self.year > 2100 and self.epoch == "INTELLIGENCE_AGE":
            self.epoch = "POST_SCARCITY_AGE"
        elif self.year > 2500 and self.epoch == "POST_SCARCITY_AGE":
            self.epoch = "INTERSTELLAR_AGE"
        elif self.year > 5000:
            self.epoch = "TRANSCENDENT_AGE"

    def get_status(self):
        return {
            "year": self.year,
            "epoch": self.epoch,
            "steps": self.steps
        }
