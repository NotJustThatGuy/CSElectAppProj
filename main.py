from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.spinner import MDSpinner

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

class ProfileListItem(TwoLineIconListItem):
    def __init__(self, username, name, **kwargs):
        super().__init__(**kwargs)
        self.text = name
        self.secondary_text = username

    def on_release(self):
        app = MDApp.get_running_app()
        app.db.open()
        userInfo = app.db.getUserInfo(username=self.secondary_text)
        username = userInfo[0]
        full_name = userInfo[3] + ", " + userInfo[1] + " " + userInfo[2]
        bio = userInfo[4]
        pc = ProfileCard(username, full_name, bio)
        app.dialog = MDDialog(
            type="custom",
            content_cls=pc,
            md_bg_color=app.theme_cls.primary_color,
        )
        app.db.close()
        app.dialog.open()

class ProfileCard(MDCard):
    def __init__(self, username, name, bio, **kwargs):
        super().__init__(**kwargs)
        self.ids.profile_basic.text = username
        self.ids.profile_basic_2.text = name
        self.ids.bio_p.text = bio

class EditProfileCard(BoxLayout):
    def __init__(self, fname, mname, lname, bio, **kwargs):
        super().__init__(**kwargs)
        if fname == "Undefined":
            self.ids.fname.text = ""
        else:
            self.ids.fname.text = fname
        if mname == "Undefined":
            self.ids.mname.text = ""
        else:
            self.ids.mname.text = mname
        if lname == "Undefined":
            self.ids.lname.text = ""
        else:
            self.ids.lname.text = lname
        if bio == "Undefined":
            self.ids.bio.text = ""
        else:
            self.ids.bio.text = bio

    def submit_prompt(self, obj):
        app = MDApp.get_running_app()
        app.edit_dialog.dismiss()
        app.db.open()
        if self.ids.fname.text == "":
            self.ids.fname.text = "Undefined"
        if self.ids.mname.text == "":
            self.ids.mname.text = "Undefined"
        if self.ids.lname.text == "":
            self.ids.lname.text = "Undefined"
        if self.ids.bio.text == "":
            self.ids.bio.text = "Undefined"
        app.db.setUserInfo(self.ids.fname.text, self.ids.mname.text, self.ids.lname.text, self.ids.bio.text)
        app.full_name = self.ids.lname.text + ", " + self.ids.fname.text + " " + self.ids.mname.text
        app.fname = self.ids.fname.text
        app.mname = self.ids.mname.text
        app.lname = self.ids.lname.text
        app.bio = self.ids.bio.text
        close_button = MDRaisedButton(text="Close", on_release=app.close_dialog)
        app.dialog = MDDialog(
            text="Info Updated", buttons=[close_button]
        )
        app.dialog.open()
        app.db.close()


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(HomeScreen(name='home'))


class FinalApp(MDApp):
    data = {
        'Edit Profile': 'account-edit',
        'View Profile': 'account',
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog()
        self.edit_dialog = MDDialog()
        self.loading = MDDialog(text="Loading")
        self.screen = Builder.load_file("main.kv")
        self.login_ids = self.screen.get_screen('login').ids
        self.home_ids = self.screen.get_screen('home').ids
        self.db = Database(dbUsername, dbPassword, dbHostname, dbDatabase)
        self.full_name = ""
        self.fname = ""
        self.mname = ""
        self.lname = ""
        self.bio = ""

    def login(self):
        self.run_loading()
        Clock.schedule_once(self.login_process)

    def login_process(self, *args):
        self.db.open()
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
                    userInfo = self.db.getUserInfo()
                    self.full_name = userInfo[3] + ", " + userInfo[1] + " " + userInfo[2]
                    self.fname = userInfo[1]
                    self.mname = userInfo[2]
                    self.lname = userInfo[3]
                    self.bio = userInfo[4]
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
        self.db.close()
        # print(self.login_ids.username.text)

    def run_loading(self):
        self.loading.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def close_edit_dialog(self, obj):
        self.edit_dialog.dismiss()

    def comingSoonToast(self, obj):
        toast("Feature Coming Soon")

    def profile_callback(self, instance):
        epc = EditProfileCard(self.fname, self.mname, self.lname, self.bio)
        pc = ProfileCard(self.db.currentUser, self.full_name, self.bio)
        yes_button = MDRaisedButton(text="Update", on_release=epc.submit_prompt)
        no_button = MDFlatButton(text="Cancel", on_release=self.close_edit_dialog)
        if instance.icon == "account":
            self.dialog = MDDialog(
                type="custom",
                content_cls=pc,
                md_bg_color=self.theme_cls.primary_color,
            )
            self.dialog.open()
        else:
            self.edit_dialog = MDDialog(
                title="Edit Profile:",
                type="custom",
                content_cls=epc,
                buttons=[no_button, yes_button],
            )
            self.edit_dialog.open()

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
        self.clearData()

    def updateList(self):
        self.db.open()
        user_basic = self.db.getUsersBasic()
        self.db.close()
        for x in user_basic:
            self.home_ids.profile_list.add_widget(ProfileListItem(x[0], x[3] + ", " + x[1] + " " + x[2]))

    def refresh_callback(self, *args):
        def refresh_callback(interval):
            self.home_ids.profile_list.clear_widgets()
            self.updateList()
            self.home_ids.refresh_layout.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Teal"
        # self.theme_cls.theme_style = "Dark"
        return self.screen

    def clearData(self):
        self.db.open()
        self.db.setStatus(0)
        self.db.currentUser = ""
        self.db.close()
        self.full_name = ""
        self.fname = ""
        self.mname = ""
        self.lname = ""
        self.bio = ""
        self.home_ids.profile_list.clear_widgets()

    def on_stop(self):
        self.clearData()


FinalApp().run()
