from datetime import datetime
import pyperclip
from kivy import Config
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.toast import toast
import tweepy
import pymongo
import logging
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable

Window.softinput_mode = 'below_target'

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s')

Kv = """
#:import Clipboard kivy.core.clipboard.Clipboard

Screen:
    name: "rootScreen"
    BoxLayout:
        orientation:'vertical'

        MDToolbar:
            title: 'P I N A K A'
            md_bg_color: .2, .2, .2, 1
            specific_text_color: 1, 1, 1, 1

        MDBottomNavigation:
            panel_color: .2, .2, .2, 1
            id: manage

            MDBottomNavigationItem:
                name: 'screen1'
                text: 'Home'
                icon: 'home'

                BoxLayout:
                    padding: "50dp", "250dp"
                    spacing: "40dp"
                    orientation: 'vertical'

                    MDTextFieldRound:
                        icon_left: "page-last"
                        id: assisting_member
                        hint_text: "Assisting Member"
                        text_color: app.theme_cls.primary_color
                        allow_copy: True
                        on_triple_tap:
                            self.text = Clipboard.paste()
                            Clipboard.copy('')

                    MDRaisedButton:
                        id: run
                        text: "GET STARTED"
                        increment_width: "164dp"
                        pos_hint: {"center_x": .5, "center_y": .2}
                        on_press:
                            app.get_started(root.ids.assisting_member.text)
                        on_release:
                            root.ids.assisting_member.text = ""

            MDBottomNavigationItem:
                name: 'screen2'
                text: 'Credentials'
                icon: 'key-plus'

                BoxLayout:
                    padding: "50dp"
                    spacing: "40dp"
                    orientation: 'vertical'
                    MDTextField:
                        id: consumer_key
                        hint_text: "Consumer Key"
                        text_color: app.theme_cls.primary_color
                        allow_copy: True
                        on_triple_tap:
                            self.text = Clipboard.paste()
                            Clipboard.copy('')

                    MDTextField:
                        id: consumer_secret
                        hint_text: "Consumer Secret"
                        text_color: app.theme_cls.primary_color
                        allow_copy: True
                        on_triple_tap:
                            self.text = Clipboard.paste()
                            Clipboard.copy('')

                    MDTextField:
                        id: access_key
                        hint_text: "Access Key Token"
                        text_color: app.theme_cls.primary_color
                        allow_copy: True
                        on_triple_tap:
                            self.text = Clipboard.paste()
                            Clipboard.copy('')

                    MDTextField:
                        id: access_secret
                        hint_text: "Access Token Secret"
                        text_color: app.theme_cls.primary_color
                        allow_copy: True
                        on_triple_tap:
                            self.text = Clipboard.paste()
                            Clipboard.copy('')

                    MDRaisedButton:
                        text: "SAVE"
                        elevation: 11
                        increment_width: "180dp"
                        pos_hint: {"center_x": .5, "center_y": .2}
                        on_press:
                            app.read_credentials(root.ids.consumer_key.text,
                            root.ids.consumer_secret.text,
                            root.ids.access_key.text,
                            root.ids.access_secret.text)
                        on_release:
                            root.ids.consumer_key.text = ""
                            root.ids.consumer_secret.text = ""
                            root.ids.access_key.text = ""
                            root.ids.access_secret.text = ""

            MDBottomNavigationItem:
                name: 'screen3'
                text: 'Downloads'
                icon: 'download'
                BoxLayout:

                    orientation: "vertical"
                    padding: "150dp", "150dp"
                    spacing: "50dp"
                    MDTextButton:
                        text: "GROUP 1"
                        on_release:
                            app.data_tables1.open()
                    MDTextButton:
                        text: "GROUP 2"
                        on_release:
                            app.data_tables2.open()
                    MDTextButton:
                        text: "GROUP 3"
                        on_release:
                            app.data_tables3.open()
                    MDTextButton:
                        text: "GROUP 4"
                        on_release:
                            app.data_tables4.open()


            MDBottomNavigationItem:
                name: 'screen4'
                text: 'Help'
                icon: 'information'

                canvas:
                    Rectangle:
                        size: self.size
                        source: app.source
"""


class MyApp(MDApp):

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.title = "PINAKA"
        self.client = pymongo.MongoClient('172.93.48.214', 27017)
        self.source = 'pinaka_lite_help.png'
        self.records = ['pragnik', 'dalipdutta', '_Pritwish']

        self.data_tables1 = MDDataTable(
            size_hint=(0.6, 0.9),
            check=True,
            rows_num=74,
            column_data=[
                ("Sr No", dp(30)),
                ("User Screen Name", dp(30))
            ]
        )

        self.data_tables2 = MDDataTable(
            size_hint=(0.6, 0.9),
            check=True,
            rows_num=74,
            column_data=[
                ("Sr No", dp(30)),
                ("User Screen Name", dp(30))
            ]
        )

        self.data_tables3 = MDDataTable(
            size_hint=(0.6, 0.9),
            check=True,
            rows_num=74,
            column_data=[
                ("Sr No", dp(30)),
                ("User Screen Name", dp(30))
            ]
        )

        self.data_tables4 = MDDataTable(
            size_hint=(0.6, 0.9),
            check=True,
            rows_num=74,
            column_data=[
                ("Sr No", dp(30)),
                ("User Screen Name", dp(30))
            ]
        )

    def get_started(self, assisting_member):

        if assisting_member is "":
            toast("Please Enter Assisting Member ID ...")
        else:
            logging.info("User" + assisting_member)

            Config.read("conf.ini")
            yesterday = Config.get("Login", "timestamp")
            group = Config.get("Group", "id")
            now = datetime.now()

            # Setting group_id
            if not yesterday or not group:
                group_id = 0

            else:
                yesterday = datetime.strptime(yesterday, "%Y-%m-%d %H:%M:%S.%f")
                day = now - yesterday

                if day.days > 0:
                    group_id = int(group) + 1
                else:
                    toast("Please Wait Till Tomorrow ...")

            # Updating conf.ini file
            Config.set("Login", "timestamp", now)
            Config.set("Group", "id", group_id)
            Config.write()

            database = self.client['pinaka']

            collection = database['androidAppData']

            doc = collection.find({'user': assisting_member, 'groupId': group_id})

            self.update_table(doc, group_id, assisting_member)

    def update_table(self, doc, group_id, assisting_member):

        if group_id == 0:

            with open("group1.txt", "w") as file1:

                file1.write(assisting_member + "\n")

                self.records.append(assisting_member)

                for record in doc:
                    file1.write(record['user_screen_name'] + "\n")
                    self.records.append(record['user_screen_name'])

            data_tables = MDDataTable(
                size_hint=(0.4, 0.9),
                rows_num=len(self.records),
                check=True,
                column_data=[
                    ("Sr No", dp(30)),
                    ("User Screen Name", dp(50))
                ],
                row_data=[
                    (f"{i + 1}", self.records[i])
                    for i in range(len(self.records))
                ],
            )

            self.data_tables1 = data_tables
            self.data_tables1.bind(on_check_press=self.on_check_press)

            toast("Group 1 Data Updated ...")

        elif group_id == 1:

            with open("group2.txt", "w") as file1:

                file1.write(assisting_member + "\n")

                self.records.append(assisting_member)

                for record in doc:
                    file1.write(record['user_screen_name'] + "\n")
                    self.records.append(record['user_screen_name'])

            data_tables = MDDataTable(
                size_hint=(0.4, 0.9),
                rows_num=len(self.records),
                check=True,
                column_data=[
                    ("Sr No", dp(30)),
                    ("User Screen Name", dp(50))
                ],
                row_data=[
                    (f"{i + 1}", self.records[i])
                    for i in range(len(self.records))
                ],
            )

            self.data_tables2 = data_tables
            self.data_tables2.bind(on_check_press=self.on_check_press)

            toast("Group 2 Data Updated ...")

        elif group_id == 2:

            with open("group3.txt", "w") as file1:

                file1.write(assisting_member + "\n")

                self.records.append(assisting_member)

                for record in doc:
                    file1.write(record['user_screen_name'] + "\n")
                    self.records.append(record['user_screen_name'])

            data_tables = MDDataTable(
                size_hint=(0.4, 0.9),
                rows_num=len(self.records),
                check=True,
                column_data=[
                    ("Sr No", dp(30)),
                    ("User Screen Name", dp(50))
                ],
                row_data=[
                    (f"{i + 1}", self.records[i])
                    for i in range(len(self.records))
                ],
            )

            self.data_tables3 = data_tables
            self.data_tables3.bind(on_check_press=self.on_check_press)

            toast("Group 3 Data Updated ...")

        elif group_id == 3:

            with open("group4.txt", "w") as file1:

                file1.write(assisting_member + "\n")

                self.records.append(assisting_member)

                for record in doc:
                    file1.write(record['user_screen_name'] + "\n")
                    self.records.append(record['user_screen_name'])

            data_tables = MDDataTable(
                size_hint=(0.4, 0.9),
                rows_num=len(self.records),
                check=True,
                column_data=[
                    ("Sr No", dp(30)),
                    ("User Screen Name", dp(50))
                ],
                row_data=[
                    (f"{i + 1}", self.records[i])
                    for i in range(len(self.records))
                ],
            )

            self.data_tables4 = data_tables
            self.data_tables4.bind(on_check_press=self.on_check_press)

            toast("Group 4 Data Updated ...")

        elif group_id > 3:
            toast("You have reached your Limit ... ")

    def read_credentials(self, consumer_key, consumer_secret, access_key, access_secret):

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        try:
            api.verify_credentials()
            logging.info("Authentication Successful")
            toast("Saving ...")

            database = self.client['pinaka']

            # read "test_db1" collection
            collection = database['credentials']
            data = {
                "consumer_key": consumer_key,
                'consumer_secret': consumer_secret,
                'access_key': access_key,
                'access_secret': access_secret,
            }

            doc = collection.find(data).count()

            if doc == 0:
                data = {
                    "consumer_key": consumer_key,
                    'consumer_secret': consumer_secret,
                    'access_key': access_key,
                    'access_secret': access_secret,
                    'status': 'available'
                }

                collection.insert_one(data)

                toast("Saved ! Thanks for Sharing ... ")
                logging.info("Saved")

            else:
                toast("Credentials Already Exists ...")

        except Exception as e:
            toast("Authentication Failed ...")
            logging.error("Twitter Authentication Failed")

    def build(self):
        return Builder.load_string(Kv)

    def on_start(self):
        Config.read("conf.ini")
        group = Config.get("Group", "id")

        # if group 1 data exists
        if group == str(0):
            records = []
            with open("group1.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables1 = self.update_previous(records)
            self.data_tables1.bind(on_check_press=self.on_check_press)

        # if group 2 data exists
        if group == str(1):
            # Group 1
            records = []
            with open("group1.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables1 = self.update_previous(records)
            self.data_tables1.bind(on_check_press=self.on_check_press)

            # Group2
            records = []

            with open("group2.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables2 = self.update_previous(records)
            self.data_tables2.bind(on_check_press=self.on_check_press)

        if group == str(2):
            records = []

            # Group 1
            with open("group1.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables1 = self.update_previous(records)
            self.data_tables1.bind(on_check_press=self.on_check_press)

            # Group 2
            records = []
            with open("group2.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables2 = self.update_previous(records)
            self.data_tables2.bind(on_check_press=self.on_check_press)

            # Group 3
            records = []
            with open("group3.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables3 = self.update_previous(records)
            self.data_tables3.bind(on_check_press=self.on_check_press)

        if group == str(3):
            records = []

            # Group 1
            with open("group1.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables1 = self.update_previous(records)
            self.data_tables1.bind(on_check_press=self.on_check_press)

            # Group 2
            records = []
            with open("group2.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables2 = self.update_previous(records)
            self.data_tables2.bind(on_check_press=self.on_check_press)

            # Group 3
            records = []
            with open("group3.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            print("list : {0}".format(records))

            print("list len  = {0}".format(len(records)))
            self.data_tables3 = self.update_previous(records)
            self.data_tables3.bind(on_check_press=self.on_check_press)

            # Group 4
            records = []
            with open("group4.txt", "r+") as file1:
                for line in file1:
                    records.append(line.strip())

            self.data_tables4 = self.update_previous(records)
            self.data_tables4.bind(on_check_press=self.on_check_press)

    def update_previous(self, records):
        data_tables = MDDataTable(
            size_hint=(0.4, 0.9),
            rows_num=len(records),
            check=True,
            column_data=[
                ("Sr No", dp(30)),
                ("User Screen Name", dp(50))
            ],
            row_data=[
                (f"{i + 1}", records[i])
                for i in range(len(records))
            ],
        )

        return data_tables

    def on_check_press(self, instance_table, current_row):
        print(current_row[1])
        name = '@' + current_row[1]
        pyperclip.copy(name)
        toast("Copied!")


if __name__ == '__main__':
    MyApp().run()
