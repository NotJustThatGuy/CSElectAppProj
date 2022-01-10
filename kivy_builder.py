kivy_builder = """
ScreenManager:
    LoginScreen:
    HomeScreen:
    
<LoginScreen>:
    name:'login'
    MDTextField:
        id: username
        hint_text: "Enter username"
        write_tab: False
        helper_text: "Old username for login; New username to register"
        helper_text_mode: "on_focus"
        icon_right: "account"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.575}
        size_hint_x: None
        width: 300
    MDTextField:
        id: password
        password: True 
        write_tab: False
        hint_text: "Enter password"
        helper_text: "Make sure your password matches your username"
        helper_text_mode: "on_focus"
        icon_right: "lock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: app.login()
    
<HomeScreen>:
    name:'home'
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        icon: 'account'
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["exit-to-app", lambda x: app.logout()]]
                    MDLabel:
                        text: 'Home Page'
                        haligh: 'center'
                    MDBottomAppBar:
                        MDToolbar:
                            title: 'Welcome'
                            icon: 'account'
                            type: 'bottom'
                            mode: 'end'
                            on_action_button: app.profile()
        MDNavigationDrawer:
            id:nav_drawer

"""