
import pygame
import sys
import os
from button import Button  # Import  Button class
from math import sin, cos, radians
from random import choice, randrange, uniform
from game import *


# Initialize  pygame engine
pygame.init()

# Initialize  window
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# Load  background image
BG = pygame.image.load(os.path.join(os.path.dirname(__file__), "assets/Background.png"))

# Function to get font and size of button/menu fonts


def get_font(size):
    return pygame.font.Font(os.path.join(os.path.dirname(__file__),"assets/font.ttf"), size)

######################################################################################
# Function to handle PLAY1 screen/2D rendring


def PLAY1():

    # Define a class for animated symbols
    class Symbol:
        def __init__(self, angle, radius):
            self.angle = angle
            self.radius = radius
            self.speed = 0.5  # Speed of rotation
            self.value = choice(green_katakana)  # Random initial symbol
            self.interval = 10  # Interval to change symbol

        def draw(self, color):
            frames = pygame.time.get_ticks()    # Get current time
        # Change symbol if interval is reached
            if not frames % self.interval:
                self.value = choice(green_katakana if color ==
                                    'green' else lightgreen_katakana)
            self.angle += self.speed  # Update rotation angle
            self.x = WIDTH // 2 + int(self.radius * cos(radians(self.angle)))
            self.y = HEIGHT // 2 + int(self.radius * sin(radians(self.angle)))
            surface.blit(self.value, (self.x, self.y))
    #############################################################################
    # Initialize screen and surface
    RES = WIDTH, HEIGHT = 1280, 720
    FONT_SIZE = 40
    alpha_value = 0
    screen = pygame.display.set_mode(RES)
    surface = pygame.Surface(RES)
    surface.set_alpha(alpha_value)
    clock = pygame.time.Clock()

    # Create lists of characters and their corresponding rendered fonts
    katakana = [chr(int('0x30A0', 16) + i) for i in range(96)]
    font = pygame.font.Font(os.path.join(os.path.dirname(__file__),'assets/MSMINCHO.ttf'), FONT_SIZE)
    green_katakana = [font.render(
        char, True, (40, randrange(160, 256), 40)) for char in katakana]
    lightgreen_katakana = [font.render(
        char, True, pygame.Color('lightgreen')) for char in katakana]

    chain_count = 8
    symbol_count = 25

    symbol_chains = []

    # Create multiple symbol chains
    for chain_index in range(chain_count):
        radius = uniform(50, min(WIDTH, HEIGHT) // 2)
        symbols = [Symbol(i * (360 / symbol_count), radius)
                   for i in range(symbol_count)]
        symbol_chains.append(symbols)
    #############################################################################

    class RotatingColorChangingCircle:
        def __init__(self):
            self.angle = 0
            self.speed = 1  # Adjust the rotation speed as needed
            self.radius = 50
            self.color = pygame.Color(255, 0, 0)  # Initial color

        def update(self):
            self.angle += self.speed
            normalized_sine = (sin(radians(self.angle)) + 1) / \
                2  # Normalize sine to [0, 1]
            # Normalize cosine to [0, 1]
            normalized_cosine = (cos(radians(self.angle)) + 1) / 2
            self.color.r = int(255 * normalized_sine)  # Scale to [0, 255]
            self.color.g = int(255 * normalized_cosine)  # Scale to [0, 255]

        def draw(self):
            center = ((WIDTH+40) // 2, (HEIGHT+30) // 2)
            pygame.draw.circle(surface, self.color, center, self.radius)

    rotating_circle = RotatingColorChangingCircle()
    #############################################################################

    class RotatingText:
        def __init__(self, text, font_size):
            self.angle = 0
            self.speed = 1  # Adjust the rotation speed as needed
            self.font = get_font(font_size)
            self.text_surface = self.font.render(
                text, True, pygame.Color("white"))

        def update(self):
            self.angle += self.speed

        def draw(self):
            rotated_text = pygame.transform.rotate(
                self.text_surface, self.angle)
            text_rect = rotated_text.get_rect(
                center=((WIDTH+30) // 2, (HEIGHT+30) // 2))
            surface.blit(rotated_text, text_rect)

    rotating_circle = RotatingColorChangingCircle()

    # Initialize rotating "BCT" text
    rotating_text_BCT = RotatingText("BCT", 60)
    #############################################################################
    # Game loop
    while True:
        # Get mouse position
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Fill the screen with black
        SCREEN.fill("black")
        screen.blit(surface, (0, 0))
        surface.fill(pygame.Color('black'))

        # Create and update the BACK button
        PLAY_BACK = Button(image=None, pos=(640, 650),
                           text_input="BACK", font=get_font(50), base_color="White", hovering_color="Green")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        # Draw animated symbols
        for symbols in symbol_chains:
            for symbol in symbols:
                symbol.draw('green')

        # Update and draw rotating circle
        rotating_circle.update()
        rotating_circle.draw()

        # Update and draw  rotating "BCT" text
        rotating_text_BCT.update()
        rotating_text_BCT.draw()

        # Update  alpha value for fading effect
        if not pygame.time.get_ticks() % 20 and alpha_value < 170:
            alpha_value += 6
            surface.set_alpha(alpha_value)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        # Update  display
        pygame.display.update()
######################################################################################
# Function to handle the OPTIONS screen


def PLAY2():
    while True:
        # Get mouse position
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Fill the screen with white
        SCREEN.fill("white")

        # Display the OPTIONS text
        myApp = App()

        # Update the display
        pygame.display.update()

######################################################################################
# Function to handle the main menu


def main_menu():
    while True:
        # Display background image
        SCREEN.blit(BG, (0, 0))

        # Get mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Display menu
        MENU_TEXT = get_font(100).render("Screen Saver", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        ABOUT_TEXT = get_font(50).render(
            "BY Subham And Utsav", True, "#b68f40")
        ABOUT_RECT = ABOUT_TEXT.get_rect(center=(640, 650))

        # Create buttons
        PLAY1_BUTTON = Button(image=pygame.image.load(os.path.join(os.path.dirname(__file__),"assets/Play Rect.png")), pos=(640, 250),
                              text_input="2D SS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        PLAY2_BUTTON = Button(image=pygame.image.load(os.path.join(os.path.dirname(__file__),"assets/Play Rect.png")), pos=(640, 400),
                              text_input="3D SS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(os.path.join(os.path.dirname(__file__),"assets/Quit Rect.png")), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Display menu text and update button colors
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(ABOUT_TEXT, ABOUT_RECT)
        for button in [PLAY1_BUTTON, PLAY2_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    PLAY1()  # Call the PLAY1 function
                if PLAY2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    PLAY2()  # Call the PLAY2 function
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Update the display
        pygame.display.update()


######################################################################################
# Start the main menu loop
main_menu()
