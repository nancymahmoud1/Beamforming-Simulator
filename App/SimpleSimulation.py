import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from math import sin, radians


class BeamformingSimulator:
    def __init__(self, frequency, steering_angle, arrays_info):
        self.frequency = frequency  # Operating frequency in Hz
        self.steering_angle = steering_angle  # Steering angle in degrees
        self.arrays_info = arrays_info  # Store array configurations
        self.wavelength = 3e8 / self.frequency  # Calculate wavelength from frequency
        self.k = 2 * np.pi / self.wavelength  # Calculate wave number

    def calculate_element_positions(self, num_elements, element_spacing, curvature_degree):
        positions = []
        if curvature_degree == 0:  # Linear array
            # Start at (0,0) and lay out elements to the right
            positions = [(i * element_spacing - (num_elements - 1) * element_spacing / 2, 0) for i in range(num_elements)]
            # element_x = n * element_spacing - (num_elements - 1) * element_spacing / 2  # Center the array
        else:  # Curved array
            # Calculate the radius of the curvature
            radius = element_spacing / (2 * sin(radians(curvature_degree / (num_elements - 1) / 2))) if num_elements > 1 else element_spacing
            # Calculate the angle increment for each element in the array
            angle_increment = np.radians(curvature_degree) / (num_elements - 1)
            # Calculate positions for each element based on curvature
            for i in range(num_elements):
                angle = -np.radians(curvature_degree) / 2 + i * angle_increment
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                # Since y is curved, adjust x position by radius to shift the array to the right start point
                positions.append((x + radius, y))
        return positions

    def simulate_multiple_arrays(self, x_range, y_range):
        """Simulate multiple arrays with given configurations."""
        x = np.linspace(x_range[0], x_range[1], 200)
        y = np.linspace(y_range[0], y_range[1], 200)
        X, Y = np.meshgrid(x, y)
        intensity_map = np.zeros_like(X, dtype=np.complexfloating)

        for array_info in self.arrays_info:
            positions = self.calculate_element_positions(array_info['num_elements'], array_info['spacing'], array_info['curvature'])
            for (ex, ey) in positions:
                distances = np.sqrt((X - ex) ** 2 + (Y - ey) ** 2)
                phase_shift = -self.k * ex * np.sin(np.radians(self.steering_angle))
                intensity_map += np.exp(1j * (self.k * distances + phase_shift))

        intensity = np.abs(intensity_map) ** 2
        intensity /= np.max(intensity)
        return x, y, intensity

    def calculate_array_factor(self, angles):
        array_factor = np.zeros_like(angles, dtype=np.complex128)
        positions = self.calculate_element_positions(self.arrays_info[0]['num_elements'], self.arrays_info[0]['spacing'],
                                                     self.arrays_info[0]['curvature'])
        for x, _ in positions:
            phase_shift = -self.k * x * np.sin(np.radians(self.steering_angle))
            array_factor += np.exp(1j * (self.k * x * np.sin(np.radians(angles)) + phase_shift))
        return np.abs(array_factor) ** 2

    def plot_intensity_heatmap(self, x, y, intensity, canvas):
        # Assuming 'canvas' is a FigureCanvasQTAgg
        canvas.figure.clf()  # Clear any existing plots
        ax = canvas.figure.subplots()
        cax = ax.imshow(intensity, extent=[-10, 10, 0, 10], origin='lower', cmap='jet', aspect='auto')
        ax.set_title('Beamforming Intensity Map')
        ax.set_xlabel('Horizontal Position (meters)')
        ax.set_ylabel('Vertical Position (meters)')
        canvas.figure.colorbar(cax, ax=ax, label='Normalized Intensity')
        canvas.draw()  # Update the canvas

    def plot_beam_profile(self, angles, array_factor, canvas):
        canvas.figure.clf()  # Clear any existing plots
        ax = canvas.figure.subplots()
        ax.plot(angles, array_factor / np.max(array_factor))
        ax.set_title('Beam Profile')
        ax.set_xlabel('Angle (degrees)')
        ax.set_ylabel('Normalized Array Factor')
        ax.grid(True)
        canvas.draw()  # Update the canvas

    # -------------------------------------------------------------------------------------------------------------------------------------
    def update_operating_frequency(self, frequency):
        self.frequency = frequency
        self.wavelength = 3e8 / self.frequency
        self.k = 2 * np.pi / self.wavelength

    def update_steering_angle(self, steering_angle):
        self.steering_angle = steering_angle
