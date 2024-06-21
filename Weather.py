import requests
import tkinter as tk 
from tkinter import messagebox
from PIL import Image , ImageTk
import urllib.parse
import os
import datetime
 
def fetch_weather_data(city):
    
      api_key = os.getenv('OPENWEATHER_API_KEY', '5a5e0c3deb4957df9c7ebf584033ca74') 
      base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
      city_encoded = urllib.parse.quote(city)
      params = { 'q':city ,'appid':api_key , 'units': 'metric'}

      try:
            response = requests.get(base_url , params=params)
            response.raise_for_status() 
            # parse jason response    
            data = response.json()
            print(f"API Response: {data}") 
            if data ['cod'] == 200 :
                 weather = {
                       'description': data['weather'][0]['description'],
                       'temperature': data['main']['temp'],
                       'humidity': data['main']['humidity'],
                       'wind_speed': data['wind']['speed'],
                 }
                 return weather 
            else :
                 return None 
           

      except requests.exceptions.RequestException as e:
          print (f"print error fetching data : {e}")
          return None 
      

def get_weather_and_display(city_entry , output_lable , weather_image_label , images):
       city = city_entry.get()
       weather = fetch_weather_data(city)
       if weather :
             output_lable.config(text = f"Weather in {city}:\n"
                                 f"Description: {weather['description']}\n"
                                 f"Temperature: {weather['temperature']} °C\n"
                                 f"Humidity: {weather['humidity']}%\n"
                                 f"Wind Speed: {weather['wind_speed']} m/s")  

             description = weather['description'].lower()
             if 'cloud' in description:
                   weather_image_label.config(image=images['cloudy'])
             elif 'sun' in description or 'clear' in description:
                    if is_night():
                           weather_image_label.config(image=images.get('clear_night'))
                    else:
                          weather_image_label.config(image=images.get('sunny'))
                          
             elif 'rain' in description:
                   weather_image_label.config(image=images['rainy'])
             elif 'haze' in description:
                   weather_image_label.config(image=images['haze' ])
             elif 'fog' in description:
                   weather_image_label.config(image=images['fog' ])
             
                   
             else:
                   weather_image_label.config(image='')   
       else :
             messagebox.showerror("Error" ,f"could not fetch weather data for {city}")
def set_background_color(window):
      current_hour = datetime.datetime.now().hour
      if 18 <= current_hour <= 6 :
            window.config(bg = 'dark blue')

      else :
            window.config(bg = 'light sky blue')
def is_night():
    current_hour = datetime.datetime.now().hour
    return 18 <= current_hour <= 6



def main():
      window = tk.Tk()
      window.title("My weather app")
      font_large = ( "Arial" , 18)
      set_background_color(window)

      city_label = tk.Label(window, text=" Hello !! Enter city name:" ,font = font_large , bg=window.cget('bg'),
                          fg='white' if is_night() else 'black')
      city_label.pack(pady=12)

      city_entry = tk.Entry(window,width = 32 , font = font_large)
      city_entry.pack(pady = 8) #pack entry wiget 

      fetch_button = tk.Button(window, text="Get Weather",
                                   command=lambda: get_weather_and_display(city_entry, output_label,weather_image_label,images),
                                   font = font_large)
      fetch_button.pack(pady=12) 


      output_label = tk.Label(window, text="" , font = font_large , bg=window.cget('bg') , fg='white' if is_night() else 'black')
      output_label.pack(pady=22)  # Label to display weather information
      try :
            images = {
                'sunny': ImageTk.PhotoImage(Image.open("SUN.JPEG")),
                'cloudy': ImageTk.PhotoImage(Image.open("CLOUDY.JPEG")),
                'rainy': ImageTk.PhotoImage(Image.open("RAINY.JPEG")),
                'haze' : ImageTk.PhotoImage(Image.open("HAZE.JPEG")),
                'fog' : ImageTk.PhotoImage(Image.open("FOG.JPEG")),
                'clear_night': ImageTk.PhotoImage(Image.open("NIGHT_SKY.JPEG")),
            }

      except Exception as e:
            print(f"Error loading images: {e}")
            images = {}


      weather_image_label = tk.Label(window ,  bg=window.cget('bg'))
      weather_image_label.pack(pady=10)

      window.mainloop()

if __name__ == "__main__":
    main()