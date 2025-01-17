from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QPoint
from math import cos, radians, sin


class ArrayVisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.element_size = 1  # Constant radius for each element
        self.array_configs = []
        # Default configuration for new arrays if not specified
        self.default_spacing = 2
        self.default_num_elements = 2
        self.default_curvature_angle = 0

    def addArray(self, spacing=None, num_elements=None, curvature_angle=None):
        if spacing is None:
            spacing = self.default_spacing
        if num_elements is None:
            num_elements = self.default_num_elements
        if curvature_angle is None:
            curvature_angle = self.default_curvature_angle
        # Adds a new array configuration
        self.array_configs.append((spacing, num_elements, curvature_angle))
        self.update()

    def editArray(self, index, spacing, num_elements, curvature_angle):
        # Adjust index to zero-based for internal processing
        zero_based_index = index - 1
        if 0 <= zero_based_index < len(self.array_configs):
            self.array_configs[zero_based_index] = (spacing, num_elements, curvature_angle)
            self.update()
        else:
            raise ValueError("Array index out of range")  # Provide feedback for invalid index

    def updateArrayNumber(self, array_num):
        # Interpret array_num as 1-based and adjust for 0-based indexing
        target_length = array_num
        current_length = len(self.array_configs)
        if target_length > current_length:
            # Add new arrays with default settings
            for _ in range(target_length - current_length):
                self.addArray()  # Use default parameters
        elif target_length < current_length:
            # Remove excess arrays
            self.array_configs = self.array_configs[:target_length]
        self.update()  # Redraw the widget with updated settings

    def get_array_configuration(self, index):
        # Adjust index to zero-based for internal processing
        zero_based_index = index - 1
        if 0 <= zero_based_index < len(self.array_configs):
            return self.array_configs[zero_based_index]
        else:
            raise IndexError("Array index out of range")

    def paintEvent(self, event):
        qp = QPainter(self)
        self.drawArrays(qp)
        qp.end()

    def drawArrays(self, qp):
        qp.setPen(QPen(QColor(0, 0, 0), 1))  # Setting pen for circle outlines
        qp.setBrush(QColor(255, 255, 255))  # Setting brush for filling circles
        centerY = self.height() / 2  # Vertical center of the widget

        num_arrays = len(self.array_configs)
        array_width = 150  # Assumed fixed width for each array's visualization component

        # Calculate the total minimum width required for all arrays without any space between them
        total_width_required = num_arrays * array_width - 100

        # Available width for spacing between arrays
        available_width_for_spacing = self.width() - total_width_required

        # Calculate dynamic spacing based on available space for spacing
        if num_arrays > 1:
            if available_width_for_spacing > 0:
                spacing_between_arrays = available_width_for_spacing // (num_arrays - 1)
            else:
                spacing_between_arrays = max(5, available_width_for_spacing // (num_arrays - 1))
        else:
            spacing_between_arrays = 0  # Only one array, no spacing needed

        # Calculate the starting x position to center the arrays in the widget
        x_start = (self.width() - (total_width_required + (num_arrays - 1) * spacing_between_arrays)) / 2

        for index, (spacing, num_elements, curvature_angle) in enumerate(self.array_configs):
            positions = []  # Store calculated positions for alignment
            current_x_start = x_start + index * (array_width + spacing_between_arrays)  # Calculate x_start for this array

            if curvature_angle == 0:  # Linear layout for arrays without curvature
                for i in range(num_elements):
                    x_pos = current_x_start + i * spacing
                    positions.append((x_pos, centerY))
            else:  # Curved layout calculation
                radius = spacing / (2 * sin(radians(curvature_angle / (num_elements - 1) / 2))) if num_elements > 1 else spacing
                start_angle = radians(90 - curvature_angle / 2)
                for i in range(num_elements):
                    angle = start_angle + i * radians(curvature_angle / (num_elements - 1))
                    x_pos = current_x_start + radius * cos(angle)
                    y_pos = centerY + radius * sin(angle) - radius
                    positions.append((x_pos, y_pos))

            for x_pos, y_pos in positions:
                if not (-2147483648 <= x_pos <= 2147483647 and -2147483648 <= y_pos <= 2147483647):
                    print(f"Invalid position values: x_pos={x_pos}, y_pos={y_pos}")
                else:
                    qp.drawEllipse(QPoint(int(x_pos), int(y_pos)), self.element_size, self.element_size)
