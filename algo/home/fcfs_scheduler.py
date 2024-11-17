# fcfs_scheduler.py
class FcfsScheduler:
    def __init__(self, processes):
        self.processes = processes
        self.results = []

    def calculate(self):
        start_time = 0
        print(f"Processes to schedule: {self.processes}")  # نمایش داده‌های ورودی
        for idx, (arrival_time, burst_time) in enumerate(self.processes):
            print(f"Processing: Arrival Time = {arrival_time}, Burst Time = {burst_time}")  # دیباگ هر پردازش
            start_time = max(start_time, arrival_time)
            finish_time = start_time + burst_time
            wait_time = start_time - arrival_time
            turnaround_time = finish_time - arrival_time
            self.results.append({
                'process': idx + 1,
                'arrival_time': arrival_time,
                'burst_time': burst_time,
                'start_time': start_time,
                'finish_time': finish_time,
                'wait_time': wait_time,
                'turnaround_time': turnaround_time,
            })
            start_time = finish_time
        print(f"Calculated Results: {self.results}")  # نمایش نتایج محاسبات

    def get_results(self):
        return self.results
