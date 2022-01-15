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
        helper_text_mode: "on_focus"
        icon_right: "account"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.575}
        size_hint_x: None
        width: 400
    MDTextField:
        id: password
        password: True 
        write_tab: False
        hint_text: "Enter password"
        helper_text_mode: "on_focus"
        icon_right: "lock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 400
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
                    ScrollView:
                        MDList:
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
                            OneLineListItem:
                                text: "Single-line item"
        MDNavigationDrawer:
            id:nav_drawer
    
    MDFloatingActionButton:
        pos_hint: {'center_x': 0.9, 'center_y': 0.075}
        icon: 'account'
        md_bg_color: app.theme_cls.primary_color
        on_release: app.profile()
    
<ProfileCard>:
    MDCard:
        orientation: 'horizontal'
        size_hint: None, None
        size:  root.size[0], 175 * (Window.size[1]/960) + 40
        elevation: 1
        padding: 10,0,0,20
        md_bg_color: app.theme_cls.primary_color
        MDCard:
            id: profile_avatar
            canvas:
                Ellipse:
                    group: 'a'
                    pos: self.pos
                    size: self.size
            size_hint: None, None
            size: 175 * (Window.size[0]/540), 175 * (Window.size[1]/960)
            elevation:0
            md_bg_color: app.theme_cls.primary_light
            border_radius: 100
            radius: [100]
        MDCard:
            md_bg_color: app.theme_cls.primary_color
            elevation: 0
            orientation: "vertical"
            padding: "20dp"
            radius: [20]
            MDLabel:
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                halign: "left"
                id: profile_basic
                text: "Hello"
                font_style: "H5"
                size_hint_y: None
                height: self.texture_size[1]
            MDSeparator:
                height: "1dp"
            MDLabel:
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                halign: "left"
                id: profile_basic_2
                text: "Full Name"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                halign: "left"
                text: "\\n"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                spacing: 30,0
                theme_text_color: "Custom"
                text_color: 1,1,1,1
                halign: "left"
                id: bio_p
                text: "Full Name"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]

"""