import pygame
import queue

class TrafficSignalUI:
    def __init__(self, controller, screen_size=(1400, 800)):
        self.controller = controller
        self.screen_size = screen_size
        self.signal_coords = [(530, 230), (810, 280), (810, 570), (480, 550)]
        self.timer_coords = [(510, 297), (810, 260), (810, 550), (545, 583)]
        self.message_queue = queue.Queue()  # Queue for preemption messages
        self.init_pygame()
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

    def step(self):
        """
        Advances the simulation by one step.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                raise SystemExit

        # Draw the background
        self.screen.blit(self.background, (0, 0))

        # Update signals
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
                signal.signalText = signal.red if signal.red <= 10 else "--"
            rotation_angle = [180, 90, 0, 270][i] if i < 4 else 0
            rotated_image = pygame.transform.rotate(image, rotation_angle)
            self.screen.blit(rotated_image, self.signal_coords[i])
            text_surface = self.font.render(
                str(signal.signalText), True, (255, 255, 255), (0, 0, 0)
            )
            self.screen.blit(text_surface, self.timer_coords[i])

        pygame.display.update()