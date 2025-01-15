import pygame
import json

# Initialize Pygame
pygame.init()

# Screen settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CANVAS_SIZE = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Point Mapper")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Canvas position (centered)
CANVAS_X = (WINDOW_WIDTH - CANVAS_SIZE) // 2
CANVAS_Y = (WINDOW_HEIGHT - CANVAS_SIZE) // 2

# Points
original_points = []
mapped_points = []
connections = []  # List of tuples to store connections between points
selected_point = None  # Index of the selected point for connection
moving_point = None  # Index of the point being moved
interaction_mode = "edit"  # Modes: "edit", "move"

# Font for debug messages
debug_font = pygame.font.SysFont(None, 24)

# Background image
background_image = pygame.image.load("assets/road_straight_left.png")  # Load your image here
background_image = pygame.transform.scale(background_image, (CANVAS_SIZE, CANVAS_SIZE))  # Scale to canvas size
image_opacity = 128  # Opacity control (0-255)

# Map a point to a 1:1 square (normalized to the canvas size)
def map_to_square(point):
    x, y = point
    return ((x - CANVAS_X) / CANVAS_SIZE, (y - CANVAS_Y) / CANVAS_SIZE)

# Map a normalized point back to canvas coordinates
def map_to_canvas(point):
    x, y = point
    return (int(x * CANVAS_SIZE + CANVAS_X), int(y * CANVAS_SIZE + CANVAS_Y))

# Draw points and lines on the canvas
def draw_points_and_lines():
    for i, point in enumerate(original_points):
        color = YELLOW if i == selected_point else RED
        pygame.draw.circle(screen, color, point, 5)

    for conn in connections:
        pygame.draw.line(screen, GREEN, original_points[conn[0]], original_points[conn[1]], 2)

    for i, point in enumerate(mapped_points):
        x, y = point
        canvas_point = map_to_canvas((x, y))
        pygame.draw.circle(screen, BLUE, canvas_point, 5)
        for conn in connections:
            start = map_to_canvas(mapped_points[conn[0]])
            end = map_to_canvas(mapped_points[conn[1]])
            pygame.draw.line(screen, GREEN, start, end, 2)

# Draw debug information
def draw_debug_info():
    debug_texts = []

    # Closest point
    mouse_pos = pygame.mouse.get_pos()
    if original_points:
        closest_point_index = min(
            range(len(original_points)), 
            key=lambda i: (original_points[i][0] - mouse_pos[0]) ** 2 + (original_points[i][1] - mouse_pos[1]) ** 2
        )
        closest_point = original_points[closest_point_index]
        debug_texts.append(f"Closest Point: {map_to_square(closest_point)}")

    # Closest connection
    if connections:
        def connection_distance(conn):
            p1 = original_points[conn[0]]
            p2 = original_points[conn[1]]
            px, py = mouse_pos
            d1 = ((px - p1[0]) ** 2 + (py - p1[1]) ** 2) ** 0.5
            d2 = ((px - p2[0]) ** 2 + (py - p2[1]) ** 2) ** 0.5
            return d1 + d2

        closest_connection = min(connections, key=connection_distance)
        debug_texts.append(f"Closest Connection: {closest_connection}")

    # Selected point
    if selected_point is not None:
        debug_texts.append(f"Selected Point: {map_to_square(original_points[selected_point])}")

    # Interaction mode
    debug_texts.append(f"Mode: {interaction_mode}")

    # Render debug messages
    for i, text in enumerate(debug_texts):
        debug_surface = debug_font.render(text, True, BLACK)
        screen.blit(debug_surface, (10, 10 + i * 20))

# Save mapped points and connections to a file
def save_points(filename="mapped_points.json"):
    data = {
        "points": mapped_points,
        "connections": connections
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Load mapped points and connections from a file
def load_points(filename="mapped_points.json"):
    global original_points, mapped_points, connections
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            mapped_points = data["points"]
            connections = data["connections"]
            original_points = [map_to_canvas((x, y)) for x, y in mapped_points]
            print("Mapped points loaded!")
    except FileNotFoundError:
        print("No saved points file found.")

# Remove the closest connection to a given position
def remove_closest_connection(pos):
    if not connections:
        return

    def distance_to_connection(conn):
        p1 = original_points[conn[0]]
        p2 = original_points[conn[1]]
        px, py = pos
        d1 = ((px - p1[0]) ** 2 + (py - p1[1]) ** 2) ** 0.5
        d2 = ((px - p2[0]) ** 2 + (py - p2[1]) ** 2) ** 0.5
        return d1 + d2

    closest_connection = min(connections, key=distance_to_connection)
    connections.remove(closest_connection)

# Remove the closest point to a given position
def remove_closest_point(pos):
    global original_points, mapped_points, connections, selected_point
    if not original_points:
        return

    closest_index = min(range(len(original_points)), key=lambda i: (original_points[i][0] - pos[0]) ** 2 + (original_points[i][1] - pos[1]) ** 2)
    original_points.pop(closest_index)
    mapped_points.pop(closest_index)
    connections = [(a, b) for a, b in connections if a != closest_index and b != closest_index]
    connections = [(a if a < closest_index else a - 1, b if b < closest_index else b - 1) for a, b in connections]
    if selected_point == closest_index:
        selected_point = None
    elif selected_point and selected_point > closest_index:
        selected_point -= 1

# Automatically connect the last two points
def auto_connect_last_points():
    if len(original_points) >= 2:
        connection = (len(original_points) - 2, len(original_points) - 1)
        connections.append(connection)

# Select the closest point to form a connection
def select_closest_point(pos):
    global selected_point
    if not original_points:
        return

    closest_index = min(range(len(original_points)), key=lambda i: (original_points[i][0] - pos[0]) ** 2 + (original_points[i][1] - pos[1]) ** 2)
    if selected_point is None:
        selected_point = closest_index
    elif selected_point != closest_index:
        connection = tuple(sorted([selected_point, closest_index]))
        if connection not in connections:
            connections.append(connection)
        selected_point = None
    else:
        selected_point = None

# Get the closest point to a given position
def get_closest_point(pos):
    if not original_points:
        return None

    closest_index = min(range(len(original_points)), key=lambda i: (original_points[i][0] - pos[0]) ** 2 + (original_points[i][1] - pos[1]) ** 2)
    return closest_index

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw the background image with opacity
    surface = pygame.Surface((CANVAS_SIZE, CANVAS_SIZE))  
    surface.set_alpha(image_opacity)  # Set image transparency
    surface.blit(background_image, (0, 0))
    screen.blit(surface, (CANVAS_X, CANVAS_Y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if interaction_mode == "edit":
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    if CANVAS_X <= pos[0] <= CANVAS_X + CANVAS_SIZE and CANVAS_Y <= pos[1] <= CANVAS_Y + CANVAS_SIZE:
                        original_points.append(pos)
                        mapped_points.append(map_to_square(pos))
                        auto_connect_last_points()
                elif event.button == 3:  # Right click
                    pos = pygame.mouse.get_pos()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        remove_closest_point(pos)
                    else:
                        remove_closest_connection(pos)
                elif event.button == 2:  # Middle click
                    pos = pygame.mouse.get_pos()
                    select_closest_point(pos)
            elif interaction_mode == "move":
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    moving_point = get_closest_point(pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if interaction_mode == "move" and event.button == 1:  # Left button released
                moving_point = None

        if event.type == pygame.MOUSEMOTION:
            if interaction_mode == "move" and moving_point is not None:
                pos = event.pos
                if CANVAS_X <= pos[0] <= CANVAS_X + CANVAS_SIZE and CANVAS_Y <= pos[1] <= CANVAS_Y + CANVAS_SIZE:
                    original_points[moving_point] = pos
                    mapped_points[moving_point] = map_to_square(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Save points
                save_points()
                print("Mapped points saved!")
            if event.key == pygame.K_l:  # Load points
                load_points()
            if event.key == pygame.K_g:  # Enter move mode
                interaction_mode = "move"
                print("Move mode activated")
            if event.key == pygame.K_h:  # Enter edit mode
                interaction_mode = "edit"
                print("Edit mode activated")
            if event.key == pygame.K_d:  # Show point connections
                print("Point IDs by connections:")
                for i, conn in enumerate(connections):
                    print(f"Connection {i}: {conn[0]} -> {conn[1]}")

    # Draw the canvas
    pygame.draw.rect(screen, BLACK, (CANVAS_X, CANVAS_Y, CANVAS_SIZE, CANVAS_SIZE), 1)
    
    # Draw the points and lines
    draw_points_and_lines()

    # Draw debug information
    draw_debug_info()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
