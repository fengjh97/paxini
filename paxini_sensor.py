"""
PaXini PX-6AX GEN3 Tactile Sensor Driver
=========================================
Supports: Serial Converter Board (单路串口转接板) via USB (CH343)
Protocol: Custom binary (55 AA / AA 55 frame headers, LRC checksum)
Baud rate: 921600
"""

import serial
import time
import serial.tools.list_ports
from typing import Optional, Dict, List, Tuple


# Sensor model -> distributed force data length (bytes)
SENSOR_MODELS = {
    "S1813_elite": 93,
    "S2015_elite": 156,
    "S1813_core": 153,
    "S2716_core": 348,
    "S3013_core": 288,
    "M2826_omega": 381,
    "L3530_omega": 405,
    "S1610_elite": 75,
    "M2324_core": 204,
    "M3025_core": 231,
    "L5325_omega": 717,
    "M2020_elite": 27,
}


def calculate_lrc(data: bytes) -> int:
    """LRC checksum: sum all bytes, invert, add 1, keep lower 8 bits."""
    lrc = 0
    for byte in data:
        lrc = (lrc + byte) & 0xFF
    return ((~lrc) + 1) & 0xFF


class PaxiniSensor:
    """Driver for PaXini PX-6AX GEN3 tactile sensor via Serial Converter Board."""

    def __init__(self, port: str = "COM3", device_id: int = 3, model: str = "S2716_core"):
        self.port = port
        self.device_id = device_id
        self.model = model
        self.dist_len = SENSOR_MODELS.get(model, 231)
        self.ser: Optional[serial.Serial] = None

    def connect(self) -> bool:
        """Open serial connection at 921600 baud."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=921600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1,
                write_timeout=0.5,
                inter_byte_timeout=0.001,
                xonxoff=False,
                rtscts=False,
            )
            return self.ser.is_open
        except serial.SerialException as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self):
        """Close serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def _build_read_cmd(self, func_code: int, addr: int, data_len: int) -> bytes:
        """Build a read command frame."""
        frame = bytearray([0x55, 0xAA])
        total = 14  # 13-byte header + 1 LRC
        frame.append((total - 5) & 0xFF)
        frame.append(((total - 5) >> 8) & 0xFF)
        frame.append(self.device_id)
        frame.append(0x00)
        frame.append(func_code | 0x80)  # set read bit
        frame.extend(addr.to_bytes(4, "little"))
        frame.extend(data_len.to_bytes(2, "little"))
        frame.append(calculate_lrc(bytes(frame)))
        return bytes(frame)

    def _build_write_cmd(self, func_code: int, addr: int, data: bytes) -> bytes:
        """Build a write command frame."""
        data_len = len(data)
        total = 13 + data_len + 1  # header + data + LRC
        frame = bytearray([0x55, 0xAA])
        frame.append((total - 5) & 0xFF)
        frame.append(((total - 5) >> 8) & 0xFF)
        frame.append(self.device_id)
        frame.append(0x00)
        frame.append(func_code & 0x7F)  # clear read bit
        frame.extend(addr.to_bytes(4, "little"))
        frame.extend(data_len.to_bytes(2, "little"))
        frame.extend(data)
        frame.append(calculate_lrc(bytes(frame)))
        return bytes(frame)

    def _send_receive(self, frame: bytes, timeout: float = 0.5) -> Optional[bytes]:
        """Send a frame and receive the response."""
        if not self.ser or not self.ser.is_open:
            return None
        self.ser.reset_input_buffer()
        self.ser.write(frame)
        time.sleep(0.01)

        response = b""
        start = time.time()
        while time.time() - start < timeout:
            if self.ser.in_waiting > 0:
                response += self.ser.read(self.ser.in_waiting)
            time.sleep(0.001)

        if not response or response[:2] != b"\xaa\x55":
            return None
        return response

    def _verify_response(self, resp: bytes) -> bool:
        """Verify response frame: header, length, LRC checksum, status byte."""
        if len(resp) < 14:
            return False
        if resp[:2] != b"\xaa\x55":
            return False
        # Verify LRC: calculated over all bytes before LRC position
        resp_length = int.from_bytes(resp[2:4], byteorder="little")
        lrc_pos = 4 + resp_length
        if lrc_pos >= len(resp):
            return False
        calc_lrc = calculate_lrc(resp[:lrc_pos])
        if calc_lrc != resp[lrc_pos]:
            return False
        # Check status byte (position 13, 0 = success)
        if resp[13] != 0x00:
            return False
        return True

    # Response frame structure (confirmed by C code UART Example.c line 142):
    #   [0-1]   AA 55         Frame header
    #   [2-3]   Length        Payload length (little-endian)
    #   [4]     DeviceAddr    Device address
    #   [5]     Reserved      Always 0x00
    #   [6]     FuncCode      Function code
    #   [7-10]  Address       Start address (4 bytes, little-endian)
    #   [11-12] DataLen       Data length field
    #   [13]    Status        Status byte (0x00 = success)
    #   [14+]   Data          Actual sensor data starts here
    #   [last]  LRC           Checksum
    #
    # NOTE: The official Read_Single_Sensor_Usb.py uses data_start=13
    # which is INCORRECT — it includes the status byte as data.
    # USB_UI.py correctly uses data_start=14. We follow USB_UI.py.
    DATA_START = 14

    def calibrate(self) -> bool:
        """Calibrate the sensor (zero out current readings)."""
        cmd = self._build_write_cmd(0x79, 0x0003, bytes([0x01]))
        resp = self._send_receive(cmd, timeout=1.0)
        if resp is None:
            return False
        return self._verify_response(resp)

    def read_resultant_force(self) -> Optional[Tuple[float, float, float]]:
        """Read resultant 3-axis force (Fx, Fy, Fz) in Newtons."""
        cmd = self._build_read_cmd(0x7B, 0x000003F0, 3)
        resp = self._send_receive(cmd, timeout=0.2)
        if not resp or not self._verify_response(resp):
            return None
        if len(resp) < self.DATA_START + 3:
            return None
        fx_raw = resp[self.DATA_START]
        fy_raw = resp[self.DATA_START + 1]
        fz_raw = resp[self.DATA_START + 2]
        # X, Y are signed int8 (-12.8 ~ +12.7 N); Z is unsigned uint8 (0 ~ 25.5 N)
        fx = (fx_raw if fx_raw <= 127 else fx_raw - 256) * 0.1
        fy = (fy_raw if fy_raw <= 127 else fy_raw - 256) * 0.1
        fz = fz_raw * 0.1
        return (fx, fy, fz)

    def read_distributed_force(self) -> Optional[List[Tuple[float, float, float]]]:
        """Read distributed force for all sensing points. Returns list of (Fx, Fy, Fz) tuples."""
        cmd = self._build_read_cmd(0x7B, 0x0000040E, self.dist_len)
        resp = self._send_receive(cmd, timeout=0.5)
        if not resp or not self._verify_response(resp):
            return None
        if len(resp) < self.DATA_START + self.dist_len:
            return None

        data = resp[self.DATA_START : self.DATA_START + self.dist_len]
        points = []
        for i in range(0, len(data) - 2, 3):
            b1, b2, b3 = data[i], data[i + 1], data[i + 2]
            fx = (b1 if b1 <= 127 else b1 - 256) * 0.1
            fy = (b2 if b2 <= 127 else b2 - 256) * 0.1
            fz = b3 * 0.1
            points.append((fx, fy, fz))
        return points


def find_sensor_port() -> Optional[str]:
    """Auto-detect PaXini sensor port (CH343 USB serial)."""
    for port in serial.tools.list_ports.comports():
        if "CH343" in (port.description or ""):
            return port.device
    return None


def find_device_id(port: str) -> Optional[int]:
    """Scan device addresses 1-6 to find the connected sensor."""
    for dev_id in range(1, 7):
        try:
            ser = serial.Serial(port, 921600, timeout=0.1, write_timeout=0.5)
            frame = bytearray(
                [0x55, 0xAA, 0x09, 0x00, dev_id, 0x00, 0xFB, 0xF0, 0x03, 0x00, 0x00, 0x03, 0x00]
            )
            frame.append(calculate_lrc(bytes(frame)))
            ser.reset_input_buffer()
            ser.write(bytes(frame))
            time.sleep(0.1)
            resp = b""
            start = time.time()
            while time.time() - start < 0.3:
                if ser.in_waiting > 0:
                    resp += ser.read(ser.in_waiting)
                time.sleep(0.005)
            ser.close()
            if resp and resp[:2] == b"\xaa\x55":
                return dev_id
        except serial.SerialException:
            pass
    return None


# ===== Main demo =====
if __name__ == "__main__":
    print("=== PaXini PX-6AX GEN3 Sensor Demo ===\n")

    # Auto-detect port
    port = find_sensor_port()
    if not port:
        print("No CH343 serial port found. Check USB connection.")
        exit(1)
    print(f"Found sensor port: {port}")

    # Auto-detect device ID
    print("Scanning device addresses...")
    dev_id = find_device_id(port)
    if not dev_id:
        print("No sensor responded. Check connections.")
        exit(1)
    print(f"Found sensor at device address: {dev_id}")

    # Connect and calibrate
    sensor = PaxiniSensor(port=port, device_id=dev_id)
    if not sensor.connect():
        print("Failed to connect.")
        exit(1)
    print("Connected!\n")

    print("Calibrating...")
    if sensor.calibrate():
        print("Calibration OK\n")
    else:
        print("Calibration failed\n")

    # Read loop
    print("Reading force data (press Ctrl+C to stop):")
    print(f"{'#':>5} | {'X(N)':>7} | {'Y(N)':>7} | {'Z(N)':>7}")
    print("-" * 37)

    try:
        i = 0
        while True:
            force = sensor.read_resultant_force()
            if force:
                fx, fy, fz = force
                print(f"{i:5d} | {fx:7.1f} | {fy:7.1f} | {fz:7.1f}")
            i += 1
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        sensor.disconnect()
        print("Disconnected.")
