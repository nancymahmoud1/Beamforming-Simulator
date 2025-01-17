from PyQt5 import QtWidgets, QtGui

import numpy as np

from App.UI.Design import Ui_MainWindow
from App.Logging_Manager import LoggingManager
from App.SimpleSimulation import BeamformingSimulator


class MainController:
    def __init__(self, app):
        self.app = app
        self.main_window = QtWidgets.QMainWindow()

        self.view = Ui_MainWindow()

        self.logging = LoggingManager()

        self.initialize_view()
        self.initialize_arrays_info()

    def initialize_view(self):
        self.view.setupUi(self.main_window)
        self.view.scenarios_button.clicked.connect(self.toggle_scenario)
        self.current_scenario = None

        self.view.arrays_number_SpinBox.valueChanged.connect(self.update_current_arrays_number)
        self.view.elements_number_SpinBox.valueChanged.connect(self.update_current_elements_number)
        self.view.elements_spacing_slider.valueChanged.connect(self.update_elements_spacing)
        self.view.array_curve_slider.valueChanged.connect(self.update_elements_curvature)

        self.view.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)

        self.view.steering_angle_slider.sliderReleased.connect(self.update_steering_angle)
        self.view.operating_frequency_combobox.currentIndexChanged.connect(self.update_operating_frequency)

        self.view.quit_app_button.clicked.connect(self.close_application)

    def toggle_scenario(self):
        scenario_settings = {
            '5G': {
                'frequency': 3.5e9,
                'elements_spacing': 0.25,
                'curvature': 0,
                'num_elements': 16
            },
            'Ultrasound': {
                'frequency': 5e6,
                'elements_spacing': 0.5,
                'curvature': 180,
                'num_elements': 32
            },
            'Tumor Ablation': {
                'frequency': 20e6,
                'elements_spacing': 0.1,
                'curvature': 90,
                'num_elements': 64
            }
        }

        previous_scenario = self.current_scenario
        if self.current_scenario is None or self.current_scenario == 'Tumor Ablation':
            self.current_scenario = '5G'
        elif self.current_scenario == '5G':
            self.current_scenario = 'Ultrasound'
        else:
            self.current_scenario = 'Tumor Ablation'

        self.logging.log(f"Switching scenario from {previous_scenario} to {self.current_scenario}")

        scenario = scenario_settings[self.current_scenario]

        self.view.current_operating_frequency = scenario['frequency']
        self.model.update_operating_frequency(self.view.current_operating_frequency)

        self.view.current_elements_spacing = scenario['elements_spacing'] * self.model.wavelength
        self.view.current_array_curvature_angle = scenario['curvature']
        self.view.elements_number_SpinBox.setValue(scenario['num_elements'])

        self.logging.log(
            f"""
            Updated scenario settings to {self.current_scenario} 
            Frequency: {self.view.format_frequency(scenario['frequency'])},
            Element Spacing:{scenario['elements_spacing']} * wavelength, 
            Curvature: {scenario['curvature']}, 
            Number of Elements: {scenario['num_elements']}
            """
        )

        self.view.scenarios_button.setText(self.current_scenario)
        self.update_and_refresh_arrays_info()

    def toggle_sidebar(self):
        # Toggle the visibility of the sidebar
        self.view.sidebar.setVisible(not self.view.sidebar.isVisible())
        if self.view.sidebar.isVisible():
            # Move button to just left of the sidebar when visible
            self.view.toggle_sidebar_button.move(int(1280 * 0.1 - 50), 390)
            icon = QtGui.QIcon("./Static/Back_Arrow.png")
            self.update_and_refresh_arrays_info()
        else:
            # Move button back to the right edge of the window when sidebar is hidden
            self.view.toggle_sidebar_button.move(int(1280 - 50), 390)
            icon = QtGui.QIcon("./Static/Forward_Arrow.png")

        self.view.toggle_sidebar_button.setIcon(icon)

    def initialize_arrays_info(self):
        # Start with an empty list of configurations
        self.configurations = []

        # Loop over the number of arrays specified in the current_arrays_number
        for i in range(1, self.view.current_arrays_number + 1):
            try:
                # Retrieve the configuration for each array
                spacing, num_elements, curvature = self.view.visualization_widget.get_array_configuration(i)
                # Append a new dictionary to the configurations list with the retrieved settings
                self.configurations.append({
                    'num_elements': num_elements,
                    'spacing': spacing,
                    'curvature': curvature
                })
            except IndexError:
                # Handle cases where the index is out of range, potentially logging or adding default configurations
                self.logging.log(f"Failed to retrieve configuration for array {i}, using default settings.")
                self.configurations.append({
                    'num_elements': 64,  # Default value if out of range
                    'spacing': 0.5,  # Default value if out of range
                    'curvature': 0  # Default value if out of range
                })

        self.model = BeamformingSimulator(self.view.current_operating_frequency, self.view.current_steering_angle, self.configurations)

        self.apply_configurations_to_visualization()

    def update_and_refresh_arrays_info(self):
        # Clear the existing configurations to ensure no outdated data is kept
        self.configurations.clear()

        # Reinitialize the configurations by fetching current settings from the visualization widget
        for i in range(1, self.view.current_arrays_number + 1):
            try:
                # Retrieve the configuration for each array
                spacing, num_elements, curvature = self.view.visualization_widget.get_array_configuration(i)
                # Append a new dictionary to the configurations list with the retrieved settings
                self.configurations.append({
                    'num_elements': num_elements,
                    'spacing': spacing,
                    'curvature': curvature
                })
            except IndexError:
                # Handle cases where the index is out of range, potentially logging or adding default configurations
                self.logging.log(f"Failed to retrieve configuration for array {i}, using default settings.")
                self.configurations.append({
                    'num_elements': 64,  # Default value if out of range
                    'spacing': 0.5,  # Default value if out of range
                    'curvature': 0  # Default value if out of range
                })

        # Optionally update visualization widget here if necessary
        self.apply_configurations_to_visualization()

    def apply_configurations_to_visualization(self):
        # Assuming self.model is an instance of BeamformingSimulator
        x_range = (-10, 10)
        y_range = (0, 10)
        x, y, intensity = self.model.simulate_multiple_arrays(x_range, y_range)

        angles = np.linspace(-90, 90, 500)  # Angles to compute beam profile (in degrees)
        array_factor = self.model.calculate_array_factor(angles)

        self.model.plot_intensity_heatmap(x, y, intensity, self.view.intensityMapCanvas)
        self.model.plot_beam_profile(angles, array_factor, self.view.beamProfileCanvas)

    # --------------------------------------------------------------------------------------------------------------------------------------

    def update_current_arrays_number(self):
        previous_value = self.view.current_arrays_number
        self.view.current_arrays_number = self.view.arrays_number_SpinBox.value()
        self.view.arrays_parameters_indicator.setText(f"{self.view.current_arrays_number} Arrays")
        self.view.current_selected_array = 0
        self.view.current_selected_ALL_array = True
        self.view.current_selected_array_button.setText("All Arrays")
        self.view.visualization_widget.updateArrayNumber(self.view.current_arrays_number)

    def update_current_elements_number(self):
        previous_value = self.view.current_elements_number
        self.view.current_elements_number = self.view.elements_number_SpinBox.value()
        self.view.arrays_parameters_indicator.setText(f"{self.view.current_elements_number} Elements")
        self.view.updateVisualization()

    def update_elements_spacing(self):
        previous_value = self.view.current_elements_spacing
        if self.view.current_operating_frequency > 0:
            self.view.current_elements_spacing = (self.view.elements_spacing_slider.value() / 100) * self.model.wavelength
        else:
            self.view.current_elements_spacing = 0  # or some default value, or raise an error/message to the user
        self.view.arrays_parameters_indicator.setText(f"{self.view.elements_spacing_slider.value()}% Wavelength")
        self.view.updateVisualization()

    def update_elements_curvature(self):
        previous_value = self.view.current_array_curvature_angle
        self.view.current_array_curvature_angle = self.view.array_curve_slider.value()
        self.view.arrays_parameters_indicator.setText(f"{self.view.current_array_curvature_angle} Degree")
        self.view.updateVisualization()

    def update_steering_angle(self):
        previous_value = self.view.current_steering_angle
        self.view.current_steering_angle = self.view.steering_angle_slider.value()
        self.view.sidebar_parameter_indicator.setText(f"{self.view.current_steering_angle} Degree")
        self.model.update_steering_angle(self.view.current_steering_angle)
        self.apply_configurations_to_visualization()

    def update_operating_frequency(self):
        index = self.view.operating_frequency_combobox.currentIndex() - 1
        self.view.current_operating_frequency = self.view.operating_frequency_values[index]
        formatted_frequency = self.view.format_frequency(self.view.current_operating_frequency)
        self.view.sidebar_parameter_indicator.setText(formatted_frequency)
        self.model.update_operating_frequency(self.view.current_operating_frequency)
        self.update_and_refresh_arrays_info()

    # --------------------------------------------------------------------------------------------------------------------------------------
    def close_application(self):
        self.logging.log(f"Application Closed")
        self.main_window.close()

    def run(self):
        self.logging.log("Application Opened")
        self.main_window.showFullScreen()
        return self.app.exec_()
