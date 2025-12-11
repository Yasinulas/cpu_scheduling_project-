import queue

class Scheduler:
    def __init__(self):
        self.timeline = []
    
    def fcfs(self, processes):
        self.timeline = []
        sorted_procs = sorted(processes, key=lambda x: x.arrival)
        current_time = 0
        
        for p in sorted_procs:
            if current_time < p.arrival:
                self.timeline.append(f"[{current_time}] - IDLE - [{p.arrival}]")
                current_time = p.arrival
            
            p.start_time = current_time
            self.timeline.append(f"[{current_time}] - {p.pid} - [{current_time + p.burst}]")
            
            p.completion = current_time + p.burst
            p.is_completed = True
            current_time = p.completion
        
        return self.timeline, sorted_procs
    
    def sjf_non_preemptive(self, processes):
        self.timeline = []
        procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
        current_time = 0
        completed = []
        
        while len(completed) < len(procs):
            ready = [p for p in procs if p.arrival <= current_time and not p.is_completed]
            
            if ready:
                shortest = min(ready, key=lambda x: x.burst)
                shortest.start_time = current_time
                
                self.timeline.append(f"[{current_time}] - {shortest.pid} - [{current_time + shortest.burst}]")
                
                shortest.completion = current_time + shortest.burst
                shortest.is_completed = True
                current_time = shortest.completion
                completed.append(shortest)
            else:
                next_arrival = min(p.arrival for p in procs if not p.is_completed)
                self.timeline.append(f"[{current_time}] - IDLE - [{next_arrival}]")
                current_time = next_arrival
        
        return self.timeline, completed
    
    def sjf_preemptive(self, processes):
        self.timeline = []
        procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
        current_time = 0
        last_pid = None
        last_start = 0
        
        while any(p.remaining > 0 for p in procs):
            ready = [p for p in procs if p.arrival <= current_time and p.remaining > 0]
            
            if ready:
                shortest = min(ready, key=lambda x: x.remaining)
                
                if last_pid != shortest.pid and last_pid is not None:
                    self.timeline.append(f"[{last_start}] - {last_pid} - [{current_time}]")
                    last_start = current_time
                
                last_pid = shortest.pid
                if shortest.start_time == -1:
                    shortest.start_time = current_time
                
                shortest.remaining -= 1
                current_time += 1
                
                if shortest.remaining == 0:
                    shortest.completion = current_time
                    shortest.is_completed = True
                    self.timeline.append(f"[{last_start}] - {shortest.pid} - [{current_time}]")
                    last_pid = None
                    last_start = current_time
            else:
                if last_pid is not None:
                    self.timeline.append(f"[{last_start}] - {last_pid} - [{current_time}]")
                    last_pid = None
                
                next_arrival = min(p.arrival for p in procs if p.remaining > 0)
                self.timeline.append(f"[{current_time}] - IDLE - [{next_arrival}]")
                current_time = next_arrival
                last_start = current_time
        
        return self.timeline, procs
    
    def round_robin(self, processes, quantum=4):
        self.timeline = []
        procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
        ready_queue = queue.Queue()
        current_time = 0
        last_pid = None
        last_start = 0
        completed = []
        
        initial = sorted([p for p in procs if p.arrival <= current_time], key=lambda x: x.arrival)
        for p in initial:
            ready_queue.put(p)
        
        while len(completed) < len(procs):
            if not ready_queue.empty():
                current_proc = ready_queue.get()
                
                if last_pid != current_proc.pid and last_pid is not None:
                    self.timeline.append(f"[{last_start}] - {last_pid} - [{current_time}]")
                
                last_pid = current_proc.pid
                if current_proc.start_time == -1:
                    current_proc.start_time = current_time
                
                exec_time = min(quantum, current_proc.remaining)
                last_start = current_time
                current_time += exec_time
                current_proc.remaining -= exec_time
                
                new_arrivals = [p for p in procs if p.arrival > current_time - exec_time and p.arrival <= current_time and not p.is_completed and not any(p2.pid == p.pid for p2 in list(ready_queue.queue))]
                for p in sorted(new_arrivals, key=lambda x: x.arrival):
                    ready_queue.put(p)
                
                if current_proc.remaining == 0:
                    current_proc.completion = current_time
                    current_proc.is_completed = True
                    completed.append(current_proc)
                    self.timeline.append(f"[{last_start}] - {current_proc.pid} - [{current_time}]")
                    last_pid = None
                else:
                    ready_queue.put(current_proc)
            else:
                if last_pid is not None:
                    self.timeline.append(f"[{last_start}] - {last_pid} - [{current_time}]")
                    last_pid = None
                
                remaining_procs = [p for p in procs if not p.is_completed]
                if remaining_procs:
                    next_arrival = min(p.arrival for p in remaining_procs)
                    self.timeline.append(f"[{current_time}] - IDLE - [{next_arrival}]")
                    current_time = next_arrival
                    last_start = current_time
                    
                    new_arrivals = [p for p in procs if p.arrival <= current_time and not p.is_completed and not any(p2.pid == p.pid for p2 in list(ready_queue.queue))]
                    for p in sorted(new_arrivals, key=lambda x: x.arrival):
                        ready_queue.put(p)
        
        return self.timeline, procs
    
    def priority_non_preemptive(self, processes):
        self.timeline = []
        procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
        current_time = 0
        completed = []
        
        while len(completed) < len(procs):
            ready = [p for p in procs if p.arrival <= current_time and not p.is_completed]
            
            if ready:
                highest = min(ready, key=lambda x: x.priority_num)
                highest.start_time = current_time
                
                self.timeline.append(f"[{current_time}] - {highest.pid} - [{current_time + highest.burst}]")
                
                highest.completion = current_time + highest.burst
                highest.is_completed = True
                current_time = highest.completion
                completed.append(highest)
            else:
                next_arrival = min(p.arrival for p in procs if not p.is_completed)
                self.timeline.append(f"[{current_time}] - IDLE - [{next_arrival}]")
                current_time = next_arrival
        
        return self.timeline, completed
    
    def priority_preemptive(self, processes):
        self.timeline = []
        procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
        current_time = 0
        last_pid = None
        last_start = 0
        
        while any(p.remaining > 0 for p in procs):
            ready = [p for p in procs if p.arrival <= current_time and p.remaining > 0]
            
            if ready:
                highest = min(ready, key=lambda x: x.priority_num)
                
                if last_pid != highest.pid and last_pid is not None:
                    self.timeline.append(f"[{last_start}] - {last_pid} - [{current_time}]")
                    last_start = current_time
                
                last_pid = highest.pid
                if highest.start_time == -1:
                    highest.start_time = current_time
                
                highest.remaining -= 1
                current_time += 1
                
                if highest.remaining == 0:
                    highest.completion = current_time
                    highest.is_completed = True
                    self.timeline.append(f"[{last_start}] - {highest.pid} - [{current_time}]")
                    last_pid = None
                    last_start = current_time
            else:
                if last_pid is not None:
                    self.timeline.append(f"[{last_start}] - {last_pid} - [{current_time}]")
                    last_pid = None
                
                next_arrival = min(p.arrival for p in procs if p.remaining > 0)
                self.timeline.append(f"[{current_time}] - IDLE - [{next_arrival}]")
                current_time = next_arrival
                last_start = current_time
        
        return self.timeline, procs