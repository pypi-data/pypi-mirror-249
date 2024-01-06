import numpy as np
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def main():
    # lower = faster, higher = more time
    width, height = 800, 600

    # creating first np vector for image
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # camera setting
    camera_position = np.array([0, 0, 0])
    camera_direction = np.array([0, 0, -1])
    camera_up = np.array([0, 1, 0])

    aspect_ratio = width / height

    # camera vector based on aspect ratio?
    camera_right = np.cross(camera_direction, camera_up) * aspect_ratio

    # Define the lighting
    light_position = np.array([5, 5, 0])
    light_color = np.array([255, 255, 255])

    # Define multiple spheres
    spheres = [
        {"position": np.array([0, 0, -5]), "radius": 1, "color": np.array([255, 0, 0])},  # red sph
        {"position": np.array([2, 1, -8]), "radius": 1.5, "color": np.array([0, 255, 0])},  # green sph
        {"position": np.array([-2, -1, -8]), "radius": 0.8, "color": np.array([0, 0, 255])},  # blue sph
    ]

    # floor setting
    floor = {"position": np.array([0, -1, 0]), "normal": np.array([0, 1, 0])}

    # color of floor (checked pattern)
    def get_floor_color(point):
        return np.array([255, 255, 255]) if (int(point[0]) + int(point[2])) % 2 else np.array([0, 0, 0])

    def trace_ray(origin, direction, depth=0):
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

        # check for intersect with floor
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

            if "position" in closest_sphere:
                normal = (intersection_point - closest_sphere["position"]) / closest_sphere["radius"]
            else:
                normal = floor["normal"]

            light_direction = light_position - intersection_point
            light_distance = np.linalg.norm(light_direction)
            light_direction /= light_distance
            diffuse_intensity = max(0, np.dot(normal, light_direction))
            final_color = closest_sphere["color"] * diffuse_intensity

            reflection_direction = direction - 2 * np.dot(direction, normal) * normal
            reflection_color = trace_ray(intersection_point + 0.001 * reflection_direction, reflection_direction, depth + 1)

            final_color = final_color + 0.2 * reflection_color

            return np.clip(final_color, 0, 255).astype(np.uint8)
        else:
            return np.array([0, 0, 0], dtype=np.uint8)

    # create a figure and axes for matplotlib
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    plt.title('Py-RayTrace')

    # create sliders for adjusting camera angles
    ax_camera_yaw = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    ax_camera_pitch = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')

    ax_button = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(ax_button, 'Render')

    slider_camera_yaw = Slider(ax_camera_yaw, 'Camera Yaw', -180, 180, valinit=0)
    slider_camera_pitch = Slider(ax_camera_pitch, 'Camera Pitch', -90, 90, valinit=0)

    # initial rendering
    image = np.zeros((height, width, 3), dtype=np.uint8)
    img = ax.imshow(np.flipud(image), animated=True)

    # update on slider inputs
    def update(val):
        camera_yaw = slider_camera_yaw.val
        camera_pitch = slider_camera_pitch.val

        global camera_direction
        camera_direction = np.array([
            np.sin(np.radians(camera_yaw)) * np.cos(np.radians(camera_pitch)),
            np.sin(np.radians(camera_pitch)),
            -np.cos(np.radians(camera_yaw)) * np.cos(np.radians(camera_pitch))
        ])

    # function to render the scene
    def render(event):
        pbar = tqdm(total=width * height, desc="Rendering", ncols=80)
        for y in range(height):
            for x in range(width):
                ray_direction = (
                        camera_direction +
                        (2 * (x + 0.5) / width - 1) * camera_right +
                        (2 * (y + 0.5) / height - 1) * camera_up
                )
                ray_direction /= np.linalg.norm(ray_direction)

                color = trace_ray(camera_position, ray_direction)

                image[y, x, :] = color

                pbar.update(1)

            img.set_array(np.flipud(image))
            fig.canvas.draw_idle()
            plt.pause(0.001)

        pbar.close()

    # on event button click, call render
    button.on_clicked(render)

    # on event change slider, call update
    slider_camera_yaw.on_changed(update)
    slider_camera_pitch.on_changed(update)

    # load and render
    update(0)

    # show the matplotlib plot
    try:
        plt.show()
    except Exception as e:
        print('Quit')

if __name__ == '__main__':
    main()
