from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSerialPort import *
from PyQt5.QtWidgets import *

from ..port_config import port_config, tracking_config


class stage:

    def __init__(self) -> None:

        self._connect_btn = QPushButton()
        self.ZPosition = 50000
        self.LastCmd = ''
        self.Received = ''
        self.center_pixel = 64
        self.piezoTracking = False
        self.pConst = 26.45
        self.iConst = 0.0
        self.dConst = 0.0
        self.tau = 0.0
        self.threshold = 0.016

    def isOpen(self):
        '''Returns True if connected.'''
        return False


class piezo_concept(stage):
    '''PiezoConcept FOC 1-axis stage adapter | Inherits QSerialPort
    '''

    def __init__(self):
        self.pixel_slider = None
        self.peak_position = 0.0
        self.pixel_coeff = 0.01

        super().__init__()

        self.serial = QSerialPort(
            None,
            readyRead=self.rx_piezo
        )
        self.serial.setBaudRate(115200)
        self.serial.setPortName('COM5')

    def isOpen(self):
        '''Returns True if connected.'''
        return self.serial.isOpen()

    def open(self):
        '''Opens the serial port.'''
        self.serial.open(QIODevice.ReadWrite)

    def close(self):
        '''Closes the supplied serial port.'''
        self.serial.close()

    def setPortName(self, name: str):
        '''Sets the serial port name.'''
        self.serial.setPortName(name)

    def setBaudRate(self, baudRate: int):
        '''Sets the serial port baudrate.'''
        self.serial.setBaudRate(baudRate)

    def open_dialog(self):
        '''Opens a port config dialog
        for the serial port.
        '''
        dialog = port_config()
        if not self.isOpen():
            if dialog.exec_():
                portname, baudrate = dialog.get_results()
                self.setPortName(portname)
                self.setBaudRate(baudrate)

    def track_dialog(self):
        '''Opens a port config dialog
        for the serial port.
        '''
        dialog = tracking_config(
            self.pConst, self.iConst, self.dConst,
            self.tau, self.threshold)
        if not self.isOpen():
            if dialog.exec_():
                (self.pConst, self.iConst, self.dConst,
                 self.tau, self.threshold) = dialog.get_results()

    def write(self, value):
        self.serial.write(value)

    def GETZ(self):
        '''Gets the current stage position along the Z axis.
        '''
        if (self.isOpen()):
            self.write(b'GET_Z\n')
            self.LastCmd = 'GETZ'

    def HOME(self):
        '''Centers the stage position along the Z axis.
        '''
        if (self.isOpen()):
            self.ZPosition = 50000
            self.write(b'MOVEZ 50u\n')
            self.LastCmd = 'MOVRZ'

    def NANO_UP(self, step: int):
        '''Moves the stage in the positive direction along the Z axis
        by the specified step in nanometers relative to its last position.
        (Not prefered check UP, DOWN, HOME, REFRESH functions instead)

        Parameters
        ----------
        step : int
            step in nanometers
        '''
        if (self.isOpen()):
            self.write(('MOVRZ +'+step+'n\n').encode('utf-8'))
            self.LastCmd = 'MOVRZ'

    def MICRO_UP(self, step: int):
        '''Moves the stage in the positive direction along the Z axis
        by the specified step in micrometers relative to its last position.
        (Not prefered check UP, DOWN, HOME, REFRESH functions instead)

        Parameters
        ----------
        step : int
            step in micrometers
        '''
        if (self.isOpen()):
            self.write(('MOVRZ +'+step+'u\n').encode('utf-8'))
            self.LastCmd = 'MOVRZ'

    def NANO_DOWN(self, step: int):
        '''Moves the stage in the negative direction along the Z axis
        by the specified step in nanometers relative to its last position.
        (Not prefered check UP, DOWN, HOME, REFRESH functions instead)

        Parameters
        ----------
        step : int
            step in nanometers
        '''
        if (self.isOpen()):
            self.write(('MOVRZ -'+step+'n\n').encode('utf-8'))
            self.LastCmd = 'MOVRZ'

    def MICRO_DOWN(self, step: int):
        '''Moves the stage in the negative direction along the Z axis
        by the specified step in micrometers relative to its last position.
        (Not prefered check UP, DOWN, HOME, REFRESH functions instead)

        Parameters
        ----------
        step : int
            step in micrometers
        '''
        if (self.isOpen()):
            self.write(('MOVRZ -'+step+'u\n').encode('utf-8'))
            self.LastCmd = 'MOVRZ'

    def UP(self, step: int, interface=False):
        '''Moves the stage in the positive direction along the Z axis
        by the specified step in nanometers
        relative to the last position set by the user.

        Parameters
        ----------
        step : int
            step in nanometers
        '''
        if (self.isOpen()):
            if self.piezoTracking and \
                    self.pixel_translation.isChecked() and interface:
                self.center_pixel += self.coeff_pixel * step
            else:
                self.ZPosition = min(max(self.ZPosition + step, 0), 100000)
                self.write(
                    ('MOVEZ '+str(self.ZPosition)+'n\n').encode('utf-8'))
                self.LastCmd = 'MOVEZ'

    def DOWN(self, step: int, interface=False):
        '''Moves the stage in the negative direction
        along the Z axis by the specified step in nanometers
        relative to the last position set by the user.

        Parameters
        ----------
        step : int
            step in nanometers
        '''
        if (self.isOpen()):
            if self.piezoTracking and \
                    self.pixel_translation.isChecked() and interface:
                self.center_pixel -= self.coeff_pixel * step
            else:
                self.ZPosition = min(max(self.ZPosition - step, 0), 100000)
                self.write(
                    ('MOVEZ '+str(self.ZPosition)+'n\n').encode('utf-8'))
                self.LastCmd = 'MOVEZ'

    def REFRESH(self):
        '''Refresh the stage position
        to the set value in case of discrepancy.
        '''
        if (self.isOpen()):
            self.write(('MOVEZ '+str(self.ZPosition)+'n\n').encode('utf-8'))
            self.LastCmd = 'MOVEZ'

    def rx_piezo(self):
        '''PiezoConcept stage dataReady signal.
        '''
        self.Received = str(
            self.serial.readAll(),
            encoding='utf8')
        if self.LastCmd != 'GETZ':
            self.GETZ()

    def autoFocusTracking(self):
        '''Toggles autofocus tracking option.
        '''
        if self.piezoTracking:
            self.piezoTracking = False
            self._tracking_btn.setText('Focus Tracking Off')
        else:
            self.piezoTracking = True
            self._tracking_btn.setText('Focus Tracking On')

    @property
    def center_pixel(self):
        return self.peak_position

    @center_pixel.setter
    def center_pixel(self, value):
        self.peak_position = value
        if self.pixel_slider is None:
            return False
        else:
            self.pixel_slider.setValue(value)
            return True

    @property
    def coeff_pixel(self):
        return self.pixel_coeff

    @coeff_pixel.setter
    def coeff_pixel(self, value):
        self.pixel_coeff = value
        if self.pixel_cal is None:
            return False
        else:
            self.pixel_cal.setValue(value)
            return True

    def getQWidget(self):
        '''Generates a QGroupBox with
        stage controls.'''
        group = QGroupBox('PiezoConcept FOC100')
        layout = QFormLayout()
        group.setLayout(layout)

        # Piezostage controls
        self._connect_btn = QPushButton(
            'Connect',
            clicked=lambda: self.open()
        )
        self._disconnect_btn = QPushButton(
            'Disconnect',
            clicked=lambda: self.close()
        )
        self._config_btn = QPushButton(
            'Config.',
            clicked=lambda: self.open_dialog()
        )
        self._tracking_conf_btn = QPushButton(
            'Tracking Config.',
            clicked=lambda: self.track_dialog()
        )
        self._tracking_btn = QPushButton(
            'Focus Tracking Off',
            clicked=lambda: self.autoFocusTracking()
        )

        self._inverted = QCheckBox('Inverted')
        self._inverted.setChecked(False)

        fine_step = 100
        coarse_step = 1
        self.fine_steps_label = QLabel('Fine step [nm]')
        self.fine_steps_slider = QSpinBox()
        self.fine_steps_slider.setMinimum(1)
        self.fine_steps_slider.setMaximum(1000)
        self.fine_steps_slider.setValue(fine_step)
        self.fine_steps_slider.setStyleSheet(
            'background-color: green')

        self.coarse_steps_label = QLabel(
            'Coarse step [um]')
        self.coarse_steps_slider = QSpinBox()
        self.coarse_steps_slider.setMinimum(1)
        self.coarse_steps_slider.setMaximum(20)
        self.coarse_steps_slider.setValue(coarse_step)

        self.pixel_slider = QDoubleSpinBox()
        self.pixel_slider.setMinimum(0)
        self.pixel_slider.setMaximum(10000)
        self.pixel_slider.setDecimals(3)
        self.pixel_slider.setSingleStep(0.005)
        self.pixel_slider.setValue(0)

        self.pixel_cal = QDoubleSpinBox()
        self.pixel_cal.setMinimum(0)
        self.pixel_cal.setMaximum(10000)
        self.pixel_cal.setDecimals(6)
        self.pixel_cal.setSingleStep(0.005)
        self.pixel_cal.setValue(0.01)

        self.pixel_translation = QCheckBox('Use Calibration')
        self.pixel_translation.setChecked(False)

        self.piezo_HOME_btn = QPushButton(
            '⌂',
            clicked=lambda: self.HOME()
        )
        self.piezo_REFRESH_btn = QPushButton(
            'R',
            clicked=lambda: self.REFRESH()
        )
        self.piezo_B_UP_btn = QPushButton(
            '<<',
            clicked=lambda: self.UP(
                self.coarse_steps_slider.value() * 1000,
                True)
        )
        self.piezo_S_UP_btn = QPushButton(
            '<',
            clicked=lambda: self.UP(
                self.fine_steps_slider.value(),
                True)
        )
        self.piezo_S_DOWN_btn = QPushButton(
            '>',
            clicked=lambda: self.DOWN(
                self.fine_steps_slider.value(),
                True)
        )
        self.piezo_B_DOWN_btn = QPushButton(
            '>>',
            clicked=lambda: self.DOWN(
                self.coarse_steps_slider.value() * 1000,
                True)
        )
        self.move_buttons = QHBoxLayout()
        self.move_buttons.addWidget(self.piezo_HOME_btn)
        self.move_buttons.addWidget(self.piezo_REFRESH_btn)
        self.move_buttons.addWidget(self.piezo_B_UP_btn)
        self.move_buttons.addWidget(self.piezo_S_UP_btn)
        self.move_buttons.addWidget(self.piezo_S_DOWN_btn)
        self.move_buttons.addWidget(self.piezo_B_DOWN_btn)

        btns = QHBoxLayout()
        btns.addWidget(self._connect_btn)
        btns.addWidget(self._disconnect_btn)
        btns.addWidget(self._config_btn)
        layout.addRow(btns)
        layout.addRow(
            self.fine_steps_label,
            self.fine_steps_slider)
        layout.addRow(
            self.coarse_steps_label,
            self.coarse_steps_slider)
        layout.addRow(self.move_buttons)
        layout.addRow(
            QLabel('Tracking:'), self._tracking_conf_btn)
        layout.addRow(
            QLabel('Fit to Pixel:'), self.pixel_slider)
        layout.addRow(
            QLabel('Pixel Calibration:'), self.pixel_cal)
        layout.addWidget(self._tracking_btn)
        layout.addWidget(self._inverted)
        layout.addWidget(self.pixel_translation)

        return group
