from sys import _xoptions
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition  
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
import os
import cv2 as cam
import googleapi
import digit_rec

Window.size = (360,640)
sheets = googleapi.recording()
preprocess = digit_rec.recognition()
ocr = digit_rec.scoresocr()

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
        
        self.acttype = ""
        self.maxgrade = None
        self.nostuds = None
        self.actnumber = None

        #Live camera capture
        # self.capture = cam.VideoCapture(1) #0
        # Clock.schedule_interval(self.load_video, 1.0/30.0)

        #Screen capture function binding   
        self.main_screen.ids.cam_button.bind(on_press=self.take_pic)

        #Task Button Events and Widgets
        self.highinputfield = MDTextField(
            id = "highinputfield",
            hint_text = 'Highest Score',
            helper_text_mode = "on_focus",
            max_text_length = 3,
            mode = "fill",
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            size_hint = (0.5,1)
        )
        self.setbuttonmax = MDRectangleFlatButton(
            text = "Set",
            text_color = "white",
            md_bg_color = "#50018c",
            pos_hint = {'center_x': 0.65, 'center_y': 0.42},
            on_press = self.retrievemax
        )  
        self.nostudsfield = MDTextField(
            id = "nostudsfield",
            hint_text = 'Number of Students',
            helper_text_mode = "on_focus",
            max_text_length = 3,
            mode = "fill",
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            size_hint = (0.5,1)
        )
        self.setbuttonno = MDRectangleFlatButton(
            text = "Set",
            text_color = "white",
            md_bg_color = "#50018c",
            pos_hint = {'center_x': 0.65, 'center_y': 0.42},
            on_press = self.get_nostuds
        )

        self.main_screen.ids.pt_button.bind(on_press=self.set_pt)
        self.main_screen.ids.wt_button.bind(on_press=self.set_wt)
        self.main_screen.ids.qt_button.bind(on_press=self.set_qt)
        self.main_screen.ids.actno_button.bind(on_press=self.setano)
        self.main_screen.ids.save_button.bind(on_press=self.savescores)

        #Temporary For Sudo Testing
        self.workingscore = 1
        self.tempimagedirectory = f'temp/{self.workingscore}.png'
        self.scorepreview = Image(
            source = self.tempimagedirectory,
            pos_hint = {'center_x': .5, 'center_y': .5},
            size_hint = (.5,.5)
        )
        self.main_screen.add_widget(self.scorepreview)

        return smanager

    def on_start(self): #Screen transition on start
        if os.path.exists(f'{os.getcwd()}/temp/'):
            print('Temp Folder Exists')
        else:
            os.makedirs(f'{os.getcwd()}/temp/')
        Clock.schedule_once(self.change_screen, 5)

    def change_screen(self, dt): #Screen transition properties
        smanager.transition = FadeTransition(clearcolor=(0,0,0,0))
        smanager.duration = 3 
        smanager.current = "mscreen"

    def load_video(self, *args): #Live camera properties
        ret, frame = self.capture.read()
        self.image_frame = cam.flip(frame,1)
        buffer = cam.flip(frame, -1).tobytes()
        texture = Texture.create(
           size=(frame.shape[1], frame.shape[0]), colorfmt = 'bgr')
        texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
        self.main_screen.ids.cam.texture = texture

    def take_pic(self, *args): #Capture function 
        #image_name = "temp/beingrecorded.jpg"
        #cam.imwrite(image_name, self.image_frame)

        #segmented = preprocess.combinedbox(image_name)
        #indiv_score = ocr.identify_score(segmented)
        indiv_score = ocr.identify_score(self.tempimagedirectory)

        scoreindex = int(indiv_score[1]) + int(indiv_score[0]) * 10 - 1
        actualscore = int(indiv_score[5]) + int(indiv_score[4]) * 10 + int(indiv_score[3]) * 100

        self.score_list[scoreindex] = actualscore

        print(scoreindex)
        print(actualscore)
        self.workingscore = self.workingscore + 1
        self.tempimagedirectory = f'temp/{self.workingscore}.png'
        print(f'New Working Score:{self.workingscore}')
        self.main_screen.remove_widget(self.scorepreview)
        self.scorepreview = Image(
            source = self.tempimagedirectory,
            pos_hint = {'center_x': .5, 'center_y': .5},
            size_hint = (.5,.5)
        )
        self.main_screen.add_widget(self.scorepreview)
        # try:
        #     os.remove(image_name)
        # except: pass

    def set_pt(self, *args):
        self.acttype = "Performance"
        self.main_screen.add_widget(self.highinputfield)
        self.main_screen.add_widget(self.setbuttonmax)

    def set_wt(self, *args):
        self.acttype = "Written"
        self.main_screen.add_widget(self.highinputfield)
        self.main_screen.add_widget(self.setbuttonmax)

    def set_qt(self, *args):
        self.acttype = "Quarterly"
        self.main_screen.add_widget(self.highinputfield)
        self.main_screen.add_widget(self.setbuttonmax)

    def retrievemax(self, *args):
        self.main_screen.remove_widget(self.highinputfield)
        self.main_screen.remove_widget(self.setbuttonmax)
        self.maxgrade = self.highinputfield.text
        print(self.maxgrade)
        self.main_screen.add_widget(self.nostudsfield)
        self.main_screen.add_widget(self.setbuttonno)
        
    def get_nostuds(self,*args):
        self.main_screen.remove_widget(self.nostudsfield)
        self.main_screen.remove_widget(self.setbuttonno)
        self.nostuds = self.nostudsfield.text
        self.score_list = []
        for prelist in range(int(self.nostuds)):
            self.score_list.append("0")
        print(self.nostuds)
        print(len(self.score_list))

    def setano(self,*args):
        self.actnofield = MDTextField(
            id = "actnofield",
            hint_text = 'Act. #',
            helper_text_mode = "on_focus",
            max_text_length = 3,
            mode = "fill",
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            size_hint = (0.5,1)
        )
        self.setbuttonactno = MDRectangleFlatButton(
            text = "Set",
            text_color = "white",
            md_bg_color = "#50018c",
            pos_hint = {'center_x': 0.65, 'center_y': 0.42},
            on_press = self.get_actno
        )
        self.main_screen.add_widget(self.actnofield)
        self.main_screen.add_widget(self.setbuttonactno)
    
    def get_actno(self,*args):
        self.main_screen.remove_widget(self.actnofield)
        self.main_screen.remove_widget(self.setbuttonactno)
        self.actnumber = self.actnofield.text
        print(self.actnumber)

    def savescores(self,*args):
        sheets.highestgrade(int(self.maxgrade), int(self.actnumber), self.acttype)
        sheets.checkgrade(int(self.nostuds), int(self.actnumber), self.acttype, self.score_list)


SnapScore().run()