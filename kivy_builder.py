kivy_builder = """
ScreenManager:
    LoginScreen:
    HomeScreen:
    
<LoginScreen>:
    name:'login'
    MDTextField:
        id: username
        hint_text: "Enter username"
        helper_text: "Your username or new username"
        helper_text_mode: "on_focus"
        icon_right: "account"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.575}
        size_hint_x: None
        width: 300
    MDTextField:
        id: password
        password: True 
        hint_text: "Enter password"
        helper_text: "Your password or new password"
        helper_text_mode: "on_focus"
        icon_right: "lock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.show_data()
    
<HomeScreen>:
    name:'home'
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDBottomAppBar:
                        MDToolbar:
                            icon: 'account'
                            type: 'bottom'
                            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                            right_action_items: [["exit-to-app", lambda x: app.logout()]]
                            on_action_button: app.profile()
                    MDLabel:
                        text: 'Home Page'
                        haligh: 'center'
        MDNavigationDrawer:
            id:nav_drawer

"""