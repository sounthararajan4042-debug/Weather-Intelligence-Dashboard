
import customtkinter as ctk
from dashboard.gui import WeatherDashboard


def main():
    root = ctk.CTk()
    app = WeatherDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
