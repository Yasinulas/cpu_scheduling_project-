class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0
        self.start_time = -1
        self.is_completed = False
        
        # Priority'i sayısala çevir
        if priority.lower() == 'high':
            self.priority_num = 1
        elif priority.lower() == 'normal':
            self.priority_num = 2
        else:  # low
            self.priority_num = 3
    
    def calculate_times(self):
        if self.completion > 0:
            self.turnaround = self.completion - self.arrival
            self.waiting = self.start_time - self.arrival
            if self.waiting < 0:
                self.waiting = 0
        return self
    
    def __str__(self):
        return f"{self.pid}: A={self.arrival}, B={self.burst}, P={self.priority}"