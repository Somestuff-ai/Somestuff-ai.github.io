import time
import ctypes
import win32gui
import win32api
import win32con
import pyautogui

# Callback function for window enumeration
def EnumWindowCallback(hwnd, lParam):
    global HWND_CalSheet
    text = win32gui.GetWindowText(hwnd)
    if "Calibration entry sheet" in text:
        HWND_CalSheet = hwnd

        return False
    return True

# Simulate clicking on "Take Measurements" button
def take_measurement(hwnd_cal_sheet, hwnd_take_meas):
    win32gui.SetForegroundWindow(hwnd_cal_sheet)
    rect = win32gui.GetWindowRect(hwnd_take_meas)
    center_x = (rect[0] + rect[2]) // 2
    center_y = (rect[1] + rect[3]) // 2
    pyautogui.click(center_x, center_y)

# Check if the button click was successful
def is_button_greyed_out(hwnd_take_meas):
    text_buffer = ctypes.create_unicode_buffer(256)
    win32gui.SendMessage(hwnd_take_meas, win32con.WM_GETTEXT, 256, text_buffer)
    return not text_buffer.value.startswith("Take")



# Main function to take CS043 reading
def take_cs043_reading():
    global HWND_CalSheet
    HWND_CalSheet = 0
    try:
        win32gui.EnumWindows(EnumWindowCallback, 0)
    except:
        if HWND_CalSheet != 0:
            hwnd_take_meas = win32gui.FindWindowEx(HWND_CalSheet, 0, None, "Take Measurement")
            if hwnd_take_meas != 0:
                while True:
                    take_measurement(HWND_CalSheet, hwnd_take_meas)
                    time.sleep(0.4)
                    if is_button_greyed_out(hwnd_take_meas):
                        break
                text = ""
                text_buffer = ctypes.create_unicode_buffer(256)  # Create a buffer to hold the text
                while not text_buffer.value.startswith("Take"):
                    time.sleep(0.2)
                    win32gui.SendMessage(hwnd_take_meas, win32con.WM_GETTEXT, 256, text_buffer)  # Use the buffer to receive the text
                    text = text_buffer.value  # Update the value of text
                return