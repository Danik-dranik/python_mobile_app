# -- coding: utf-8 --
# Добавление библиотек
from kivymd.app import MDApp
from farmersmapview import FarmersMapView
import sqlite3
from kivymd.theming import ThemableBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import smtplib
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import geocoder
from kivymd.uix.dialog import MDInputDialog
from urllib import parse
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
import requests
import re

Window.size = (300, 500)

cheking_user_log = 0

user_email_data = []


# Класс экрана меню
class MenuScreen(Screen):
    pass


class ToolScreen(Screen):
    maps = ObjectProperty(None)

    # Функция поиска местоположения
    def findme(self):
        try:
            g = geocoder.ip('me')
            result = g.latlng
            lat = result[0]
            lon = result[1]
            print(lat, lon)
            mapview = self.maps
            mapview.center_on(lat, lon)
        except Exception as err:
            print(err)

    def cheking_user_log_in_system(self):
        if not data:
            dontLogin()
        elif data[-1] == 1:
            self.manager.current = 'addplace'

    def cheking_user_log_in_system_for_callback(self):
        if not data:
            dontLogin()
        elif data[-1] == 1:
            self.manager.current = 'callback'


class SearchPopupMenu(MDInputDialog):
    title = 'Поиск по адресу'
    text_button_ok = 'Поиск'
    maps = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.size_hint = [.9, .3]
        self.events_callback = self.callback

    def open(self):
        super().open()
        Clock.schedule_once(self.set_field_focus, 0.5)

    def callback(self, *args):
        try:
            URL = "https://geocode.search.hereapi.com/v1/geocode"
            address = self.text_field.text
            print(address)
            location = address
            api_key = '2Nmhize-Lxxc_DAePAaYLbhmlkRy7l_Lh7MmcuQnV4s'
            PARAMS = {'apikey': api_key, 'q': location}
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            lat = data['items'][0]['position']['lat']
            lon = data['items'][0]['position']['lng']

            print(lat, lon)
        except Exception as err:
            print(err)


# Класс экрана разработчика
class PrivacyPolicyScreen(Screen):
    pass


data = []


# Класс экрана авторизации
class LoginScreen(Screen):

    # Функция проверки данных
    def loginBtn(self):
        email = ObjectProperty(None)
        password = ObjectProperty(None)
        try:
            sqliteConnection = sqlite3.connect("markets.db")
            cursor = sqliteConnection.cursor()
            user_email = self.email.text
            user_password = self.password.text
            cursor.execute("SELECT * FROM users WHERE mail = ? AND password = ?", (user_email, user_password,))
            cur = cursor.fetchone()
            if cur is None:
                invalidLogin()
            else:
                user_email_data.append(user_email)
                self.reset()
                succeslogin()
                cheking_user_log = 1
                data.append(cheking_user_log)
        except Exception as err:
            print(err)

    def createBtn(self):
        self.reset()
        sm.current = "signin"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


# Класс экрана регистрации
class SigninScreen(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    nnum_list = ObjectProperty(None)
    type_user = ObjectProperty(None)

    # Функция проверки корректности заполненых данных и добавление в бд
    def submit(self, *args):
        sqliteConnection = sqlite3.connect("markets.db")
        cursor = sqliteConnection.cursor()
        user_email = self.email.text
        user_namee = self.namee.text
        user_password = self.password.text
        user_nnum_list = self.nnum_list.text
        user_type_user = self.type_user.text

        regex = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"

        if re.search(regex,
                     user_email) and user_namee != "" and user_password != "" and user_nnum_list != "" and user_type_user != "":
            try:
                print("connection")
                cursor.execute("SELECT * FROM users WHERE mail = ? AND password = ?", (user_email, user_password,))
                cur = cursor.fetchone()
                if cur is None:
                    sql = '''INSERT INTO users (mail, nik, password, num_list, type_user) VALUES (?, ?, ?, ?, ?)'''
                    val = (user_email, user_namee.encode('utf-8'), user_password, user_nnum_list.encode('utf-8'), user_type_user.encode('utf-8'))
                    cursor.execute(sql, val)
                    sqliteConnection.commit()
                    self.reset()
                    succesReg()
                    sm.current = "login"
                else:
                    print("Вы в базе данных")
                    invalidForm()
            except Exception as e:
                print(e)
                invalidForm()
        else:
            print("не правильные данные")
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""
        self.nnum_list.text = ""
        self.type_user.text = ""


# Класс экрана Обратной связи
class CallBackScreen(Screen):
    massagee = ObjectProperty(None)

    # Функция отправки сообщения на Gmail
    def sendEmail(self, *args):
        try:
            sender_email = "vosmoshnostiapp@gmail.com"
            rec_email = "daniklogunov@gmail.com"
            password = "vwsiwEIrhY"
            message = self.massagee.text
            print(message)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            print("login success")
            new_mesage = str(message) + " " + str(user_email_data[0])
            server.sendmail(sender_email, rec_email, new_mesage.encode('utf-8'))
            print("Email was send")
            self.resetEmail()
            successSendassege()
        except Exception as err:
            print(err)

    def resetEmail(self):
        self.massagee.text = ""


class AddPlaceScreen(Screen):
    market_namee = ObjectProperty(None)
    ffimd = ObjectProperty(None)
    address = ObjectProperty(None)
    market_site = ObjectProperty(None)
    market_vk = ObjectProperty(None)
    market_time = ObjectProperty(None)

    def get_market(self, *args):
        sqliteConnection = sqlite3.connect("markets.db")
        cursor = sqliteConnection.cursor()
        market_name = self.market_namee.text
        market_ffimd = self.ffimd.text
        market_addres = self.address.text
        market_vk_data = self.market_vk.text
        market_website = self.market_site.text
        market_time_data = self.market_time.text

        URL = "https://geocode.search.hereapi.com/v1/geocode"
        location = market_addres
        api_key = '2Nmhize-Lxxc_DAePAaYLbhmlkRy7l_Lh7MmcuQnV4s'
        PARAMS = {'apikey': api_key, 'q': location}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        print(data)
        lat = data['items'][0]['position']['lat']
        lon = data['items'][0]['position']['lng']

        try:
            print("connection")
            sql = '''INSERT INTO markets (FMID, MarketName, Website, Facebook, street, x, y) VALUES (?, ?, ?, ?, ?, ?, ?)'''
            val = (market_ffimd, market_name, market_website, market_vk_data, market_addres, lon, lat)
            cursor.execute(sql, val)
            sqliteConnection.commit()
            self.sucsesfull()
            self.reset()
        except Exception as e:
            print(e)
            invalidForm()

    def reset(self):
        self.market_namee.text = ""
        self.ffimd.text = ""
        self.address.text = ""
        self.market_vk.text = ""
        self.market_site.text = ""
        self.market_time.text = ""

    def sucsesfull(self):
        self.pop = Popup(title='Не соответствие данных',
                    content=Label(text='Пожалуйста введите\n правильные данные.'),
                    size_hint=(None, None), size=(225, 225))

        self.pop.open()


# Класс экранов
class WindowManager(ScreenManager):
    sm = ScreenManager()
    sm.add_widget(ToolScreen(name='tollbar'))
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(SigninScreen(name='signin'))
    sm.add_widget(CallBackScreen(name='callback'))
    sm.add_widget(PrivacyPolicyScreen(name='addplace'))
    sm.add_widget(PrivacyPolicyScreen(name='privacyPolicy'))


# Функция успешной отправки сообщения
def successSendassege():
    pop = Popup(title='Успшено',
                content=Label(text='Писмо было отправлено.'),
                size_hint=(None, None), size=(225, 225))
    pop.open()


# Функция неправильного ввода данных
def invalidLogin():
    pop = Popup(title='Вход в аккаунт не выполнен',
                content=Label(text='Не правильный\nемайл или пароль'),
                size_hint=(None, None), size=(225, 225))
    pop.open()


# Функция неправильного заполнения данных
def invalidForm():
    pop = Popup(title='Не соответствие данных',
                content=Label(text='Пожалуйста введите\n правильные данные.'),
                size_hint=(None, None), size=(225, 225))

    pop.open()


# Функция успешной авторизации
def succeslogin():
    pop = Popup(title='Успешный вход',
                content=Label(text='Вы успешно вошли в аккаунт.'),
                size_hint=(None, None), size=(225, 225))

    pop.open()


# Функция успешной регестрации
def succesReg():
    pop = Popup(title='Успешная регистрация',
                content=Label(text='ВЫ успешно зарегистрировались.'),
                size_hint=(None, None), size=(225, 225))

    pop.open()


def dontLogin():
    pop = Popup(title='Ошибка',
                content=Label(text='Вы не зарегистрированны.'),
                size_hint=(None, None), size=(225, 225))

    pop.open()


sm = WindowManager()


# Класс приложения
class MainApp(MDApp):
    connection = None
    cursor = None
    search_menu = None

    class ContentNavigationDrawer(BoxLayout):
        pass

    class DrawerList(ThemableBehavior, MDList):
        pass

    def cheking_log_in(self):
        pop = Popup(title='Не доступный функционал',
                    content=Label(text='Вы не авторизировались.'),
                    size_hint=(None, None), size=(225, 225))

        pop.open()

    def on_start(self):
        self.theme_cls.primary_palette = 'BlueGray'

        # реализация GPS
        # GpsHelper().run()

        # Подключение к бд
        self.connection = sqlite3.connect("markets.db")
        self.cursor = self.connection.cursor()

        # Установка поисковой строки
        self.search_menu = SearchPopupMenu()

        screens = [MenuScreen(name="menu"), LoginScreen(name="login"), SigninScreen(name="signin"),
                   AddPlaceScreen(name="addplace")]
        for screen in screens:
            sm.add_widget(screen)


MainApp().run()
