import pygame

# Initialize Pygame
pygame.init()

# Set the window size
width = 800
height = 600

# Create the window
screen = pygame.display.set_mode((width, height))

# Create variables to store the input text
input_fields = {
    "name": "",
    "age": "",
    "email": ""
}

# Create a variable to track which input field is active
active_field = "name"

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalnum() or event.unicode == " ":
                input_fields[active_field] += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                input_fields[active_field] = input_fields[active_field][:-1]
            elif event.key == pygame.K_RETURN:
                if active_field == "email":
                    print(input_fields)
                    input_fields = {
                        "name": "",
                        "age": "",
                        "email": ""
                    }
                else:
                    active_field = list(input_fields.keys())[list(input_fields.keys()).index(active_field) + 1]

    # Draw the input fields
    pygame.draw.rect(screen, (255, 255, 255), (100, 100, 200, 50))
    pygame.draw.rect(screen, (255, 255, 255), (100, 200, 200, 50))
    pygame.draw.rect(screen, (255, 255, 255), (100, 300, 200, 50))

    # Draw the input text
    font = pygame.font.Font(None, 32)
    text = font.render(input_fields["name"], True, (0, 0, 0))
    screen.blit(text, (110, 110))
    text = font.render(input_fields["age"], True, (0, 0, 0))
    screen.blit(text, (110, 210))
    text = font.render(input_fields["email"], True, (0, 0, 0))
    screen.blit(text, (110, 310))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
