import pygame
import sys
import random
import os
from pygame.locals import *
import time

# Initialize Pygame
pygame.init()

# Load icon
icon = pygame.image.load("assets/icon.ico")

# Set icon
pygame.display.set_icon(icon)

# Screen dimensions
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 700

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
SOFT_BLACK =(64,64,64)
SOFT_WHITE = (200,200,200)


# Game constants
GRAVITY = 0.4
JUMP_STRENGTH = -8 
PIPE_SPEED = -3
PIPE_GAP = 180

# Max pipe height
MIN_PIPE_HEIGHT = 100
MAX_PIPE_HEIGHT = SCREEN_HEIGHT - 300

AB_WIDTH = 320
AB_HEIGHT = 450

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load assets
bird_image = pygame.image.load("birds/b0.png")
bird_image = pygame.transform.scale(bird_image, (40, 40))
title_image = pygame.image.load("assets/txt.png")
title_image = pygame.transform.scale(title_image, (300, 80))
over_image = pygame.image.load("assets/game-over.png")
over_image = pygame.transform.scale(over_image, (400, 300))
dark_image = pygame.image.load("assets/dark-mode.png")
dark_image = pygame.transform.scale(dark_image, (30, 30))
light_image = pygame.image.load("assets/light-mode.png")
light_image = pygame.transform.scale(light_image, (30, 30))
my_image = pygame.image.load("assets/My.png")
my_image = pygame.transform.scale(my_image, (120, 120))

# Load settings image
settings_image = pygame.image.load("assets/settings.png")
settings_image = pygame.transform.scale(settings_image, (40, 40))

# Load close image
close_image = pygame.image.load("assets/close.png")
close_image = pygame.transform.scale(close_image, (30, 30))

# Backgrounds
light_background = pygame.image.load("assets/background-light.png")
light_background = pygame.transform.scale(light_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
dark_background = pygame.image.load("assets/background-dark.png")
dark_background = pygame.transform.scale(dark_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
is_dark_mode = False
background_image = light_background

# High Score File
HIGH_SCORE_FILE = "highscore.txt"

PIPE_WIDTH = 60  # Increased width from 50 to 70
PIPE_EDGE_RADIUS = 15  # Controls roundness of corners

def load_high_score():
    """Load high score from file. If file does not exist, return 0."""
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0  # If file is empty or corrupted, return 0
    return 0  # Default high score

def save_high_score(score):
    """Save high score to file if it's higher than the previous high score."""
    high_score = load_high_score()
    if score > high_score:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))  # Save new high score

# Bird class
class Bird:
    def __init__(self, image):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.image = image  # Use the passed image

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 40)

    def change_image(self, new_image):
        self.image = new_image  # Change the bird image

# Pipe class
class Pipe:   
    def __init__(self, x):
        self.x = x
        self.height = random.randint(MIN_PIPE_HEIGHT, MAX_PIPE_HEIGHT)  # Limited range for playability
        self.gap = PIPE_GAP  

        # Define top and bottom pipe rectangles with increased width
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)  
        self.bottom_rect = pygame.Rect(self.x, self.height + self.gap, PIPE_WIDTH, SCREEN_HEIGHT - (self.height + self.gap))  

    def update(self):
        self.x += PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        # Draw top pipe with only the top two corners rounded
        pygame.draw.rect(screen, GREEN, self.top_rect, border_bottom_left_radius=PIPE_EDGE_RADIUS, border_bottom_right_radius=PIPE_EDGE_RADIUS)  
        
        # Draw bottom pipe with only the bottom two corners rounded
        pygame.draw.rect(screen, GREEN, self.bottom_rect, border_top_left_radius=PIPE_EDGE_RADIUS, border_top_right_radius=PIPE_EDGE_RADIUS)  

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH  # Adjust for new pipe width

class Sidebar:
    def __init__(self):
        self.width = 200
        self.height = SCREEN_HEIGHT
        self.x = -self.width  # Start off-screen
        self.y = 0
        self.speed = 10
        self.visible = False
        self.border_radius = 15  # Radius for rounded corners
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((64, 64, 64, 128))  # Semi-transparent background (alpha = 128)
        self.change_bird_box_visible = False  # New attribute to control visibility of the bird selection box

    def draw(self):
        if self.visible:
            if self.x < 0:
                self.x += self.speed

            pygame.draw.rect(
                screen, 
                (64, 64, 64, 128),  # Semi-transparent color
                (self.x, self.y, self.width, self.height), 
                border_top_right_radius=self.border_radius,
                border_bottom_right_radius=self.border_radius  # Rounded corners
            )

            font = pygame.font.Font(None, 24)

            # Draw options
            change_bird_text = font.render("Change Bird", True, WHITE)
            about_text = font.render("About", True, WHITE)
            reset_score_text = font.render("Reset High Score", True, WHITE)

            screen.blit(change_bird_text, (self.x + 20, 100))
            screen.blit(about_text, (self.x + 20, 150))
            screen.blit(reset_score_text, (self.x + 20, 200))
            screen.blit(close_image, (self.x + 160, 10))
            screen.blit(settings_image, (10, 10))

    def toggle(self):
        self.visible = not self.visible
        if not self.visible:
            self.x = -self.width

    def is_clicked(self, pos):
        if self.visible:
            return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height
        return False

def load_bird_images():
    bird_images = []
    birds_folder = "birds"
    if os.path.exists(birds_folder):
        for filename in os.listdir(birds_folder):
            if filename.endswith(".png"):
                bird_image = pygame.image.load(os.path.join(birds_folder, filename))
                bird_image = pygame.transform.scale(bird_image, (75, 60))  # Resize to match the game's bird size
                bird_images.append(bird_image)
    return bird_images

def show_bird_selection_box(bird_images):
    box_width = 300
    box_height = 450
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = (SCREEN_HEIGHT - box_height) // 2

    running = True
    selected_bird = bird_images[0]  # Default to the first bird image

    while running:
        screen.blit(background_image, (0, 0))

        # Draw the selection box
        pygame.draw.rect(screen, (64, 64, 64, 200), (box_x, box_y, box_width, box_height), border_radius=15)

        # Draw bird images in the box
        for i, bird_image in enumerate(bird_images):
            bird_x = box_x + 20 + (i % 3) * 90  # Arrange birds in a grid
            bird_y = box_y + 20 + (i // 3) * 90

            # Draw the bird image
            screen.blit(bird_image, (bird_x, bird_y))

            # Draw a border around the selected bird
            if selected_bird == bird_image:
                pygame.draw.rect(screen, SOFT_WHITE, (bird_x - 5, bird_y - 10, 90, 80), 3, border_radius=10)  # Border around the selected bird

        # Draw the "Change" button
        change_button_rect = pygame.Rect(box_x + 100, box_y + 385, 100, 40)
        pygame.draw.rect(screen, GRAY, change_button_rect, border_radius=30)
        font = pygame.font.Font(None, 24)
        change_text = font.render("Change", True, WHITE)
        screen.blit(change_text, (box_x + 116, box_y + 398))

        # Check if a bird is clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, bird_image in enumerate(bird_images):
            bird_x = box_x + 20 + (i % 3) * 90
            bird_y = box_y + 20 + (i // 3) * 90
            if bird_x - 10 <= mouse_x <= bird_x + 75 and bird_y - 10 <= mouse_y <= bird_y + 60:
                if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                    selected_bird = bird_image  # Update the selected bird

        # Check if the "Change" button is clicked
        if change_button_rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                if selected_bird:
                    running = False  # Close the selection box and return the selected bird

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()
        clock.tick(60)

    return selected_bird

def about_screen():
    """Display the About Screen."""
    about_font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    # About Screen content
    about_title = about_font.render("About Flappy Bird", True, WHITE)
    created_by = small_font.render("Created by Subham", True, WHITE)
    version = small_font.render("Version 1.0", True, WHITE)
    instructions = small_font.render("Press ESC to go back", True, WHITE)

    # Create a semi-transparent background for the About Screen
    about_background = pygame.Surface((AB_WIDTH, AB_HEIGHT), pygame.SRCALPHA)
    about_background.fill((64, 64, 64, 200))  # Semi-transparent background

    running = True
    while running:
        

        pygame.draw.rect(
            screen,  # Draw the rectangle on the main screen, not on `about_background`
            (64, 64, 64, 200),  # Semi-transparent dark color
        pygame.Rect(
                    (SCREEN_WIDTH - AB_WIDTH) // 2 + 100, (SCREEN_HEIGHT - AB_HEIGHT) // 2,  # Position
                    AB_WIDTH, AB_HEIGHT  # Width & Height
                    ),border_radius=15  # Rounded corners
        )


        # Draw the About Screen content
        screen.blit(about_title, ((SCREEN_WIDTH - about_title.get_width()) // 2 + 100, (SCREEN_HEIGHT - AB_HEIGHT) // 2 + 70))
        screen.blit(created_by, ((SCREEN_WIDTH - created_by.get_width()) // 2 + 100, (SCREEN_HEIGHT - AB_HEIGHT) // 2 + 150))
        screen.blit(version, ((SCREEN_WIDTH - version.get_width()) // 2 + 100, (SCREEN_HEIGHT - AB_HEIGHT) // 2 + 200))
        screen.blit(my_image, ((SCREEN_WIDTH - my_image.get_width()) // 2 + 100, (SCREEN_HEIGHT - AB_HEIGHT) // 2 + 250))
        screen.blit(instructions, ((SCREEN_WIDTH - instructions.get_width()) // 2 + 100, (SCREEN_HEIGHT - AB_HEIGHT) // 2 + 400))
        screen.blit(close_image, ((SCREEN_WIDTH - AB_WIDTH) // 2 + 100 + 280, (SCREEN_HEIGHT - AB_HEIGHT) // 2 + 10))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 500 <= x <= 530 and 135 <= y <= 165:
                    return

        pygame.display.flip()
        clock.tick(60)

def toggle_background():
    global is_dark_mode, background_image
    is_dark_mode = not is_dark_mode
    background_image = dark_background if is_dark_mode else light_background

def draw_toggle_button():
    pygame.draw.rect(screen, WHITE if is_dark_mode else SOFT_BLACK, (SCREEN_WIDTH - 70, 10, 60, 40), border_radius=70)
    screen.blit(light_image if is_dark_mode else dark_image, (SCREEN_WIDTH - 55, 15))

# Start screen function
def start_screen():
    blink = True
    blink_counter = 0
    instructions_font = pygame.font.Font(None, 48)
    created_by_text = pygame.font.Font(None, 28).render("CREATED BY SUBHAM", True, WHITE)

    sidebar = Sidebar()
    reset_message = None
    reset_message_start_time = 0
    reset_message_duration = 2

    bird_images = load_bird_images()  # Load all bird images
    selected_bird = bird_image  # Default to the initial bird image

    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(title_image, (SCREEN_WIDTH // 2 - title_image.get_width() // 2, SCREEN_HEIGHT // 3 + 30))

        if blink:
            instructions_text = instructions_font.render("Press SPACE to Start", True, WHITE)
            screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 95))

        screen.blit(settings_image, (10, 10))
        sidebar.draw()
        draw_toggle_button()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rect = pygame.Rect(SCREEN_WIDTH - 100, 10, 90, 40)

        screen.blit(created_by_text, (SCREEN_WIDTH - created_by_text.get_width() - 10, 680))

        if button_rect.collidepoint(mouse_x, mouse_y) or (10 <= mouse_x <= 40 and 10 <= mouse_y <= 40):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if reset_message and time.time() - reset_message_start_time < reset_message_duration:
            confirmation_font = pygame.font.Font(None, 36)
            confirmation_text = confirmation_font.render(reset_message, True, WHITE)
            screen.blit(confirmation_text, (SCREEN_WIDTH // 2 - confirmation_text.get_width() // 2, 60))
        else:
            reset_message = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                return selected_bird  # Return the selected bird image

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if 10 <= x <= 40 and 10 <= y <= 40:
                    sidebar.toggle()
                if sidebar.is_clicked((x, y)):
                    if 100 <= y <= 130:
                        selected_bird = show_bird_selection_box(bird_images)  # Update the selected bird image
                    elif 150 <= y <= 180:
                        sidebar.toggle()
                        about_screen()
                    elif 200 <= y <= 230:
                        with open(HIGH_SCORE_FILE, "w") as file:
                            file.write("0")
                        sidebar.toggle()
                        reset_message = "Reset Successfull"
                        reset_message_start_time = time.time()
                    if 160 <= x <= 190 and 10 <= y <= 40:
                        sidebar.toggle()
                if button_rect.collidepoint(x, y):
                    toggle_background()

        blink_counter += 1
        if blink_counter >= 30:
            blink = not blink
            blink_counter = 0

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(score):
    """Display Game Over screen and show high score. Allow restart or quit."""
    high_score = load_high_score()
    
    # Check if the current score is a new high score
    if score > high_score:
        save_high_score(score)  # Update high score
        high_score = score  # Update locally

    small_font = pygame.font.Font(None, 36)

    blink1 = True
    score_text = small_font.render(f"Score: {score}", True, BLACK)
    high_score_text = small_font.render(f"High Score: {high_score}", True, BLACK)  # Show high score

    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(over_image, (SCREEN_WIDTH // 2 - over_image.get_width() // 2, SCREEN_HEIGHT // 3 - 140))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3 + 50))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 3 + 80))  # Display high score
        if blink1:
            restart_text = small_font.render("Press ENTER to Restart", True, BLACK)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart game
                    return True  
                if event.key == pygame.K_ESCAPE:  # Exit game
                    pygame.quit()
                    sys.exit()

        blink1 = not blink1
        clock.tick(2)

# Main game loop
def main():
    while True:
        selected_bird_image = start_screen()  # Get the selected bird image
        birdT = pygame.transform.scale(selected_bird_image, (40, 40))
        bird = Bird(birdT)  # Pass the selected bird image to the Bird instance
        pipes = [Pipe(SCREEN_WIDTH + i * 200) for i in range(2)]
        score = 0
        high_score = load_high_score()
        running = True

        while running:
            screen.blit(background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.jump()

            bird.update()

            for pipe in pipes:
                pipe.update()
                pipe.draw()

            bird.draw()

            if pipes and pipes[0].is_off_screen():
                pipes.pop(0)
                last_pipe_x = pipes[-1].x if pipes else SCREEN_WIDTH
                pipes.append(Pipe(last_pipe_x + 300))
                score += 1

            for pipe in pipes:
                if bird.get_rect().colliderect(pipe.top_rect) or bird.get_rect().colliderect(pipe.bottom_rect):
                    running = False

            if bird.y > SCREEN_HEIGHT or bird.y < 0:
                running = False

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)

            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 50))

            pygame.display.flip()
            clock.tick(60)

        if not game_over_screen(score):
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
