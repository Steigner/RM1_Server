import subprocess
import csv


class Weather(object):
    @classmethod
    def download_weather(cls):
        subprocess.run("app/weather/weather.sh", shell=True)

    @classmethod
    def get_weather(cls):
        # init
        weather = []
        temperature = None
        humidity = None
        preasure = None

        # open csv file and read datas
        with open("app/weather/weather.csv", "r") as file:
            reader = csv.reader(file, delimiter=" ")
            for row in reader:
                temperature = row[-1]
                humidity = row[-2]
                preasure = row[-3]
                for i in range(len(row) - 3):
                    weather.append(row[i])

        # becouse it is possible to describe weather by 1-4 words
        # split it and get as string
        weather = " ".join(str(e) for e in weather)

        # clear csv file after data is readed
        f = open("app/weather/weather.csv", "w+")
        f.close()

        return weather, temperature, humidity, preasure


# Testing purposes -> weather.csv
# Partly cloudy 1026hPa 76% +8°C
# Sunny 1011hPa 42% +8°C
