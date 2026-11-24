
import customtkinter as ctk
import requests
import threading

from tkinter import messagebox
from app.weather_service import weather_description


API_URL = "http://127.0.0.1:8000"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WeatherDashboard:

    def __init__(self, root):

        self.root = root
        self.root.title("Weather Intelligence Dashboard")
        self.root.geometry("1150x750")
        self.root.minsize(950, 650)
        self.root.configure(fg_color="#0B1220")

        self.current_city = None

        self.create_widgets()
        self.load_history()
        self.load_favorites()

    def create_widgets(self):

        # Main layout
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=220,
            corner_radius=0,
            fg_color="#111B2E"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main = ctk.CTkFrame(
            self.root,
            fg_color="#0B1220",
            corner_radius=0
        )
        self.main.pack(side="left", fill="both", expand=True)

        # Sidebar
        ctk.CTkLabel(
            self.sidebar,
            text="WEATHER\nINTELLIGENCE",
            font=("Arial", 21, "bold"),
            text_color="#60A5FA"
        ).pack(pady=(35, 45))

        ctk.CTkLabel(
            self.sidebar,
            text="MENU",
            text_color="#64748B",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=25, pady=10)

        ctk.CTkButton(
            self.sidebar,
            text="  Dashboard",
            anchor="w",
            fg_color="#1D4ED8",
            hover_color="#2563EB",
            command=self.show_dashboard
        ).pack(fill="x", padx=15, pady=7)

        ctk.CTkButton(
            self.sidebar,
            text="  Search History",
            anchor="w",
            fg_color="transparent",
            hover_color="#26354D",
            command=self.show_history
        ).pack(fill="x", padx=15, pady=7)

        ctk.CTkButton(
            self.sidebar,
            text="  Favorites",
            anchor="w",
            fg_color="transparent",
            hover_color="#26354D",
            command=self.show_favorites
        ).pack(fill="x", padx=15, pady=7)

        ctk.CTkLabel(
            self.sidebar,
            text="PYTHON WEATHER APP\nPowered by Open-Meteo",
            text_color="#64748B",
            font=("Arial", 10),
            justify="left"
        ).pack(side="bottom", pady=25)

        # Dashboard content
        self.content = ctk.CTkScrollableFrame(
            self.main,
            fg_color="transparent"
        )
        self.content.pack(fill="both", expand=True, padx=30, pady=25)

        ctk.CTkLabel(
            self.content,
            text="Weather Dashboard",
            font=("Arial", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.content,
            text="Check current weather conditions around the world.",
            font=("Arial", 13),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(5, 25))

        # Search bar
        search_frame = ctk.CTkFrame(
            self.content,
            fg_color="#17243A",
            corner_radius=12
        )
        search_frame.pack(fill="x", pady=(0, 22))

        self.city_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter city name...",
            height=45,
            font=("Arial", 14),
            fg_color="#0F1A2D",
            border_color="#334155"
        )
        self.city_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=12,
            pady=12
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=110,
            height=45,
            command=self.search_weather
        ).pack(side="left", padx=(0, 12), pady=12)

        # Current weather card
        self.weather_card = ctk.CTkFrame(
            self.content,
            fg_color="#17243A",
            corner_radius=18
        )
        self.weather_card.pack(fill="x", pady=5)

        self.city_label = ctk.CTkLabel(
            self.weather_card,
            text="Search for a city",
            font=("Arial", 23, "bold")
        )
        self.city_label.pack(pady=(25, 5))

        self.temperature_label = ctk.CTkLabel(
            self.weather_card,
            text="--°C",
            font=("Arial", 55, "bold"),
            text_color="#60A5FA"
        )
        self.temperature_label.pack(pady=5)

        self.condition_label = ctk.CTkLabel(
            self.weather_card,
            text="Current weather condition",
            font=("Arial", 16),
            text_color="#CBD5E1"
        )
        self.condition_label.pack(pady=(0, 25))

        ctk.CTkButton(
            self.weather_card,
            text="Add to Favorites",
            command=self.add_favorite
        ).pack(pady=(0, 22))

        # Weather information cards
        ctk.CTkLabel(
            self.content,
            text="Weather Details",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(25, 12))

        details = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        details.pack(fill="x")

        self.humidity_value = self.create_detail_card(
            details, "HUMIDITY", "--%"
        )

        self.wind_value = self.create_detail_card(
            details, "WIND SPEED", "-- km/h"
        )

        self.feels_value = self.create_detail_card(
            details, "FEELS LIKE", "--°C"
        )

        self.status_label = ctk.CTkLabel(
            self.content,
            text="Ready",
            text_color="#94A3B8"
        )
        self.status_label.pack(anchor="w", pady=20)

    def create_detail_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            fg_color="#17243A",
            corner_radius=14
        )
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            text_color="#94A3B8"
        ).pack(pady=(18, 8))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 21, "bold")
        )
        value_label.pack(pady=(0, 20))

        return value_label

    def search_weather(self):

        city = self.city_entry.get().strip()

        if not city:
            messagebox.showwarning(
                "Input Required",
                "Please enter a city name."
            )
            return

        self.status_label.configure(text="Loading weather...")

        threading.Thread(
            target=self.fetch_weather,
            args=(city,),
            daemon=True
        ).start()

    def fetch_weather(self, city):

        try:
            response = requests.get(
                f"{API_URL}/weather",
                params={"city": city},
                timeout=15
            )
            response.raise_for_status()

            data = response.json()

            self.root.after(
                0,
                lambda: self.display_weather(data)
            )

        except requests.RequestException as error:

            error_message = str(error)

            self.root.after(
                0,
                lambda message=error_message: self.show_error(message)
            )

    def display_weather(self, data):

        location = data["location"]
        current = data["weather"]["current"]

        self.current_city = location["name"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]
        feels = current["apparent_temperature"]
        condition = weather_description(current["weather_code"])

        self.city_label.configure(
            text=f'{location["name"]}, {location["country"]}'
        )

        self.temperature_label.configure(
            text=f"{temperature}°C"
        )

        self.condition_label.configure(
            text=condition
        )

        self.humidity_value.configure(
            text=f"{humidity}%"
        )

        self.wind_value.configure(
            text=f"{wind} km/h"
        )

        self.feels_value.configure(
            text=f"{feels}°C"
        )

        self.status_label.configure(
            text="Weather updated successfully"
        )

        self.load_history()

    def show_error(self, error):

        self.status_label.configure(text="Something went wrong")

        messagebox.showerror(
            "Weather Error",
            error
        )

    def add_favorite(self):

        if not self.current_city:
            messagebox.showwarning(
                "No City",
                "Search for a city first."
            )
            return

        try:
            response = requests.post(
                f"{API_URL}/favorites",
                json={"city": self.current_city},
                timeout=10
            )
            response.raise_for_status()

            self.load_favorites()

            messagebox.showinfo(
                "Success",
                "City added to favorites."
            )

        except requests.RequestException as error:
            self.show_error(str(error))

    def load_history(self):

        try:
            response = requests.get(
                f"{API_URL}/history",
                timeout=10
            )
            response.raise_for_status()

            self.history_data = response.json()

        except requests.RequestException:
            self.history_data = []

    def load_favorites(self):

        try:
            response = requests.get(
                f"{API_URL}/favorites",
                timeout=10
            )
            response.raise_for_status()

            self.favorites_data = response.json()

        except requests.RequestException:
            self.favorites_data = []

    def show_dashboard(self):
        self.content.pack(fill="both", expand=True, padx=30, pady=25)

    def show_history(self):

        self.content.pack_forget()

        window = ctk.CTkToplevel(self.root)
        window.title("Search History")
        window.geometry("500x450")
        window.configure(fg_color="#0B1220")

        ctk.CTkLabel(
            window,
            text="Search History",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        for item in self.history_data:
            ctk.CTkLabel(
                window,
                text=f'• {item["city"]}  |  {item["searched_at"]}',
                font=("Arial", 13)
            ).pack(anchor="w", padx=25, pady=5)

        window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_extra_window(window)
        )

    def show_favorites(self):

        self.content.pack_forget()

        window = ctk.CTkToplevel(self.root)
        window.title("Favorite Cities")
        window.geometry("450x400")
        window.configure(fg_color="#0B1220")

        ctk.CTkLabel(
            window,
            text="Favorite Cities",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        for item in self.favorites_data:
            ctk.CTkButton(
                window,
                text=item["city"],
                command=lambda city=item["city"]: self.open_favorite(city)
            ).pack(fill="x", padx=30, pady=6)

        window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_extra_window(window)
        )

    def open_favorite(self, city):

        self.content.pack(fill="both", expand=True, padx=30, pady=25)

        self.city_entry.delete(0, "end")
        self.city_entry.insert(0, city)

        self.search_weather()

    def close_extra_window(self, window):

        window.destroy()
        self.show_dashboard()
