import pygame
import sys
import json
import os
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions and grid settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 35
GRID_WIDTH, GRID_HEIGHT = 100, 100  # Grid dimensions
NUM_LAYERS = 9  # Maximum number of layers (1-9)

# Load tile images dynamically from the assets folder
ASSETS_FOLDER = "assets"
TILE_IMAGES = [pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)]  # First index for "empty" tiles
tile_names = ["empty"]  # Keep track of tile names for debugging

for filename in sorted(os.listdir(ASSETS_FOLDER)):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        tile_path = os.path.join(ASSETS_FOLDER, filename)
        tile_image = pygame.image.load(tile_path)
        tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
        TILE_IMAGES.append(tile_image)
        tile_names.append(filename)  # Store the name of the file

current_tile = 1  # Start with the first tile (1 because 0 is "empty")
current_rotation = 0
current_layer = 0  # Default to layer 1 (index 0 in code logic)
camera_x, camera_y = 0, 0

# Initialize grids with NumPy arrays for multiple layers
tiles = np.zeros((NUM_LAYERS, GRID_WIDTH, GRID_HEIGHT), dtype=int)
rotations = np.zeros((NUM_LAYERS, GRID_WIDTH, GRID_HEIGHT), dtype=int)

def draw_grid(screen, camera_x, camera_y):
    """Draws the grid on the screen."""
    start_x = (camera_x // TILE_SIZE) * TILE_SIZE
    start_y = (camera_y // TILE_SIZE) * TILE_SIZE
    for x in range(start_x, camera_x + SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x - camera_x, 0), (x - camera_x, SCREEN_HEIGHT))
    for y in range(start_y, camera_y + SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y - camera_y), (SCREEN_WIDTH, y - camera_y))

def draw_tiles(screen, tiles, rotations, camera_x, camera_y, active_layer):
    """Draws the tiles, with reduced opacity for non-active layers."""
    start_x = max(camera_x // TILE_SIZE, 0)
    start_y = max(camera_y // TILE_SIZE, 0)
    end_x = min((camera_x + SCREEN_WIDTH) // TILE_SIZE + 1, GRID_WIDTH)
    end_y = min((camera_y + SCREEN_HEIGHT) // TILE_SIZE + 1, GRID_HEIGHT)

    for layer in range(NUM_LAYERS):
        alpha = 255 if layer == active_layer else 100  # Full opacity for active layer, reduced for others
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile_index = tiles[layer, x, y]
                if tile_index != 0:
                    tile_image = TILE_IMAGES[tile_index].copy()
                    tile_image.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                    rotated_tile = pygame.transform.rotate(tile_image, rotations[layer, x, y])
                    screen.blit(rotated_tile, (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))

def save_tiles_to_json(tiles, rotations, filename):
    """Saves the entire grid of tiles and rotations for all layers to a JSON file."""
    tiles_list = tiles.tolist()
    rotations_list = rotations.tolist()
    with open(filename, 'w') as f:
        json.dump({"tiles": tiles_list, "rotations": rotations_list}, f)

def load_tiles_from_json(filename):
    """Loads the entire grid of tiles and rotations for all layers from a JSON file."""
    with open(filename, 'r') as f:
        data = json.load(f)
        tiles = np.array(data["tiles"], dtype=int)
        rotations = np.array(data["rotations"], dtype=int)
        return tiles, rotations

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tilemap Editor with Layers and Opacity")

# Main loop
running = True
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        camera_y = max(camera_y - 5, 0)
    if keys[pygame.K_DOWN]:
        camera_y = min(camera_y + 5, (GRID_HEIGHT * TILE_SIZE) - SCREEN_HEIGHT)
    if keys[pygame.K_LEFT]:
        camera_x = max(camera_x - 5, 0)
    if keys[pygame.K_RIGHT]:
        camera_x = min(camera_x + 5, (GRID_WIDTH * TILE_SIZE) - SCREEN_WIDTH)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                current_tile = (current_tile - 1) % len(TILE_IMAGES)
            elif event.button == 5:  # Scroll down
                current_tile = (current_tile + 1) % len(TILE_IMAGES)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_rotation = (current_rotation + 90) % 360
            elif event.key == pygame.K_s:
                save_tiles_to_json(tiles, rotations, 'tiles.json')
                print("Tiles saved to tiles.json")
            elif event.key == pygame.K_l:
                try:
                    tiles, rotations = load_tiles_from_json('tiles.json')
                    print("Tiles loaded from tiles.json")
                except FileNotFoundError:
                    print("No save file found.")
            elif pygame.K_1 <= event.key <= pygame.K_9:  # Switch layers with number keys
                new_layer = event.key - pygame.K_1
                if new_layer < NUM_LAYERS:
                    current_layer = new_layer
                    print(f"Switched to layer {current_layer + 1}")

        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = (mouse_x + camera_x) // TILE_SIZE, (mouse_y + camera_y) // TILE_SIZE
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                tiles[current_layer, grid_x, grid_y] = current_tile
                rotations[current_layer, grid_x, grid_y] = current_rotation
        elif pygame.mouse.get_pressed()[2]:  # Right mouse button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = (mouse_x + camera_x) // TILE_SIZE, (mouse_y + camera_y) // TILE_SIZE
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                tiles[current_layer, grid_x, grid_y] = 0
                rotations[current_layer, grid_x, grid_y] = 0

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the tiles and grid
    draw_tiles(screen, tiles, rotations, camera_x, camera_y, current_layer)
    draw_grid(screen, camera_x, camera_y)

    # Tile preview
    mouse_x, mouse_y = pygame.mouse.get_pos()
    preview_x, preview_y = (mouse_x + camera_x) // TILE_SIZE, (mouse_y + camera_y) // TILE_SIZE
    if 0 <= preview_x < GRID_WIDTH and 0 <= preview_y < GRID_HEIGHT:
        rotated_preview = pygame.transform.rotate(TILE_IMAGES[current_tile], current_rotation)
        screen.blit(rotated_preview, (preview_x * TILE_SIZE - camera_x, preview_y * TILE_SIZE - camera_y))

    # Display current tile and layer info
    font = pygame.font.SysFont(None, 24)
    tile_info = f"Tile: {tile_names[current_tile]} ({current_tile}), Rotation: {current_rotation}°, Layer: {current_layer + 1}"
    text = font.render(tile_info, True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
