from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.spinner import MDSpinner

from kivy_builder import kivy_builder
from kivymd.toast import toast
from kivy.clock import Clock
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

class ProfileCard(MDCard, RoundedRectangularElevationBehavior):
    pass


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(HomeScreen(name='home'))


class FinalApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog()
        self.loading = MDDialog(text="Loading")
        self.screen = Builder.load_string(kivy_builder)
        self.login_ids = self.screen.get_screen('login').ids
        self.home_ids = self.screen.get_screen('home').ids
        self.db = Database(dbUsername, dbPassword, dbHostname, dbDatabase)

    def login(self):
        self.run_loading()
        Clock.schedule_once(self.login_process)
    def login_process(self, *args):
        close_button = MDRaisedButton(text="Close", on_release=self.close_dialog)
        more_button = MDFlatButton(text="Forgot Password", on_release=self.comingSoonToast)
        self.dialog = MDDialog(title='Username Check', buttons=[more_button, close_button])
        username = self.login_ids.username.text
        password = self.login_ids.password.text
        if username == "" or password == "":
            self.loading.dismiss()
            self.dialog.text = 'Please enter all fields'
            self.dialog.open()
        else:
            if self.db.isExisting(username):
                if self.db.isUserPass(username, password):
                    self.db.currentUser = username
                    self.db.setStatus(1)
                    self.loading.dismiss()
                    self.screen.current = 'home'
                else:
                    self.loading.dismiss()
                    self.dialog.text = 'Incorrect password'
                    self.dialog.open()
            else:
                self.db.createAcc(username, password)
                self.loading.dismiss()
                self.dialog.text = 'Account has been created. Please login again'
                self.dialog.open()
        # print(self.login_ids.username.text)

    def run_loading(self):
        self.loading.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def comingSoonToast(self, obj):
        toast("Feature Coming Soon")

    def profile(self):
        profile_card = ProfileCard()
        profile = MDDialog()
        profile.add_widget(profile_card)
        profile.open()

    def navigation_draw(self):
        pass

    def logout(self):
        yes_button = MDRaisedButton(text="Logout", on_release=self.logout_prompt)
        no_button = MDFlatButton(text="Cancel", on_release=self.close_dialog)
        self.dialog = MDDialog(
            title="Logout",
            text="Are you sure you want to log out?",
            buttons=[no_button, yes_button]
        )
        self.dialog.open()

    def logout_prompt(self, obj):
        self.login_ids.username.set_text(None, "")
        self.login_ids.password.set_text(None, "")
        self.screen.current = 'login'
        self.dialog.dismiss()
        self.db.setStatus(0)

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Teal"
        # self.theme_cls.theme_style = "Dark"
        return self.screen

    def on_stop(self):
        self.db.setStatus(0)
        self.db.close()


FinalApp().run()
