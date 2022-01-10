from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_builder import kivy_builder

# from kivy.core.window import Window
# Window.size = (540, 960)  # phone size, can be commented out

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

    def show_data(self):
        close_button = MDRaisedButton(text="Close", on_release=self.close_dialog)
        more_button = MDFlatButton(text="Forgot Password")
        if self.login_ids.username.text is "":
            check_string = 'Please enter a username'
            self.dialog = MDDialog(title='Username Check', text=check_string, buttons=[more_button, close_button])
            self.dialog.open()
        elif self.login_ids.username.text is "Invalid":
            check_string = 'Username is Invalid'
            self.dialog = MDDialog(title='Username Check', text=check_string, buttons=[more_button, close_button])
            self.dialog.open()
        else:
            self.root.transition.direction = "left"
            self.root.transition.mode = "push"
            self.screen.current = 'home'
        # print(self.login_ids.username.text)

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def profile(self):
        self.dialog = MDDialog(text="Profile")
        self.dialog.open()

    def navigation_draw(self):
        pass

    def logout(self):
        self.login_ids.username.set_text(None, "")
        self.login_ids.password.set_text(None, "")
        self.root.transition.direction = "right"
        self.root.transition.mode = "push"
        self.screen.current = 'login'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.screen


FinalApp().run()
