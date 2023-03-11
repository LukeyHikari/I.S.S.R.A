from sys import _xoptions
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition  
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2 as cam

Window.size = (360,640)

class SnapScore(MDApp):
    global smanager
    smanager = ScreenManager()

    def build(self):
        self.title = "SnapScore"
        #Add the screens to the main screen manager
        self.main_screen = Builder.load_file('snapscore.kv')
        self.open_screen = Builder.load_file('openscreen.kv') 
        smanager.add_widget(self.open_screen) 
        smanager.add_widget(self.main_screen)

        #Live camera capture
        self.capture = cam.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)

        #Screen capture function binding   
        self.main_screen.ids.cam_button.bind(on_press=self.take_pic)

        return smanager

    def on_start(self): #Screen transition on start
        Clock.schedule_once(self.change_screen, 5)

    def change_screen(self, dt): #Screen transition properties
        smanager.transition = FadeTransition(clearcolor=(0,0,0,0))
        smanager.duration = 3 
        smanager.current = "mscreen"

    def load_video(self, *args): #Live camera properties
        ret, frame = self.capture.read()
        self.image_frame = cam.flip(frame, 1)
        buffer = cam.flip(frame, -1).tobytes()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt = 'bgr')
        texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.main_screen.ids.cam.texture = texture

    def take_pic(self, *args): #Capture function 
        image_name = "App/temp/picture.png"
        cam.imwrite(image_name, self.image_frame)

if __name__ == '__main__':
    SnapScore().run()