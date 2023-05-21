import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
import datetime
import time
import pyzbar.pyzbar as pyzbar
import cv2
import re
import webbrowser
import subprocess
import os
import webview
import pyautogui

# Initialize the Tkinter window
root = tk.Tk()
root.geometry('700x1000+300+100') # Set the size of the window
root.title('Smart Mirror GUI')
root.configure(bg='black') # Set the background color to black
root.attributes('-fullscreen', True)

# Create a function to update the time and date labels
def update_time_date():
    global time_label
    global date_label
    now = datetime.datetime.now()
    

    time_label.config(text=now.strftime('%I:%M %p'))
    date_label.config(text=now.strftime('%A %B %d %Y'))
    def time_date_update():
        time_label.config(text=now.strftime('%I:%M %p'))
        date_label.config(text=now.strftime('%A %B %d %Y'))
    root.after(1000, time_date_update) # Schedule the next update after 1 second

# Create a function to update the weather information
def update_weather_info():
    #import requests library
    import requests
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe 
    global weather_icon_label
    global weather_temp_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    
    #fetching weather API data
    city = "Birmingham"

    url = ('http://api.openweathermap.org/data/2.5/weather?'
            'q={}&appid=5f9cb6420a1d292494abb582c1f4a4c5&'
            'units=metric'.format(city))

    #converting API data to printable data
    res = requests.get(url)
    data = res.json()

    #seperating relevant data
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind = data['wind']['speed']
    description = data['weather'][0]['description']
    temp = data['main']['temp']

    # Load the weather icon image using PIL
    icon_image = Image.open(f'weather-icon.png')
    icon_image = icon_image.resize((50, 50))
    icon_photo = ImageTk.PhotoImage(icon_image)
    weather_icon_label.config(image=icon_photo)
    weather_icon_label.image = icon_photo

    #adding text to relevant labels
    weather_temp_label.config(text=f'Temperature: {temp}°C')
    weather_hum_label.config(text=f'Humidity: {humidity} %')
    weather_press_label.config(text=f'Pressure: {pressure} psi')
    weather_wind_label.config(text=f'Wind speed: {wind} km/h')
    weather_desc_label.config(text=f'{description}')
    root.after(60000, update_weather_info) # Schedule the next update after 1 minute

def update_news_info():
    import requests
    import json

    global news_txt_label
    
        # Set the API endpoint and query parameters
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'category=general&'
        'apiKey=765697550012483f9dd679fd61c21d22')

    # Make the HTTP request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)
    latest_headline = data['articles'][0]['title']
    news_txt_label.config(text=f'{latest_headline}')
    root.after(3600000, update_news_info)

def update_multi_news_info():
    import requests
    import json

    global news_txt_label
    
        # Set the API endpoint and query parameters
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'category=general&'
        'apiKey=765697550012483f9dd679fd61c21d22')

    # Make the HTTP request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)
    headlines = []
    
    for article in data["articles"][:5]:   
        headlines.append(article['title'])
    headlines_str = "\n".join(headlines)
    news_txt_label.config(text=f'{headlines_str}')

def update_enter_news_info():
    import requests
    import json

    global news_txt_label
    
        # Set the API endpoint and query parameters
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'category=entertainment&'
        'apiKey=765697550012483f9dd679fd61c21d22')

    # Make the HTTP request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)
    headlines = []
    
    for article in data["articles"][:5]:   
        headlines.append(article['title'])
    headlines_str = "\n".join(headlines)
    news_txt_label.config(text=f'{headlines_str}')

def update_busi_news_info():
    import requests
    import json

    global news_txt_label
    
        # Set the API endpoint and query parameters
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'category=business&'
        'apiKey=765697550012483f9dd679fd61c21d22')

    # Make the HTTP request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)
    headlines = []
    
    for article in data["articles"][:5]:   
        headlines.append(article['title'])
    headlines_str = "\n".join(headlines)
    news_txt_label.config(text=f'{headlines_str}')

def update_sports_news_info():
    import requests
    import json

    global news_txt_label
    
        # Set the API endpoint and query parameters
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'category=sports&'
        'apiKey=765697550012483f9dd679fd61c21d22')

    # Make the HTTP request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)
    headlines = []
    
    for article in data["articles"][:5]:   
        headlines.append(article['title'])
    headlines_str = "\n".join(headlines)
    news_txt_label.config(text=f'{headlines_str}')

def update_health_news_info():
    import requests
    import json

    global news_txt_label
    
        # Set the API endpoint and query parameters
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'category=health&'
        'apiKey=765697550012483f9dd679fd61c21d22')

    # Make the HTTP request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)
    headlines = []
    
    for article in data["articles"][:5]:   
        headlines.append(article['title'])
    headlines_str = "\n".join(headlines)
    news_txt_label.config(text=f'{headlines_str}')

def update_science_news_info():
    import requests
    import json

    global news_txt_label
    
        # Set the API endpoint and query parameters
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'category=science&'
        'apiKey=765697550012483f9dd679fd61c21d22')

    # Make the HTTP request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)
    headlines = []
    
    for article in data["articles"][:5]:   
        headlines.append(article['title'])
    headlines_str = "\n".join(headlines)
    news_txt_label.config(text=f'{headlines_str}')  

def update_tech_news_info():
    import requests
    import json

    global news_txt_label
    
        # Set the API endpoint and query parameters
    url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'category=technology&'
        'apiKey=765697550012483f9dd679fd61c21d22')

    # Make the HTTP request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = json.loads(response.text)
    headlines = []
    
    for article in data["articles"][:5]:   
        headlines.append(article['title'])
    headlines_str = "\n".join(headlines)
    news_txt_label.config(text=f'{headlines_str}')
#creates function to display weather info in depth
##Image recognition function
def Scan():
    def splitter(splitee):
        #splits at all instances of \n
        y = re.search("b'(.+?)'",splitee).group(1)
        print(y)
        return (y)
    
    def recog():
     
        def decode(im) :
          # should find barcodes and QR codes
          decodedObjects = (pyzbar.decode(im))
          print(decodedObjects) #test line to see what passed
          # Print results
          if not decodedObjects:
              print("The code was not detected or the code is blank/corrupted")
              return decodedObjects, "F"
          else:
              for obj in decodedObjects:
                print('Type : ', obj.type)
                print('Data : ', obj.data,'\n')
             
              return decodedObjects,obj.data
         
         
        # Main
        if __name__ == '__main__':

          height= (root.winfo_height())/1.5
          width = (root.winfo_width())/2
          print(height)
          print(width)
          dim = (int(width),int(height))
          cam = cv2.VideoCapture(0)
          cv2.namedWindow("Camera", cv2.WND_PROP_AUTOSIZE)
          cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
          cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
          passed= ""
          img_counter = 0

        while True:
              ret, frame = cam.read()
              if not ret:
                  print("failed to grab frame")
                  break
              frame = cv2.resize(frame,dim,interpolation=cv2.INTER_AREA)
              y=root.geometry().split('+')
              print(y)
              
              cv2.moveWindow("Camera",int(y[1])+int(width/2),int(y[2])+int(height/3.5))
              cv2.imshow("Camera", frame)

              k = cv2.waitKey(1)
              if k%256 == 27:
                  # ESC pressed
                  print("Escape hit, closing...")
                  break
              elif k%256 == 32:
                  # SPACE pressed
                  img_name = "opencv_frame_{}.png".format(img_counter)
                  cv2.imwrite(img_name, frame)
                  print("{} written!".format(img_name))
                  # reads image and identifies the QR code meaning
                  im = cv2.imread('opencv_frame_{}.png'.format(img_counter),0)
                  decodedObjects,NTool = decode(im)
                  passed = passed + str(NTool) +"\n"
                  img_counter += 1
                  cv2.destroyAllWindows()
                  break
                  

        cam.release()
        cv2.destroyAllWindows()
        return(passed)
    #################Main script########################

    #calls for QR scan, try for barcode too
    while True:
        #These are long #subprocess.run(["powershell", "-command", "&{$p='HKCU:SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3';$v=(Get-ItemProperty -Path $p).Settings;$v[8]=3;&Set-ItemProperty -Path $p -Name Settings -Value $v;&Stop-Process -f -ProcessName explorer}"])
        Tstock = recog()
        # Stops mirror display
        if Tstock == "F\n":
            print("Please go to https://www.youtube.com/watch?v=dQw4w9WgXcQ for a video on support")
            break
        elif Tstock == "":
            print("Thank you for using the smart mirror")
           # subprocess.run(["powershell", "-command","&{$p='HKCU:SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3';$v=(Get-ItemProperty -Path $p).Settings;$v[8]=2;&Set-ItemProperty -Path $p -Name Settings -Value $v;&Stop-Process -f -ProcessName explorer}"])
            break
        else:
             height= (root.winfo_height())/1.5
             width = (root.winfo_width())/2
             print(height)
             print(width)
             reMat = splitter(Tstock)
             if reMat[:4]=="http":
                 #opens webpage, can add functionality on top of this
                 #lol= tk.Tk()
                 #lol.geometry('400x500')
                 #webview.create_window('Web', reMat)
                 #webview.start(gui='mshtml')

                 webbrowser.open_new(reMat)
             else:
                 #webview.create_window('Web',"https://www.google.co.uk/search?q="+reMat)
                 webbrowser.open("https://www.google.co.uk/search?q="+reMat)
             break


def weather_function():
    #get current time and date
    now = datetime.datetime.now()
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button
    global Scan_button
    
    enter_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Entertainment News", command = enter_news_function)
    enter_news_button.place(relx = 0.61, rely = 0.15, anchor = 'sw')

    busi_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Business News", command = busi_news_function)
    busi_news_button.place(relx = 0.69, rely = 0.15, anchor = 'sw')

    sport_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Sports News", command = sports_news_function)
    sport_news_button.place(relx = 0.75, rely = 0.15, anchor = 'sw')

    health_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Health News", command = health_news_function)
    health_news_button.place(relx = 0.865, rely = 0.15, anchor = 'sw')

    science_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Science News", command = science_news_function)
    science_news_button.place(relx = 0.805, rely = 0.15, anchor = 'sw')

    tech_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Tech News", command = tech_news_function)
    tech_news_button.place(relx = 0.95, rely = 0.15, anchor = 'sw')

    #remove labels to allow them to be removed/moved
    weather_button.destroy()
    news_button.destroy()
    time_label.destroy()
    date_label.destroy()
    weather_icon_label.destroy()
    weather_temp_label.destroy()
    busi_news_button.destroy()
    enter_news_button.destroy()
    sport_news_button.destroy()
    health_news_button.destroy()
    science_news_button.destroy()
    tech_news_button.destroy()
    Scan_button.destroy()
    
    #new label creation and placement
    weather_temp_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    weather_temp_label.place(relx = 0.0, rely = 0.3, anchor ='sw')
    
    weather_icon_label = tk.Label(root, bg='black')
    weather_icon_label.place(relx = 0.04, rely = 0.25, anchor = 'sw')

    weather_hum_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    weather_hum_label.place(relx = 0.0, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    weather_press_label.place(relx = 0.0, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    weather_wind_label.place(relx = 0.0, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri',14), bg='black', fg='white')
    weather_desc_label.place(relx = 0.0, rely = 0.5, anchor ='sw')

    time_label = tk.Label(root, font=('calibri', 16), bg='black', fg='white')
    time_label.place(relx = 0.05, rely = 0.05, anchor = 'sw')
    time_label.config(text=now.strftime('%I:%M %p'))

    date_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=160)
    date_label.place(relx = 0.85, rely = 0.075, anchor = 'sw')
    date_label.config(text=now.strftime('%A %B %d %Y'))

    #create button to go back to homescreen
    Home =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Home", command = Homescreen2)
    Home.place(relx = 0.5, rely = 0.9, anchor = 'center')

    


    update_weather_info()
    update_time_date()
    update_news_info()


# initial homescreen to remove start button (only used for first instance of homescreen on start)
def Homescreen1():
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_icon_label
    global weather_temp_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global Scan_button
    #new label creation and placement
    weather_temp_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    weather_temp_label.place(relx = 0.0, rely = 0.95, anchor ='sw')
    
    weather_icon_label = tk.Label(root, bg='black')
    weather_icon_label.place(relx = 0.04, rely = 0.9, anchor = 'sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.0, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.0, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.0, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.0, rely = 0.5, anchor ='sw')

    time_label = tk.Label(root, font=('calibri', 40), bg='black', fg='white')
    time_label.pack(side='top', pady=10)

   
    date_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    date_label.pack(side='top')

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.8, anchor ='sw')
    news_label.config(text="Top Headline:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.95, anchor ='sw')

    welcome_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    welcome_label.place(relx = 0.5, rely = 0.5 , anchor ="center")
    welcome_label.config(text="Welcome to your new Smart Mirror")
    
    root.after(5000, welcome_label.destroy)
    
    update_time_date()
    update_weather_info()
    update_news_info()

    #remove unwanted labels from screen
    weather_hum_label.destroy()
    weather_press_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()
    Start.destroy()
   
    #create button to go to weather page
    weather_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Weather", command = weather_function)
    weather_button.place(relx = 0.0, rely = 0.15, anchor = 'sw')

    news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "News", command = news_function)
    news_button.place(relx = 0.92, rely = 0.15, anchor = 'sw')

    Scan_button =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Camera", command = Scan)
    Scan_button.place( relx=0.5, rely = 0.9,anchor = 'center')

#same as homescreen1 but does not need to have Start.destroy anymore (used for all instances excluding first)
def Homescreen2():
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button
    global Scan_button


    #remove labels so they can moved
    time_label.destroy()
    date_label.destroy()
    weather_temp_label.destroy()
    weather_icon_label.destroy()
    weather_hum_label.destroy()
    weather_press_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()
    news_label.destroy()
    news_txt_label.destroy()
    Home.destroy()
    Start.destroy()
    busi_news_button.destroy()
    enter_news_button.destroy()
    sport_news_button.destroy()
    health_news_button.destroy()
    science_news_button.destroy()
    tech_news_button.destroy()

    #create new labels

    weather_icon_label = tk.Label(root, bg='black')
    weather_icon_label.place(relx = 0.04, rely = 0.9, anchor = 'sw')

    weather_temp_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    weather_temp_label.place(relx = 0.0, rely = 0.95, anchor ='sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.05, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.05, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.05, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.05, rely = 0.5, anchor ='sw')

    time_label = tk.Label(root, font=('calibri', 40), bg='black', fg='white')
    time_label.pack(side='top', pady=10)

    date_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    date_label.pack(side='top')

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.8, anchor ='sw')
    news_label.config(text="Top Headline:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.95, anchor ='sw')


    update_time_date()
    update_weather_info()
    update_news_info()
    #remove unecessary labels
    weather_hum_label.destroy()
    weather_press_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()

    #create button for relevant pages
    weather_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Weather", command = weather_function)
    weather_button.place(relx = 0.0, rely = 0.15, anchor = 'sw')

    news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "News", command = news_function)
    news_button.place(relx = 0.92, rely = 0.15, anchor = 'sw')

    Scan_button =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Camera", command = Scan)
    Scan_button.place( relx=0.5, rely = 0.9,anchor = 'center')

def enter_news_function():
    #get current time and date
    now = datetime.datetime.now()
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button
    
    #remove labels to allow them to be removed/moved
    weather_button.destroy()
    news_button.destroy()
    time_label.destroy()
    date_label.destroy()
    news_txt_label.destroy()
    news_label.destroy()
 
    
    #new label creation and placement


    time_label = tk.Label(root, font=('calibri', 16), bg='black', fg='white')
    time_label.place(relx = 0.05, rely = 0.05, anchor = 'sw')
    time_label.config(text=now.strftime('%I:%M %p'))

    date_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=160)
    date_label.place(relx = 0.85, rely = 0.075, anchor = 'sw')
    date_label.config(text=now.strftime('%A %B %d %Y'))

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.2, anchor ='sw')
    news_label.config(text="Top Headlines:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.9, anchor ='sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.05, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.05, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.05, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.05, rely = 0.5, anchor ='sw')
    

    #create button to go back to homescreen
    Home =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Home", command = Homescreen2)
    Home.place(relx = 0.5, rely = 0.9, anchor = 'center')

    update_weather_info()
    update_time_date()
    update_enter_news_info()

    weather_press_label.destroy()
    weather_hum_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()

def busi_news_function():
    #get current time and date
    now = datetime.datetime.now()
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button

    #remove labels to allow them to be removed/moved
    weather_button.destroy()
    news_button.destroy()
    time_label.destroy()
    date_label.destroy()
    news_txt_label.destroy()
    news_label.destroy()
 
    
    #new label creation and placement


    time_label = tk.Label(root, font=('calibri', 16), bg='black', fg='white')
    time_label.place(relx = 0.05, rely = 0.05, anchor = 'sw')
    time_label.config(text=now.strftime('%I:%M %p'))

    date_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=160)
    date_label.place(relx = 0.85, rely = 0.075, anchor = 'sw')
    date_label.config(text=now.strftime('%A %B %d %Y'))

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.2, anchor ='sw')
    news_label.config(text="Top Headlines:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.9, anchor ='sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.05, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.05, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.05, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.05, rely = 0.5, anchor ='sw')
    

    #create button to go back to homescreen
    Home =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Home", command = Homescreen2)
    Home.place(relx = 0.5, rely = 0.9, anchor = 'center')

    update_weather_info()
    update_time_date()
    update_busi_news_info()

    weather_press_label.destroy()
    weather_hum_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()

def sports_news_function():
    #get current time and date
    now = datetime.datetime.now()
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button
    
    #remove labels to allow them to be removed/moved
    weather_button.destroy()
    news_button.destroy()
    time_label.destroy()
    date_label.destroy()
    news_txt_label.destroy()
    news_label.destroy()
 
    
    #new label creation and placement


    time_label = tk.Label(root, font=('calibri', 16), bg='black', fg='white')
    time_label.place(relx = 0.05, rely = 0.05, anchor = 'sw')
    time_label.config(text=now.strftime('%I:%M %p'))

    date_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=160)
    date_label.place(relx = 0.85, rely = 0.075, anchor = 'sw')
    date_label.config(text=now.strftime('%A %B %d %Y'))

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.2, anchor ='sw')
    news_label.config(text="Top Headlines:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.9, anchor ='sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.05, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.05, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.05, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.05, rely = 0.5, anchor ='sw')
    

    #create button to go back to homescreen
    Home =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Home", command = Homescreen2)
    Home.place(relx = 0.5, rely = 0.9, anchor = 'center')

    update_weather_info()
    update_time_date()
    update_sports_news_info()

    weather_press_label.destroy()
    weather_hum_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()

def health_news_function():
    #get current time and date
    now = datetime.datetime.now()
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button
    
    #remove labels to allow them to be removed/moved
    weather_button.destroy()
    news_button.destroy()
    time_label.destroy()
    date_label.destroy()
    news_txt_label.destroy()
    news_label.destroy()
 
    
    #new label creation and placement


    time_label = tk.Label(root, font=('calibri', 16), bg='black', fg='white')
    time_label.place(relx = 0.05, rely = 0.05, anchor = 'sw')
    time_label.config(text=now.strftime('%I:%M %p'))

    date_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=160)
    date_label.place(relx = 0.85, rely = 0.075, anchor = 'sw')
    date_label.config(text=now.strftime('%A %B %d %Y'))

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.2, anchor ='sw')
    news_label.config(text="Top Headlines:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.9, anchor ='sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.05, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.05, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.05, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.05, rely = 0.5, anchor ='sw')
    

    #create button to go back to homescreen
    Home =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Home", command = Homescreen2)
    Home.place(relx = 0.5, rely = 0.9, anchor = 'center')

    update_weather_info()
    update_time_date()
    update_health_news_info()

    weather_press_label.destroy()
    weather_hum_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()

def science_news_function():
    #get current time and date
    now = datetime.datetime.now()
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button
    
    #remove labels to allow them to be removed/moved
    weather_button.destroy()
    news_button.destroy()
    time_label.destroy()
    date_label.destroy()
    news_txt_label.destroy()
    news_label.destroy()
 
    
    #new label creation and placement


    time_label = tk.Label(root, font=('calibri', 16), bg='black', fg='white')
    time_label.place(relx = 0.05, rely = 0.05, anchor = 'sw')
    time_label.config(text=now.strftime('%I:%M %p'))

    date_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=160)
    date_label.place(relx = 0.85, rely = 0.075, anchor = 'sw')
    date_label.config(text=now.strftime('%A %B %d %Y'))

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.2, anchor ='sw')
    news_label.config(text="Top Headlines:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.9, anchor ='sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.05, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.05, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.05, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.05, rely = 0.5, anchor ='sw')
    

    #create button to go back to homescreen
    Home =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Home", command = Homescreen2)
    Home.place(relx = 0.5, rely = 0.9, anchor = 'center')

    update_weather_info()
    update_time_date()
    update_science_news_info()

    weather_press_label.destroy()
    weather_hum_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()

def tech_news_function():
    #get current time and date
    now = datetime.datetime.now()
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button
    
    #remove labels to allow them to be removed/moved
    weather_button.destroy()
    news_button.destroy()
    time_label.destroy()
    date_label.destroy()
    news_txt_label.destroy()
    news_label.destroy()
 
    
    #new label creation and placement


    time_label = tk.Label(root, font=('calibri', 16), bg='black', fg='white')
    time_label.place(relx = 0.05, rely = 0.05, anchor = 'sw')
    time_label.config(text=now.strftime('%I:%M %p'))

    date_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=160)
    date_label.place(relx = 0.85, rely = 0.075, anchor = 'sw')
    date_label.config(text=now.strftime('%A %B %d %Y'))

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.2, anchor ='sw')
    news_label.config(text="Top Headlines:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.9, anchor ='sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.05, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.05, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.05, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.05, rely = 0.5, anchor ='sw')
    

    #create button to go back to homescreen
    Home =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Home", command = Homescreen2)
    Home.place(relx = 0.5, rely = 0.9, anchor = 'center')

    update_weather_info()
    update_time_date()
    update_tech_news_info()

    weather_press_label.destroy()
    weather_hum_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()

def news_function():
    #get current time and date
    now = datetime.datetime.now()
    #imports global variables used in all other functions
    # all variables present to allow for screen wipe
    global weather_button
    global Home
    global time_label
    global date_label
    global weather_temp_label
    global weather_icon_label
    global weather_hum_label
    global weather_press_label
    global weather_wind_label
    global weather_desc_label
    global news_button
    global news_label
    global news_txt_label
    global busi_news_button
    global enter_news_button
    global sport_news_button
    global health_news_button
    global science_news_button
    global tech_news_button
    global Scan_button
    
    #remove labels to allow them to be removed/moved
    weather_button.destroy()
    time_label.destroy()
    date_label.destroy()
    news_txt_label.destroy()
    news_label.destroy()
    Scan_button.destroy()
    
    #new label creation and placement


    time_label = tk.Label(root, font=('calibri', 16), bg='black', fg='white')
    time_label.place(relx = 0.05, rely = 0.05, anchor = 'sw')
    time_label.config(text=now.strftime('%I:%M %p'))

    date_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=160)
    date_label.place(relx = 0.85, rely = 0.075, anchor = 'sw')
    date_label.config(text=now.strftime('%A %B %d %Y'))

    news_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white')
    news_label.place(relx = 0.875, rely = 0.2, anchor ='sw')
    news_label.config(text="Top Headlines:")

    news_txt_label = tk.Label(root, font=('calibri', 14), bg='black', fg='white', wraplength=200)
    news_txt_label.place(relx = 0.85, rely = 0.9, anchor ='sw')

    weather_hum_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_hum_label.place(relx = 0.05, rely = 0.35, anchor ='sw')

    weather_press_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_press_label.place(relx = 0.05, rely = 0.4, anchor ='sw')

    weather_wind_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_wind_label.place(relx = 0.05, rely = 0.45, anchor ='sw')

    weather_desc_label = tk.Label(root, font=('calibri', 20), bg='black', fg='white')
    weather_desc_label.place(relx = 0.05, rely = 0.5, anchor ='sw')
    

    #create button to go back to homescreen
    Home =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Home", command = Homescreen2)
    Home.place(relx = 0.5, rely = 0.9, anchor = 'center')

    news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "News", command = news_function)
    news_button.place(relx = 0.92, rely = 0.15, anchor = 'sw')

    enter_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Entertainment News", command = enter_news_function)
    enter_news_button.place(relx = 0.61, rely = 0.15, anchor = 'sw')

    busi_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Business News", command = busi_news_function)
    busi_news_button.place(relx = 0.69, rely = 0.15, anchor = 'sw')

    sport_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Sports News", command = sports_news_function)
    sport_news_button.place(relx = 0.75, rely = 0.15, anchor = 'sw')

    health_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Health News", command = health_news_function)
    health_news_button.place(relx = 0.865, rely = 0.15, anchor = 'sw')

    science_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Science News", command = science_news_function)
    science_news_button.place(relx = 0.805, rely = 0.15, anchor = 'sw')

    tech_news_button = tk.Button(root, font=('calibri', 10), bg='black', fg='white', text = "Tech News", command = tech_news_function)
    tech_news_button.place(relx = 0.95, rely = 0.15, anchor = 'sw')

    update_weather_info()
    update_time_date()
    update_multi_news_info()

    weather_press_label.destroy()
    weather_hum_label.destroy()
    weather_wind_label.destroy()
    weather_desc_label.destroy()


# Call the update functions to start updating the UI

Start =tk.Button(root, font=('calibri', 8), bg='black', fg='white', text = "Start Smart Mirror", command = Homescreen1)
Start.place(relx = 0.5, rely = 0.9, anchor = 'center')


# Start the Tkinter main loop

root.mainloop()
