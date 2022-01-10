from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_builder import kivy_builder
from kivymd.toast import toast
from connector import Database

from kivy.core.window import Window
Window.size = (540/1.25, 960/1.25)  # phone size, can be commented out

dbUsername = "u770933303_test"
dbPassword = "Test1234"
dbHostname = "156.67.73.101"
dbDatabase = "u770933303_test"

class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(HomeScreen(name='home'))


class FinalApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog()
        self.screen = Builder.load_string(kivy_builder)
        self.login_ids = self.screen.get_screen('login').ids
        self.home_ids = self.screen.get_screen('home').ids

    def login(self):
        db = Database(dbUsername,dbPassword,dbHostname,dbDatabase)
        close_button = MDRaisedButton(text="Close", on_release=self.close_dialog)
        more_button = MDFlatButton(text="Forgot Password", on_release=self.comingSoonToast)
        self.dialog = MDDialog(title='Username Check', buttons=[more_button, close_button])
        username = self.login_ids.username.text
        password = self.login_ids.password.text
        if username == "" or password == "":
            self.dialog.text = 'Please enter all fields'
            self.dialog.open()
        else:
            if db.isExisting(username):
                if db.isUserPass(username, password):
                    self.screen.current = 'home'
                else:
                    self.dialog.text = 'Incorrect password'
                    self.dialog.open()
            else:
                db.createAcc(username, password)
                self.dialog.text = 'Account has been created. Please login again'
                self.dialog.open()
        # print(self.login_ids.username.text)

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def comingSoonToast(self, obj):
        toast("Feature Coming Soon")

    def profile(self):
        self.dialog = MDDialog(text="Profile")
        self.dialog.open()

    def navigation_draw(self):
        pass

    def logout(self):
        self.login_ids.username.set_text(None, "")
        self.login_ids.password.set_text(None, "")
        self.screen.current = 'login'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.screen


FinalApp().run()
