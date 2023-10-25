from inputs import get_gamepad
import pyautogui
import math
import threading

pyautogui.PAUSE = 0

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)
    

    def __init__(self):
        
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode
        x = round(self.LeftJoystickX,2)
        y = round(self.LeftJoystickY,2)
        a = self.A
        b = self.B 
        _x = self.X
        _y = self.Y
        right_trigger = round(self.RightTrigger,2)
        return [x, y, a, b, _x, _y, right_trigger]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

class Mouse():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.speed = 0.25
        self.deadzone = 0.05
        self.can_click = True
        
    def move(self,left,right):
        if abs(left) > self.deadzone:
            self.x += left*self.speed
        if abs(right) > self.deadzone:
            self.y += right*self.speed*-1
            
    def click(self):
        if joy.A == 1 and self.can_click == True:
            self.can_click = False
            pyautogui.click()
        elif joy.A == 0:
            self.can_click = True



if __name__ == '__main__':
    joy = XboxController()
    mouse = Mouse()
    
    while True:
        controller = joy.read()
        print(controller)
        mouse.pos = mouse.move(joy.LeftJoystickX,joy.LeftJoystickY)
        mouse.click()
        pyautogui.moveTo(mouse.x,mouse.y,0)
        
        # End the program if start key is pressed
        if joy.Back == 1:
            print("Start button is pressed. Stopping the program.")
            break
        