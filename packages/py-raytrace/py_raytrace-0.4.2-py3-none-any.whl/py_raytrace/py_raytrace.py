import numpy as np
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# Define the image dimensions
width, height = 800, 600

# Create an image buffer
image = np.zeros((height, width, 3), dtype=np.uint8)

# Define the camera parameters
camera_position = np.array([0, 0, 0])
camera_direction = np.array([0, 0, -1])
camera_up = np.array([0, 1, 0])

# Calculate the aspect ratio
aspect_ratio = width / height

# Adjust the camera right vector based on the aspect ratio
camera_right = np.cross(camera_direction, camera_up) * aspect_ratio

# Define the lighting
light_position = np.array([5, 5, 0])
light_color = np.array([255, 255, 255])

# Define multiple spheres
spheres = [
    {"position": np.array([0, 0, -5]), "radius": 1, "color": np.array([255, 0, 0])},  # Red sphere
    {"position": np.array([2, 1, -8]), "radius": 1.5, "color": np.array([0, 255, 0])},  # Green sphere
    {"position": np.array([-2, -1, -8]), "radius": 0.8, "color": np.array([0, 0, 255])},  # Blue sphere
]

# Define the floor
floor = {"position": np.array([0, -1, 0]), "normal": np.array([0, 1, 0])}

# Function to get the color of a point on the floor
def get_floor_color(point):
    return np.array([255, 255, 255]) if (int(point[0]) + int(point[2])) % 2 else np.array([0, 0, 0])

# Ray tracing function
def trace_ray(origin, direction, depth=0):
    # Maximum recursion depth
    max_depth = 5

    if depth >= max_depth:
        return np.array([0, 0, 0], dtype=np.uint8)

    closest_t = float('inf')
    closest_sphere = None

    for sphere in spheres:
        sphere_to_ray = origin - sphere["position"]
        b = np.dot(sphere_to_ray, direction)
        c = np.dot(sphere_to_ray, sphere_to_ray) - sphere["radius"]**2
        discriminant = b**2 - c

        if discriminant > 0:
            t = -b - np.sqrt(discriminant)
            if 0 < t < closest_t:
                closest_t = t
                closest_sphere = sphere

    # Check for intersection with the floor
    denom = np.dot(floor["normal"], direction)
    if abs(denom) > 1e-6:
        t = np.dot(floor["position"] - origin, floor["normal"]) / denom
        if t > 0 and (closest_sphere is None or t < closest_t):
            closest_t = t
            intersection_point = origin + closest_t * direction
            normal = floor["normal"]
            closest_sphere = {"color": get_floor_color(intersection_point)}

    if closest_sphere:
        intersection_point = origin + closest_t * direction

        # Check if the intersection is with a sphere or the floor
        if "position" in closest_sphere:
            # For spheres, calculate the normal based on the sphere's position and radius
            normal = (intersection_point - closest_sphere["position"]) / closest_sphere["radius"]
        else:
            # For the floor, the normal is already defined
            normal = floor["normal"]

        # Lighting calculation
        light_direction = light_position - intersection_point
        light_distance = np.linalg.norm(light_direction)
        light_direction /= light_distance
        diffuse_intensity = max(0, np.dot(normal, light_direction))
        final_color = closest_sphere["color"] * diffuse_intensity

        # Recursive reflection
        reflection_direction = direction - 2 * np.dot(direction, normal) * normal
        reflection_color = trace_ray(intersection_point + 0.001 * reflection_direction, reflection_direction, depth + 1)

        # Combine diffuse and reflection
        final_color = final_color + 0.2 * reflection_color

        return np.clip(final_color, 0, 255).astype(np.uint8)
    else:
        return np.array([0, 0, 0], dtype=np.uint8)

# Create a figure and axes for matplotlib
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
fig.canvas.set_window_title('Py-Ray Trace')

# Create sliders for adjusting camera angles
ax_camera_yaw = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_camera_pitch = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')

ax_button = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(ax_button, 'Render')

slider_camera_yaw = Slider(ax_camera_yaw, 'Camera Yaw', -180, 180, valinit=0)
slider_camera_pitch = Slider(ax_camera_pitch, 'Camera Pitch', -90, 90, valinit=0)

# Initial rendering
image = np.zeros((height, width, 3), dtype=np.uint8)  # Initialize the image
img = ax.imshow(np.flipud(image), animated=True)  # Initialize the displayed image

# Function to update the scene based on slider changes
# Function to update the camera direction based on slider changes
def update(val):
    # Get current slider values
    camera_yaw = slider_camera_yaw.val
    camera_pitch = slider_camera_pitch.val

    # Update camera direction based on yaw and pitch
    global camera_direction
    camera_direction = np.array([
        np.sin(np.radians(camera_yaw)) * np.cos(np.radians(camera_pitch)),
        np.sin(np.radians(camera_pitch)),
        -np.cos(np.radians(camera_yaw)) * np.cos(np.radians(camera_pitch))
    ])


# Function to render the scene and update the displayed image
def render(event):
    # Render the scene with the updated camera direction
    pbar = tqdm(total=width * height, desc="Rendering", ncols=80)
    for y in range(height):
        for x in range(width):
            # Compute ray direction for each pixel
            ray_direction = (
                    camera_direction +
                    (2 * (x + 0.5) / width - 1) * camera_right +
                    (2 * (y + 0.5) / height - 1) * camera_up
            )
            ray_direction /= np.linalg.norm(ray_direction)

            # Trace the ray and get the color
            color = trace_ray(camera_position, ray_direction)

            # Assign the color to the corresponding pixel in the image
            image[y, x, :] = color

            # Update the progress bar
            pbar.update(1)

        # Update the displayed image after each row
        img.set_array(np.flipud(image))
        fig.canvas.draw_idle()
        plt.pause(0.001)  # Pause for figure to update

    pbar.close()

# Attach the render function to the "Render" button
button.on_clicked(render)


# Attach the update function to slider changes
slider_camera_yaw.on_changed(update)
slider_camera_pitch.on_changed(update)

# Initial rendering
update(0)

# # Update the displayed image
# img = ax.imshow(np.flipud(image), animated=True)

# Show the matplotlib plot
plt.show()
