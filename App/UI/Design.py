from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from App.UI.ArrayVisualizationWidget import ArrayVisualizationWidget


class Ui_MainWindow(object):
    def __init__(self, current_selected_ALL_array=False, current_arrays_number=1, current_array_curvature_angle=0, current_elements_number=2,
                 current_elements_spacing=0.5, current_steering_angle=90, current_operating_frequency=700e6):
        self.visualization_widget = ArrayVisualizationWidget()

        self.BUTTON_STYLESHEET = """
        QPushButton {
            color: #B0BEC5;
            background-color: rgba(255, 255, 255, 0);
            border: 1px solid #B0BEC5
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 10);
        }
        """

        self.QUIT_BUTTON_STYLESHEETSHEET = """
        QPushButton {
            color: rgb(8, 51, 143);
            background-color: rgba(255, 255, 255, 0);
            border: 3px solid rgb(8, 51, 143)
        }
        QPushButton:hover {
            border-color: rgb(253, 94, 80);
            color: rgb(253, 94, 80);
        }
        """
        self.SCENARIOS_BUTTON_STYLESHEETSHEET = """
        QPushButton {
            color: rgb(8, 51, 143);
            background-color: rgba(255, 255, 255, 0);
            border: 3px solid rgb(8, 51, 143)
        }
        """
        self.SLIDER_STYLESHEET = """
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 2px;
            background: #dddddd;
            margin: 2px 0;
        }
        QSlider::handle:horizontal {
            background: rgb(11, 62, 159);
            width: 16px;
            margin: -10px 0;
            border-radius: 3px;
        }
        QSlider::sub-page:horizontal {
            background: rgb(4, 29, 127);
            border: 1px solid rgb(4, 29, 127);
            height: 1px;
            border-radius: 2px;
        }
        """
        self.SPINBOX_STYLESHEET = """
        QSpinBox {
            background-color: #1A1A40;
            color: #E0E0E0;
            border: 1px solid #B0BEC5;
            border-radius: 5px;
            padding: 5px;
        }

        QSpinBox::up-button {
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 16px;
            background-color: rgb(19, 97, 189);
            border: 1px solid #B0BEC5;
            border-left: none;
            border-radius: 0px 5px 0px 0px;
        }

        QSpinBox::down-button {
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 16px;
            background-color: rgb(19, 97, 189);
            border: 1px solid #B0BEC5;
            border-left: none;
            border-radius: 0px 0px 5px 0px;
        }

        QSpinBox::up-arrow {
            width: 10px;
            height: 10px;
            image: url("./Static/Up_Arrow.png");
            border: none;
        }

        QSpinBox::down-arrow {
            width: 10px;
            height: 10px;
            image: url("./Static/Down_Arrow.png");
            border: none;
        }

        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: rgb(11, 70, 177);
        }

        QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
            background-color: rgb(11, 70, 177);
        }
        """
        self.COMBOBOX_STYLESHEET = """
        QComboBox {
            border: 2px solid #8F8F8F;
            border-radius: 5px;
            padding: 5px;
            background-color: #1A1A1A;
            color: #FFFFFF;
            font-size: 14px;
        }

        QComboBox:hover {
            border-color: rgb(9, 60, 145);
        }

        QComboBox::drop-down {
            border: none;
            width: 30px;
            border-radius: 0px 5px 5px 0px;
        }

        QComboBox::down-arrow {
            image: url("./Static/Down_Arrow.png");
            width: 10px;
            height: 10px;
        }

        QComboBox QAbstractItemView {
            border: 1px solid rgb(9, 60, 145);
            color: #FFFFFF;
            selection-background-color: rgb(9, 60, 145);
            selection-color: #FFFFFF;
            padding: 5px;
        }
        """

        self.sidebar_open = False

        self.current_selected_ALL_array = current_selected_ALL_array
        self.current_arrays_number = current_arrays_number

        self.current_selected_array = 1

        self.current_array_curvature_angle = current_array_curvature_angle
        self.current_elements_number = current_elements_number
        self.current_elements_spacing = current_elements_spacing

        self.current_steering_angle = current_steering_angle
        self.current_operating_frequency = current_operating_frequency

        self.operaring_frequency_values = [
            700e6,  # 700 MHz (5G)
            900e6,  # 900 MHz (5G)
            1.8e9,  # 1.8 GHz (5G)
            2.1e9,  # 2.1 GHz (5G)
            3.5e9,  # 3.5 GHz (5G)
            5e9,  # 5 GHz (5G and advanced applications)
            1e6,  # 1 MHz (Ultrasound, tumor ablation)
            3e6,  # 3 MHz (Ultrasound, therapeutic applications)
            5e6,  # 5 MHz (Ultrasound, industrial applications)
            10e6,  # 10 MHz (Ultrasound, tumor ablation)
            20e6  # 20 MHz (Ultrasound, advanced tumor ablation)
        ]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setFont(QtGui.QFont("Noto Serif Balinese"))
        MainWindow.setStyleSheet("background-color:#1A1A40")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setupVisualization(MainWindow)
        self.setupHorizontalLayouts()
        self.setupMainButtons(MainWindow)
        self.setupMenuBar(MainWindow)
        self.setupSidebar(MainWindow)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupVisualization(self, MainWindow):
        # Ensure this method is called after setting up the centralwidget in setupUi

        # Create a widget that will contain the visualization widget
        container = QtWidgets.QWidget(self.centralwidget)
        container.setFixedSize(1200, 700)  # Set the size of the container
        container.setStyleSheet("""
            background-color: rgb(9, 60, 145);
            border: 2px solid white;
            border-radius: 15px;
            margin-top: 100px;
        """)

        # Create a layout for the container
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(10, 30, 10, 10)  # Add some margin for the title

        # Add a title label
        title_label = QtWidgets.QLabel(container)
        title_label.setText("Beamforming Simulator")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: white;               /* Text color */
            font-size: 18px;            /* Font size */
            font-weight: bold;          /* Bold text */
            padding: 10px;              /* Padding around text */
            border: 2px solid white;    /* Add border */
            border-radius: 15px;        /* Rounded corners */
        """)
        title_label.setMaximumSize(250, 200)

        container_layout.addWidget(title_label)

        # Add the visualization widget to the container
        container_layout.addWidget(self.visualization_widget)
        self.visualization_widget.setMinimumSize(500, 50)  # Ensure the visualization widget expands to fill the container

        # Now, place the container in the centralwidget, centered horizontally
        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        main_layout.addWidget(container, 0, QtCore.Qt.AlignCenter)  # Align center horizontally

        # Initialize the visualization with default settings
        spacing_factor = 10
        self.visualization_widget.addArray(
            spacing=self.current_elements_spacing * spacing_factor,
            num_elements=self.current_elements_number,
            curvature_angle=self.current_array_curvature_angle,
        )

    def setupHorizontalLayouts(self):
        self.title_layout = self.createHorizontalLayout(self.centralwidget, 470, 10, 372, 52)
        self.title_icon = self.createLabel(self.title_layout, "./Static/Sensor.png", 50)
        self.title_label = self.createLabel(self.title_layout, text_font=("PT Sans", 20), max_size=(370, 50))

        self.inputs_layout = self.createHorizontalLayout(self.centralwidget, 20, 70, 1241, 41)

    def setupSidebar(self, MainWindow):
        self.sidebar = QtWidgets.QWidget(self.centralwidget)
        self.sidebar.setGeometry(QtCore.QRect(int(1280 * 0.1), 5, int(1280 * 0.9), 790))
        self.sidebar.setStyleSheet("""
            QWidget {
                background-color: rgba(34, 34, 68, 255)
                color: #E0E0E0;
                border-left: 1px solid #B0BEC5;
                border-top: 1px solid #B0BEC5;
                border-bottom: 1px solid #B0BEC5;
            }
        """)
        self.sidebar.setVisible(False)

        self.operating_frequency_values = [
            700e6,  # 700 MHz (5G)
            900e6,  # 900 MHz (5G)
            1.8e9,  # 1.8 GHz (5G)
            2.1e9,  # 2.1 GHz (5G)
            3.5e9,  # 3.5 GHz (5G)
            5e9,  # 5 GHz (5G and advanced applications)
            1e6,  # 1 MHz (Ultrasound, tumor ablation)
            3e6,  # 3 MHz (Ultrasound, therapeutic applications)
            5e6,  # 5 MHz (Ultrasound, industrial applications)
            10e6,  # 10 MHz (Ultrasound, tumor ablation)
            20e6  # 20 MHz (Ultrasound, advanced tumor ablation)
        ]

        # Set a vertical layout for the sidebar
        sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(15)

        # Grid layout for plots
        self.gridLayoutWidget = QtWidgets.QWidget(self.sidebar)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setStyleSheet("border: none;")  # Remove outer border

        self.plots_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.plots_layout.setContentsMargins(0, 0, 0, 0)
        self.plots_layout.setObjectName("plots_layout")

        # Add the grid layout widget to the sidebar's layout
        sidebar_layout.addWidget(self.gridLayoutWidget)

        # Setup plot holders and widgets
        self.setupPlotHolders()

        # Horizontal layout for control buttons
        self.controls_widget = QtWidgets.QWidget(self.sidebar)
        self.controls_widget.setMaximumHeight(80)  # Limit the height of the controls layout
        self.controls_widget.setStyleSheet("border: none;")  # Remove outer border

        self.controls_layout = QtWidgets.QHBoxLayout(self.controls_widget)
        self.controls_layout.setContentsMargins(5, 5, 5, 5)
        self.controls_layout.setSpacing(10)

        # Create and add buttons to the controls_layout
        self.return_sidebar_buttons = self.createButton(self.controls_layout, "Back", isVisible=False,
                                                        method=self.return_sidebar_initial_button)

        self.steering_angle_button = self.createButton(self.controls_layout, "Steering Angle", method=self.show_steering_angle_slider)
        self.steering_angle_slider = self.createSlider(self.controls_layout, min_value=-90, max_value=90,
                                                       initial_value=self.current_steering_angle, isVisible=False)

        self.operating_frequency_button = self.createButton(self.controls_layout, "Operating Frequency", method=self.show_frequency_combobox)
        self.operating_frequency_combobox = self.createComboBox(layout=self.controls_layout, options=self.operaring_frequency_values,
                                                                placeholder="Operating Frequency", isVisible=False)

        self.sidebar_parameter_indicator = self.createLabel(self.controls_layout, max_size=150, isVisible=False)

        self.SIDEBAR_CONTROLLER_BUTTONS = [self.return_sidebar_buttons, self.steering_angle_button, self.steering_angle_slider,
                                           self.operating_frequency_button, self.operating_frequency_combobox, self.sidebar_parameter_indicator]

        # Add the controls_widget to the sidebar's layout
        sidebar_layout.addWidget(self.controls_widget)

    def setupPlotHolders(self):
        # Creating a single group box to contain all plots for clarity and styling
        self.plotsGroupBox = QtWidgets.QGroupBox("Plots", self.gridLayoutWidget)
        self.plotsGroupBox.setStyleSheet("""
            background-color: rgb(210, 210, 210);
            color: black;
        """)
        self.plots_layout.addWidget(self.plotsGroupBox, 0, 0, 1, 1)

        # Setting up a layout within the group box for plots
        plots_layout = QtWidgets.QGridLayout(self.plotsGroupBox)
        plots_layout.setContentsMargins(5, 5, 5, 5)
        plots_layout.setSpacing(10)

        # Creating matplotlib canvases for the intensity map and beam profile
        self.intensityMapFigure = Figure()
        self.intensityMapCanvas = FigureCanvas(self.intensityMapFigure)
        self.intensityMapCanvas.setStyleSheet("background-color: #1A1A40;")

        self.beamProfileFigure = Figure()
        self.beamProfileCanvas = FigureCanvas(self.beamProfileFigure)
        self.beamProfileCanvas.setStyleSheet("background-color: #1A1A40;")

        # Adding canvases to the plots layout
        plots_layout.addWidget(self.intensityMapCanvas, 0, 0)  # Position at row 0, column 0
        plots_layout.addWidget(self.beamProfileCanvas, 0, 1)  # Position at row 0, column 1

    def setupMainButtons(self, MainWindow):
        self.return_main_buttons = self.createButton(self.inputs_layout, "Back", self.return_main_initial_button, isVisible=False)
        self.current_selected_array_button = self.createButton(self.inputs_layout, "Array 1", self.toggle_current_selected_array,
                                                               isVisible=False)

        self.adjust_array_number = self.createButton(self.inputs_layout, "Adjust Arrays Number", self.show_arrays_number_SpinBox)
        self.arrays_number_SpinBox = self.createSpinBox(self.inputs_layout, min_value=1, max_value=8, initial_value=self.current_arrays_number,
                                                        isVisible=False)

        self.elements_number_button = self.createButton(self.inputs_layout, "Elements Number", self.show_elements_number_SpinBox)
        self.elements_number_SpinBox = self.createSpinBox(self.inputs_layout, min_value=2, max_value=64,
                                                          initial_value=self.current_elements_number, isVisible=False)

        self.elements_spacing_button = self.createButton(self.inputs_layout, "Elements Spacing", self.show_spacing_input)
        self.elements_spacing_slider = self.createSlider(layout=self.inputs_layout, min_value=1, max_value=100,
                                                         initial_value=int(self.current_elements_spacing * 100), isVisible=False)

        self.add_curve_button = self.createButton(self.inputs_layout, "Array Curve", self.show_curve_input)
        self.array_curve_slider = self.createSlider(layout=self.inputs_layout, min_value=0, max_value=180, initial_value=0, isVisible=False)

        self.arrays_parameters_indicator = self.createLabel(self.inputs_layout, max_size=110, isVisible=False)

        self.ARRAYS_CONTROLLER_BUTTONS = [self.return_main_buttons, self.array_curve_slider, self.adjust_array_number,
                                          self.elements_number_button,
                                          self.elements_spacing_button, self.add_curve_button, self.elements_spacing_slider,
                                          self.elements_number_SpinBox, self.arrays_number_SpinBox, self.current_selected_array_button,
                                          self.arrays_parameters_indicator]

        # Creating the quit_app_button directly on the centralwidget without using the layout
        self.scenarios_button = QtWidgets.QPushButton(self.centralwidget)
        self.scenarios_button.setGeometry(QtCore.QRect(1080, 15, 110, 40))
        self.scenarios_button.setFont(QtGui.QFont("Hiragino Sans GB", 13, True))
        self.scenarios_button.setStyleSheet(self.SCENARIOS_BUTTON_STYLESHEETSHEET)
        self.scenarios_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.scenarios_button.setText("Scenarios")

        self.quit_app_button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_app_button.setGeometry(QtCore.QRect(1200, 15, 40, 40))
        self.quit_app_button.setFont(QtGui.QFont("Hiragino Sans GB", 40, True))
        self.quit_app_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.quit_app_button.setStyleSheet(self.QUIT_BUTTON_STYLESHEETSHEET)
        self.quit_app_button.setText("X")

        # Toggle sidebar button
        self.toggle_sidebar_button = QtWidgets.QPushButton(self.centralwidget)
        self.toggle_sidebar_button.setGeometry(QtCore.QRect(1230, 390, 55, 55))
        self.toggle_sidebar_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toggle_sidebar_button.setStyleSheet("border:none")
        icon = QtGui.QIcon("./Static/Forward_Arrow.png")
        self.toggle_sidebar_button.setIcon(icon)
        self.toggle_sidebar_button.setIconSize(QtCore.QSize(55, 55))

    def setupMenuBar(self, MainWindow):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        MainWindow.setMenuBar(self.menubar)

    # --------------------------------------------------------------------------------------------------------------------------------------

    def createHorizontalLayout(self, parent, x, y, width, height):
        widget = QtWidgets.QWidget(parent)
        widget.setGeometry(QtCore.QRect(x, y, width, height))
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setObjectName(f"horizontalLayoutWidget_{x}_{y}")
        return layout

    def createLabel(self, layout, pixmap=None, max_size=50, text_font=None, isVisible=True):
        label = QtWidgets.QLabel(layout.parent())
        if pixmap:
            label.setPixmap(QtGui.QPixmap(pixmap))
        if text_font:
            font = QtGui.QFont()
            font.setFamily(text_font[0])
            font.setPointSize(text_font[1])
            label.setFont(font)
        label.setStyleSheet("color:white")
        label.setMaximumSize(QtCore.QSize(*([max_size] * 2 if isinstance(max_size, int) else max_size)))
        label.setScaledContents(True)
        layout.addWidget(label)
        if not isVisible:
            label.hide()
        return label

    def createButton(self, layout, text, method=None, isVisible=True):
        button = QtWidgets.QPushButton(layout.parent())
        button.setMaximumSize(QtCore.QSize(150, 50))
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(self.BUTTON_STYLESHEET)
        layout.addWidget(button)
        button.setText(text)
        button.setObjectName(f"{text.lower().replace(' ', '_')}_button")
        if method:
            button.clicked.connect(method)
        if not isVisible:
            button.hide()
        return button

    def createSlider(self, layout, min_value=0, max_value=100, initial_value=50, orientation=QtCore.Qt.Horizontal, isVisible=True):
        # Create a horizontal layout for the slider and label
        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(10)

        # Create the slider
        slider = QtWidgets.QSlider(orientation, layout.parent())
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(initial_value)
        slider.setMaximumWidth(200)
        slider.setStyleSheet(self.SLIDER_STYLESHEET)
        if not isVisible:
            slider.hide()

        # Add the slider and label to the horizontal layout
        slider_layout.addWidget(slider)

        # Add the horizontal layout to the parent layout
        layout.addLayout(slider_layout)

        return slider

    def createSpinBox(self, layout, min_value=0, max_value=100, initial_value=50, isVisible=True):
        spin_box = QtWidgets.QSpinBox(layout.parent())
        spin_box.setMinimum(min_value)
        spin_box.setMaximum(max_value)
        spin_box.setValue(initial_value)
        spin_box.setMaximumSize(260, 40)  # Set maximum width and height
        spin_box.setStyleSheet(self.SPINBOX_STYLESHEET)
        if not isVisible:
            spin_box.hide()

        # Add the spin box to the layout
        layout.addWidget(spin_box)

        return spin_box

    def format_frequency(self, freq):
        if freq is None:
            return "Frequency not set"  # Return a default message or handle this scenario appropriately

        # Helper function to format frequency with or without decimal point as necessary
        def format_value(value, unit):
            if value.is_integer():
                return f"{int(value)} {unit}"  # Convert to integer and format if no decimal part
            else:
                return f"{value:.1f} {unit}"  # Keep one decimal if there is a significant digit

        if freq >= 1e9:
            return format_value(freq / 1e9, "GHz")
        elif freq >= 1e6:
            return format_value(freq / 1e6, "MHz")
        else:
            return f"{freq} Hz"  # Frequency values below 1 MHz are less likely to need fractional display

    def createComboBox(self, layout, options, default_value=None, placeholder="Options", isEditable=False, isVisible=True):
        # Convert frequency values to strings if they are not already
        if options and isinstance(options[0], float):  # Check if the first item is a float
            options = [self.format_frequency(freq) for freq in options]

        combo_box = QtWidgets.QComboBox(layout.parent())
        combo_box.addItems(options)
        combo_box.setEditable(isEditable)
        combo_box.setMaximumSize(260, 40)
        combo_box.setStyleSheet(self.COMBOBOX_STYLESHEET)

        # Insert and set a placeholder if no default value is specified or not found in options
        if not default_value or default_value not in options:
            combo_box.insertItem(0, placeholder)  # Insert placeholder at the top
            combo_box.setCurrentIndex(0)
            combo_box.model().item(0).setEnabled(False)  # Disable the placeholder so it can't be selected

        # If a valid default value is provided, set it as the current item
        elif default_value and default_value in options:
            combo_box.setCurrentText(default_value)

        if not isVisible:
            combo_box.hide()

        # Add the combo box to the layout
        layout.addWidget(combo_box)

        return combo_box

    # --------------------------------------------------------------------------------------------------------------------------------------

    def updateVisualization(self):
        spacing_factor = 5
        if self.current_selected_ALL_array:
            for i in range(1, self.current_arrays_number + 1):
                self.visualization_widget.editArray(
                    index=self.current_selected_array + i,
                    spacing=self.current_elements_spacing * spacing_factor,
                    num_elements=self.current_elements_number,
                    curvature_angle=self.current_array_curvature_angle,
                )
        else:
            self.visualization_widget.editArray(
                index=self.current_selected_array,
                spacing=self.current_elements_spacing * spacing_factor,
                num_elements=self.current_elements_number,
                curvature_angle=self.current_array_curvature_angle,
            )

    # --------------------------------------------------------------------------------------------------------------------------------------
    def return_main_initial_button(self):
        if self.return_main_buttons.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            self.show_button([self.adjust_array_number, self.elements_number_button, self.elements_spacing_button,
                              self.add_curve_button])

    def return_sidebar_initial_button(self):
        if self.return_sidebar_buttons.isVisible():
            self.hide_button(self.SIDEBAR_CONTROLLER_BUTTONS)
            self.show_button([self.operating_frequency_button, self.steering_angle_button])

    def toggle_current_selected_array(self):
        if self.current_selected_ALL_array:
            self.current_selected_ALL_array = not self.current_selected_ALL_array

        next_selected_array = self.current_selected_array + 1

        if next_selected_array <= self.current_arrays_number:
            self.current_selected_array = next_selected_array
            self.current_selected_array_button.setText(f"Array {self.current_selected_array}")
        else:
            self.current_selected_ALL_array = True
            self.current_selected_array_button.setText("All Arrays")
            self.current_selected_array = 0

    def show_curve_input(self):
        if not self.array_curve_slider.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            self.arrays_parameters_indicator.setText(f"{self.current_array_curvature_angle} Degree")
            controller_buttons = [self.return_main_buttons, self.array_curve_slider, self.arrays_parameters_indicator]
            if self.current_arrays_number > 1:
                controller_buttons.append(self.current_selected_array_button)
            self.show_button(controller_buttons)

    def show_spacing_input(self):
        if not self.elements_spacing_slider.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            controller_buttons = [self.return_main_buttons, self.elements_spacing_slider, self.arrays_parameters_indicator]
            if self.current_arrays_number > 1:
                controller_buttons.append(self.current_selected_array_button)
            self.show_button(controller_buttons)
            self.arrays_parameters_indicator.setText(f"{self.elements_spacing_slider.value()} % wavelength")

    def show_arrays_number_SpinBox(self):
        if not self.arrays_number_SpinBox.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            self.arrays_parameters_indicator.setText(f"{self.current_arrays_number} Arrays")
            controller_buttons = [self.return_main_buttons, self.arrays_number_SpinBox, self.arrays_parameters_indicator]
            self.show_button(controller_buttons)

    def show_elements_number_SpinBox(self):
        if not self.elements_number_SpinBox.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            self.arrays_parameters_indicator.setText(f"{self.current_elements_number} Elements")
            controller_buttons = [self.return_main_buttons, self.elements_number_SpinBox, self.arrays_parameters_indicator]
            if self.current_arrays_number > 1:
                controller_buttons.append(self.current_selected_array_button)
            self.show_button(controller_buttons)

    def show_frequency_combobox(self):
        if not self.operating_frequency_combobox.isVisible():
            self.hide_button(self.SIDEBAR_CONTROLLER_BUTTONS)
            controller_buttons = [self.return_sidebar_buttons, self.operating_frequency_combobox, self.sidebar_parameter_indicator]
            self.show_button(controller_buttons)
            formatted_frequency = self.format_frequency(self.current_operating_frequency)
            self.sidebar_parameter_indicator.setText(formatted_frequency)

    def show_steering_angle_slider(self):
        if not self.steering_angle_slider.isVisible():
            self.hide_button(self.SIDEBAR_CONTROLLER_BUTTONS)
            controller_buttons = [self.return_sidebar_buttons, self.steering_angle_slider, self.sidebar_parameter_indicator]
            self.show_button(controller_buttons)
            self.sidebar_parameter_indicator.setText(f"{self.current_steering_angle} Degree")

    # --------------------------------------------------------------------------------------------------------------------------------------

    def hide_button(self, buttons):
        for button in buttons:
            if button.isVisible():
                button.hide()

    def show_button(self, buttons):
        for button in buttons:
            if not button.isVisible():
                button.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Transmitter Beamforming Simulator"))
        self.title_label.setText(_translate("MainWindow", "Transmitter Beamforming Simulator"))
