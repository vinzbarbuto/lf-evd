import pygame
import sys
import threading
import queue

class TrafficSignalUI:
    def __init__(self, controller, screen_size=(1400, 800)):
        self.controller = controller
        self.screen_size = screen_size
        self.signal_coords = [(530, 230), (810, 230), (810, 570), (530, 570)]
        self.timer_coords = [(530, 210), (810, 210), (810, 550), (530, 550)]
        self.message_queue = queue.Queue()  # Queue for preemption messages
        self.init_pygame()
        self.start_message_handler()
        self.running = True  # Control the simulation state

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Traffic Signal Simulation")
        self.background = pygame.image.load("images/intersection.png")
        self.red_signal = pygame.image.load("images/signals/red.png")
        self.yellow_signal = pygame.image.load("images/signals/yellow.png")
        self.green_signal = pygame.image.load("images/signals/green.png")
        self.font = pygame.font.Font(None, 30)

    def start_message_handler(self):
        threading.Thread(target=self.handle_messages, daemon=True).start()

    def handle_messages(self):
        while True:
            signal_number = self.message_queue.get()
            if 0 <= signal_number < self.controller.num_signals:
                threading.Thread(
                    target=self.controller.preemption, args=(signal_number,)
                ).start()

    def step(self):
        """
        Advances the simulation by one step.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Trigger preemption with keys 1, 2, 3, 4
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    signal_number = event.key - pygame.K_1
                    threading.Thread(
                        target=self.controller.preemption, args=(signal_number,)
                    ).start()

        # Draw the background
        self.screen.blit(self.background, (0, 0))

        # Update signals
        with self.controller.lock:
            for i, signal in enumerate(self.controller.signals):
                if i == self.controller.current_green:
                    image = (
                        self.yellow_signal
                        if self.controller.current_yellow
                        else self.green_signal
                    )
                    signal.signalText = (
                        signal.yellow if self.controller.current_yellow else signal.green
                    )
                else:
                    image = self.red_signal
                    signal.signalText = signal.red if signal.red <= 10 else "---"
                self.screen.blit(image, self.signal_coords[i])
                text_surface = self.font.render(
                    str(signal.signalText), True, (255, 255, 255), (0, 0, 0)
                )
                self.screen.blit(text_surface, self.timer_coords[i])

        pygame.display.update()