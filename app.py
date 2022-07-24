import os
from threading import Thread
from tkinter import font, PhotoImage

import customtkinter
import requests
from requests import get

from assets.my_gif import MyGif
from weather_card import WeatherCard


class MyApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ---- App Settings ----
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.title("Weather App")
        icon_image = PhotoImage(file="assets/icon.png")
        self.iconphoto(False, icon_image)
        self.geometry("740x320")
        self.resizable(False, False)
        # ---- App Widgets ----
        # -- User input --
        self.input_location = customtkinter.CTkEntry(self, width=550, placeholder_text='Please enter a location')
        self.input_location.bind('<Return>', self.get_weather)
        self.input_location.place(x=25, y=20)
        self.btn_search = customtkinter.CTkButton(self, text="Search", width=120, command=self.get_weather)
        self.btn_search.place(x=590, y=20)
        # -- Weather Container --
        # Weather card placeholder
        self.placeholder = customtkinter.CTkFrame(self, height=200)
        # self.placeholder = WeatherCard(master=self, weather=weather, height=200)
        self.placeholder.place(relx=0.5, rely=0.58, relwidth=0.93, height=240, anchor='center')
        self.gif_load = MyGif(self.placeholder, 'assets/loading.gif')
        self.gif_load.place(relx=0.5, rely=0.5, anchor='center')
        self.l_placeholder = customtkinter.CTkLabel(self.placeholder, text="Weather not set.",
                                                    text_font=font.Font(size=25),
                                                    wraplength=500)
        self.l_placeholder.place(relx=0.5, rely=0.5, anchor='center')
        # Weather Container
        self.weather_card = None
        # Get user weather if connected to the internet
        if self.check_connection():
            self.l_placeholder.configure(text="Searching for your location...")
            self.input_location.configure(state='disabled')
            self.btn_search.configure(state='disabled')
            t = Thread(target=self.get_local_weather)
            t.start()

    def get_weather(self, e=None, location=None):
        if self.weather_card:
            self.weather_card.destroy()
            self.weather_card = None

        if location:
            t = Thread(target=self.weather_request, args=location)
            t.start()
        else:
            t = Thread(target=self.weather_request)
            t.start()

    def get_local_weather(self):
        # Get user ip
        my_ip = self.get_ip()

        if my_ip:
            # Get user location
            location = self.get_location(my_ip)
            if location:
                # Get the weather for user location
                self.get_weather(location=location)
            else:
                self.on_search_end(error="Weather not set.")
                return
        else:
            self.on_search_end(error="Weather not set.")
            return

    @staticmethod
    def check_connection():
        try:
            get('http://google.com')
            return True
        except:
            return False

    @staticmethod
    def get_ip():
        try:
            response = requests.get('https://api64.ipify.org?format=json').json()
        except:
            return None
        return response["ip"]

    @staticmethod
    def get_location(ip_address):
        try:
            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
            country = {"country": response.get("country_name")}
            return country
        except:
            return None

    def weather_request(self, location=None):
        weather = None
        req_url = None
        error = ""
        API_KEY = os.environ.get('API_Key')
        URL = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}"

        if location is None:
            # Check if user entered location
            if self.input_location.get() != "":
                req_url = URL + "&q=" + self.input_location.get()
            else:
                self.on_search_end(False, error="Please select a location first.")
                return
        else:
            req_url = URL + "&q=" + location

        # disable user input
        self.on_search_start()

        try:
            # Send request
            response = get(req_url)
            # Get weather json
            weather = response.json()
            if "error" in weather:
                error = weather['error']['message']
                self.on_search_end(success=False, error=error)
                return
        except requests.exceptions.ConnectionError as e:
            self.on_search_end(success=False, error="A Connection error occurred.")
            return
        except Exception as e:
            self.on_search_end(success=False, error="An Error has occurred.")
            return

        # Display weather card if request was successful
        if weather:
            self.weather_card = WeatherCard(weather=weather)
            self.weather_card.place(relx=0.5, rely=0.58, relwidth=0.93, height=240, anchor='center')
            self.on_search_end(success=True)

    def on_search_start(self):
        # disable user inputs
        self.input_location.configure(state='disabled')
        self.btn_search.configure(state='disabled')
        self.l_placeholder.place_forget()
        # start loading animation
        self.gif_load.start_animate()

    def on_search_end(self, success=True, error="Request failed, check your internet \nconnection and try again."):
        # remove loading animation
        self.gif_load.stop_animate()
        # Enable user inputs
        self.input_location.configure(state='normal')
        self.btn_search.configure(state='normal')
        if not success:
            self.l_placeholder.configure(text=error)
            self.l_placeholder.place(relx=0.5, rely=0.5, anchor='center')
