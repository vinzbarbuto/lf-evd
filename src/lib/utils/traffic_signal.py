import random
import threading
import queue

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""

class TrafficSignalController:
    def __init__(self, num_signals, random_timer=False, timer_range=(10, 20), default_timers=None, time_extension=10):
        """
        Initializes the traffic signal controller.
        """
        self.preemption_queue = queue.Queue()
        self.num_signals = num_signals
        self.random_timer = random_timer
        self.timer_range = timer_range
        self.signals = []
        self.preempted = False  # Indicates if preemption is active
        self.current_green = 0
        self.next_green = 1
        self.current_yellow = 0
        self.default_timers = default_timers or {
            "green": [15, 15, 15, 15],
            "yellow": 5,
            "red": 150,
        }
        self.time_extension = time_extension
        self.lock = threading.Lock()
        self.initialize_signals()

    def initialize_signals(self):
        """
        Initializes the traffic signals with the specified timers.
        """
        min_time, max_time = self.timer_range
        for i in range(self.num_signals):
            green = random.randint(min_time, max_time) if self.random_timer else self.default_timers["green"][i]
            yellow = self.default_timers["yellow"]
            red = self.default_timers["red"]
            self.signals.append(TrafficSignal(red, yellow, green))

    def manage_signals(self):
        """
        Handles a single step of the traffic signal cycle, including the current phase and signal switch.
        This method is intended to be called periodically.
        """
        with self.lock:
            # If preemption is active, skip this step
            if self.preempted:
                return
            
            # Handle green phase
            if self.signals[self.current_green].green > 1:
                self.signals[self.current_green].green -= 1
                return  # Continue green phase in the next step
            
            # Handle yellow phase
            if self.current_yellow == 0:
                self.current_yellow = 1
                return  # Transition to yellow phase
            
            if self.signals[self.current_green].yellow > 1:
                self.signals[self.current_green].yellow -= 1
                return  # Continue yellow phase in the next step
            
            # End of yellow phase, reset and switch to next signal
            self.current_yellow = 0
            
            self.current_green = self.next_green
            current_signal = self.signals[self.current_green]
            
            if self.random_timer:
                current_signal.green = random.randint(*self.timer_range)
            else:
                current_signal.green = self.default_timers["green"][self.current_green]
            current_signal.yellow = self.default_timers["yellow"]
            current_signal.red = self.default_timers["red"]

            # Update to the next green signal
            if not self.preemption_queue.empty():
                preempted = self.preemption_queue.get_nowait()
                if preempted != self.current_green:
                    self.next_green = preempted % self.num_signals
                else:
                    self.next_green = (self.current_green + 1) % self.num_signals
            else:
                self.next_green = (self.current_green + 1) % self.num_signals

            self.signals[self.next_green].red = current_signal.yellow + current_signal.green
            
    def preemption(self, signal_number):
        """
        Preempts the current signal and switches to the specified signal.
        """
        with self.lock:# Pause the signal management loop
            self.preempted = True

            current = self.signals[self.current_green]
            if signal_number == self.current_green: # Green phase extension
                if self.current_yellow == 0:
                    current.green += self.time_extension
                    current.red += current.yellow + self.time_extension
                    for i in range(self.num_signals):
                        if i != self.current_green:
                            self.signals[i].red += self.time_extension
                else:
                    current.yellow += self.time_extension
                    current.red += self.time_extension
                    for i in range(self.num_signals):
                        if i != self.current_green:
                            self.signals[i].red += self.time_extension
            else: # Red truncation
                current.green = 0
                self.preemption_queue.put((self.current_green + 1) % self.num_signals)
                self.next_green = signal_number

            # Resume the signal management loop
            self.preempted = False 
