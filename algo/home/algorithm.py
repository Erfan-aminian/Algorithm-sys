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
