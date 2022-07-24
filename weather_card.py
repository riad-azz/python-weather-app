from datetime import datetime
from tkinter import PhotoImage, font
from urllib.request import urlopen

import customtkinter
from customtkinter import CTkFrame


class WeatherCard(CTkFrame):
    def __init__(self, weather: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # --- Weather Stats ---
        self.date = datetime.now().strftime("%A %I:%M %p")
        last_updated = datetime.strptime(weather['current']['last_updated'], "%Y-%m-%d %H:%M")
        self.last_updated = last_updated.strftime("%A, %d %b %H:%M %p")
        self.country = weather['location']['country']
        self.region = weather['location']['region']
        self.temp_c = str(weather['current']['temp_c'])[:2] + "°"
        self.temp_f = str(weather['current']['temp_f'])[:2] + "°"
        self.wind_kph = str(weather['current']['wind_kph']) + " kph"
        self.wind_mph = str(weather['current']['wind_mph']) + " mph"
        self.humidity = str(weather['current']['humidity']) + "%"
        self.text = weather['current']['condition']['text']
        # Getting the 128x128 icon
        icon_url = weather['current']['condition']['icon'].split('/')
        icon_url[4] = "128x128"
        self.icon_url = "https:" + "/".join(icon_url)
        self.international = True
        # --- Widgets ---
        # Weather Icon
        self.image = ""
        raw_data = None
        icon_text = ""

        with urlopen(self.icon_url) as url:
            raw_data = url.read()

        if raw_data:
            self.image = PhotoImage(data=raw_data)
        else:
            icon_text = "X"

        self.l_icon = customtkinter.CTkLabel(self, text=icon_text, image=self.image, text_font=font.Font(size=74))
        self.l_icon.place(x=5, y=10, width=110, height=120)
        # Weather Temperature
        self.l_temp = customtkinter.CTkLabel(self, text=self.temp_c, text_font=font.Font(size=74))
        self.l_temp.place(x=128, y=10, width=145)
        # Weather degree choices
        # Celsius
        self.btn_temp_c = customtkinter.CTkButton(self, text="C",
                                                  command=lambda: self.measure_type(international=True),
                                                  text_font=font.Font(size=20), fg_color="#2A2D2E")
        self.btn_temp_c.place(x=280, y=20, width=40, height=40)
        # Separator
        self.temp_seperator = customtkinter.CTkLabel(self, text="|", text_font=font.Font(size=28))
        self.temp_seperator.place(x=328, y=16, width=4)
        # Fahrenheit
        self.btn_temp_f = customtkinter.CTkButton(self, text="F",
                                                  command=lambda: self.measure_type(international=False),
                                                  text_font=font.Font(size=20), fg_color="#2A2D2E")
        self.btn_temp_f.place(x=340, y=20, width=40, height=40)
        # Country name
        self.l_country = customtkinter.CTkLabel(self, text=self.country,
                                                text_font=font.Font(size=14, weight="bold"),
                                                wraplength=298,
                                                anchor='e')
        self.l_country.place(relx=0.99, y=20, anchor='e', width=300)
        # Region name
        self.l_region = customtkinter.CTkLabel(self, text=self.region,
                                               text_font=font.Font(size=13),
                                               wraplength=298,
                                               anchor='e')
        self.l_region.place(relx=0.99, y=50, anchor='e', width=300)
        # Current date
        self.l_date = customtkinter.CTkLabel(self, text=self.date, text_font=font.Font(size=13), anchor='e')
        self.l_date.place(relx=0.99, y=80, anchor='e', width=300)
        # Weather Info text
        self.l_info = customtkinter.CTkLabel(self, text=self.text, text_font=font.Font(size=13), anchor='e')
        self.l_info.place(relx=0.99, y=110, anchor='e', width=300)
        # Humidity
        self.l_humidity = customtkinter.CTkLabel(self, text="Humidity : " + self.humidity, text_font=font.Font(size=16),
                                                 anchor='w')
        self.l_humidity.place(relx=0.01, y=150, anchor='w')
        # Wind speed
        self.l_wind = customtkinter.CTkLabel(self, text="Wind : " + self.wind_kph, text_font=font.Font(size=16),
                                             anchor='w')
        self.l_wind.place(relx=0.01, y=180, anchor='w')
        # Last update
        self.l_last_update = customtkinter.CTkLabel(self, text="Last updated : " + self.last_updated,
                                                    text_font=font.Font(size=16),
                                                    anchor='w')
        self.l_last_update.place(relx=0.01, y=210, anchor='w')

    def measure_type(self, international=True):
        self.international = international
        if self.international:
            self.l_temp.configure(text=self.temp_c)
            self.l_wind.configure(text="Wind : " + self.wind_kph)
        else:
            self.l_temp.configure(text=self.temp_f)
            self.l_wind.configure(text="Wind : " + self.wind_mph)
