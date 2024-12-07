class SJFAlgorithm:
    """
    Shortest Job First (SJF) Algorithm for scheduling processes.
    """

    def __init__(self, processes):
        """
        Initialize the algorithm with a list of processes.

        :param processes: List of dictionaries containing process details.
                          Example: [{"id": 1, "arrival_time": 0, "burst_time": 6}, ...]
        """
        self.processes = processes
        self.scheduled_processes = []

    def execute(self):
        """
        Run the SJF scheduling algorithm.
        Sorts processes by arrival time and burst time.
        """
        # Sort by arrival time initially
        self.processes.sort(key=lambda x: x["arrival_time"])

        current_time = 0
        ready_queue = []
        processes_to_schedule = self.processes[:]

        while processes_to_schedule or ready_queue:
            # Add processes that have arrived to the ready queue
            ready_queue.extend(
                [p for p in processes_to_schedule if p["arrival_time"] <= current_time]
            )
            processes_to_schedule = [
                p for p in processes_to_schedule if p not in ready_queue
            ]

            if ready_queue:
                # Sort the ready queue by burst time
                ready_queue.sort(key=lambda x: x["burst_time"])

                # Select the shortest job
                current_process = ready_queue.pop(0)

                # Update current time and log the scheduled process
                start_time = current_time
                current_time += current_process["burst_time"]
                finish_time = current_time

                self.scheduled_processes.append(
                    {
                        "id": current_process["id"],
                        "start_time": start_time,
                        "finish_time": finish_time,
                        "waiting_time": start_time - current_process["arrival_time"],
                        "turnaround_time": finish_time - current_process["arrival_time"],
                    }
                )
            else:
                # If no process is ready, increment the time
                current_time += 1

    def get_results(self):
        """
        Return the results of the SJF scheduling.

        :return: List of scheduled processes with waiting and turnaround times.
        """
        return self.scheduled_processes


class SRTAlgorithm:
    def __init__(self, processes):
        """
        :param processes: لیستی از دیکشنری‌ها شامل اطلاعات هر فرآیند
                         [{'process_name': 'P1', 'arrival_time': 0, 'burst_time': 5},
                          {'process_name': 'P2', 'arrival_time': 1, 'burst_time': 3}, ...]
        """
        self.processes = sorted(processes, key=lambda x: x['arrival_time'])
        self.result = []

    def execute(self):
        """
        اجرای الگوریتم SRT
        :return: لیستی از دیکشنری‌ها شامل زمان‌های اجرا، انتظار و تکمیل برای هر فرآیند
        """
        processes = self.processes
        n = len(processes)
        remaining_time = [p['burst_time'] for p in processes]
        complete = 0
        time = 0
        waiting_time = [0] * n
        turnaround_time = [0] * n
        completed = [False] * n

        while complete < n:
            # پیدا کردن فرآیند با کمترین زمان باقی‌مانده
            idx = -1
            min_remaining_time = float('inf')

            for i in range(n):
                if (not completed[i]) and (processes[i]['arrival_time'] <= time) and (
                        remaining_time[i] < min_remaining_time):
                    min_remaining_time = remaining_time[i]
                    idx = i

            if idx == -1:
                time += 1  # هیچ فرآیندی آماده نیست، بنابراین زمان را افزایش می‌دهیم
                continue

            # کاهش زمان باقی‌مانده فرآیند انتخاب شده
            remaining_time[idx] -= 1

            if remaining_time[idx] == 0:  # اگر فرآیند تمام شد
                completed[idx] = True
                complete += 1
                finish_time = time + 1
                waiting_time[idx] = finish_time - processes[idx]['arrival_time'] - processes[idx]['burst_time']
                turnaround_time[idx] = finish_time - processes[idx]['arrival_time']

            time += 1

        # محاسبه زمان‌های تکمیل و انتظار برای هر فرآیند
        for i in range(n):
            self.result.append({
                'process_name': processes[i]['process_name'],
                'waiting_time': waiting_time[i],
                'turnaround_time': turnaround_time[i],
                'completion_time': waiting_time[i] + turnaround_time[i] + processes[i]['arrival_time']
            })

        return self.result


# algorithms.py
from collections import deque


class RoundRobin:
    def __init__(self, processes, quantum):
        """
        :param processes: لیستی از پردازش‌ها که شامل process_name, arrival_time, burst_time, priority, quantum است
        :param quantum: زمان کوانتوم که در الگوریتم استفاده می‌شود
        """
        self.processes = processes
        self.quantum = quantum

    def execute(self):
        """
        اجرای الگوریتم Round Robin
        :return: نتایج الگوریتم شامل زمان ورود، زمان پایان، زمان اجرای پردازش‌ها و زمان پاسخ
        """
        queue = []
        for process in self.processes:
            queue.append(process)

        time = 0
        result = []
        waiting_times = {}
        turn_around_times = {}
        completed = []

        while queue:
            process = queue.pop(0)
            process_name, arrival_time, burst_time, priority, quantum = process
            remaining_time = burst_time

            if remaining_time > self.quantum:
                # پردازش برای زمان کوانتوم کامل اجرا می‌شود
                time += self.quantum
                remaining_time -= self.quantum
                # پردازش دوباره به صف اضافه می‌شود
                queue.append((process_name, arrival_time, remaining_time, priority, self.quantum))
            else:
                # پردازش تا پایان تمام می‌شود
                time += remaining_time
                waiting_time = time - arrival_time - burst_time
                turn_around_time = time - arrival_time
                waiting_times[process_name] = waiting_time
                turn_around_times[process_name] = turn_around_time
                completed.append(process_name)
                remaining_time = 0

            result.append({
                'process_name': process_name,
                'arrival_time': arrival_time,
                'burst_time': burst_time,
                'waiting_time': waiting_times.get(process_name, 0),
                'turn_around_time': turn_around_times.get(process_name, 0),
                'completion_time': time
            })

        return result

