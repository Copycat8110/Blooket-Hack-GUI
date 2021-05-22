# Imports necessary packages
try:
    import requests,json,sys,math,os,time
    import PySimpleGUI as sg
    from colorama import init, Fore, Back, Style
    from selenium.webdriver.common.keys import Keys
    from seleniumwire import webdriver
except Exception:
    import os
    print("Installing required packages")
    os.system("pip install requests")
    os.system("pip install PySimpleGUI")
    os.system("pip install selenium")
    os.system("pip install selenium-wire")
    os.system("pip install colorama")
    os.system("pip install webdriver-manager")
    import requests,json
    import PySimpleGUI as sg
    from colorama import init, Fore, Back, Style
    from selenium.webdriver.common.keys import Keys
    from seleniumwire import webdriver
init(autoreset=True)

# Sets color; defines place
sg.theme('DarkAmber')
def place(elem):
    return sg.Column([[elem]], pad=(0,0))

# Defines useful function for later
def checkDouble(lst):
	count={}
	for item in lst:
		if item not in count:
			count[item]=1
		else:
			return True
	return False

# Functions to make windows with layouts
# I use functions and seperate windows because the only way to make a dynamic layout is to put it inside a new window
def make_win1():
    layout = [[sg.Text('Game ID:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Set ID'), sg.Button('Exit')]]
    return sg.Window('Blooket Hack: Kick', layout, finalize=True)

def make_win2():
    return sg.Window('Blooket Hack: Player Kick List', layout2, finalize=True)

def make_win3():
    layout3 = [
            [sg.Text('Game ID:'), sg.Input(key='gameID')],
            [sg.Text('Bot Name:'), sg.Input(key='botsName')],
            [sg.Text('Number of Bots'), sg.Input(key='tempBots')],
            [sg.Button('Flood'), sg.Button('Exit')]
         ]
    return sg.Window('Blooket Hack: Bots', layout3, finalize=True)

def make_win4():
    layout4 = [
            [sg.Text('Blooket Hack GUI')],
            [sg.Button('Add Bots'), sg.Button('Kick Players'), sg.Button('Information'), sg.Button('Auto')]
         ]
    return sg.Window('Blooket Hack GUI', layout4, finalize=True, size=(320, 75))

def make_win5():
    layout5 = [
            [sg.Text('Game ID:'), sg.Input(key='gamePin')],
            [sg.Text('Name:'), sg.Input(key='gameName')],
            [sg.Button('Set ID', key='ID2'), sg.Button('Exit')]]
    return sg.Window('Blooket Hack: Auto Answer', layout5, finalize=True)

def make_win6():
    return sg.Window('Blooket Hack: Answer', layout6, finalize=True)

# Creates Windows, sets up Window 4 as the main one
window1, window2, window3, window4, window5, window6 = None, None, None, make_win4(), None, None
tempAnswer, Answer = None, None
StopLoop = None

# Sets up the Chrome Driver
webdriver_location="chromedriver.exe"
options=webdriver.ChromeOptions()
options.use_chromium=True
options.add_experimental_option('excludeSwitches',['enable-logging'])

# Finds Chrome Path
ChromePresent = True
if os.path.isfile(r'C:\Program Files\Google\Chrome\Application\chrome.exe'):
	options.binary_location=r'C:\Program Files\Google\Chrome\Application\chrome.exe'
elif os.path.isfile(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'):
	options.binary_location=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
else:
	sg.popup("Blooket Auto Answer Requires Chrome To Be Installed.\nYou can still use the other features.")
	ChromePresent = False
	
# Event Loop
while True:
    window, event, values = sg.read_all_windows(timeout=100)
    # Breaks event loop, effectivly closes window
    if event == sg.WIN_CLOSED or event == 'Exit':
        try:
            window.close()
        except Exception: # In case all windows are closed
            sys.exit()
        if window == window2:       # If closing win 2, mark as closed
            window2 = None
        elif window == window1:     # If closing win 1, emark as closed, ect.
            window1 = None
        elif window == window3:
            window3 = None
        elif window == window4:
            window4 = None
        elif window == window5:
            window5 = None
        elif window == window6:
            window6 = None

    # Activates when Setting game code    
    if event == 'Set ID':
        if not window2:
            window['-OUTPUT-'].update(values['-IN-'])
            gamePin = str(values['-IN-'])

            # Checks that the game pin is 6 characters
            if len(gamePin) != 6:
                sg.popup("The GameID should be 6 characters")
            else:
                
                # kgsenseis code to obtain a list of names in a lobby
                r=requests.put("https://api.blooket.com/api/firebase/join",data={"id":gamePin,"name":"blooketbad"},headers={"Referer":"https://www.blooket.com/"})
                joinText=r.text
                r=requests.delete(f"https://api.blooket.com/api/firebase/client?id={gamePin}&name=blooketbad",headers={"Referer":"https://www.blooket.com/"})

                if joinText == """{"success":false,"msg":"no game"}""":
                    sg.popup("No game found!")
                else:
                    players=json.loads(joinText)["host"]["c"].keys()

                    # Some protection to ensure that people dont name themselves after my keys and break it
                    play = []
                    for playerName in players:
                        tempName = 'player' + playerName
                        play.append(tempName)

                    # Splits the list into equally sized chunks that make up a square array

                    Square = int(math.ceil(len(play) ** (1/2)))
                    play = [play[i:i + Square] for i in range(0, len(play), Square)]
                    print(play)

                    # Adds empty lists in case of error

                    if len(play) != Square:
                        play.append([])
                    
                    # Second layout listing the names from previous code
                    i = 0
                    layout2 = [[[place(sg.Button(playerName[6:], size=(10, 5), key=(playerName), pad=(0,0))) for playerName in play[i]] for i in range(Square)],
                               [sg.Button("Kick All", key='-KICK-'), sg.Button("Exit")]]
                    window2 = make_win2()
        else:
            sg.popup('Close your current Kicking window to open another.')
         
    # Activates when you click a players name
    try :
        if event[:6] == 'player':
            print(event[:6])
            # Kicks the player with the name
            r=requests.delete(f"https://api.blooket.com/api/firebase/client?id={gamePin}&name={event[6:]}",headers={"Referer":"https://www.blooket.com/"})
            window[event].update(visible=False)
    except Exception:
        pass

    # Activates when kicking all
    if event == '-KICK-':
            tempPlay = [item for sublist in play for item in sublist]
            for playerName in tempPlay: # A loop to kick everyone
                r=requests.delete(f"https://api.blooket.com/api/firebase/client?id={gamePin}&name={playerName[6:]}",headers={"Referer":"https://www.blooket.com/"})
                window[playerName].update(visible=False)
            sg.popup('Success! All players kicked.')
            
    # Information pop up
    if event == 'Information':
        sg.popup('This is a GUI prodcued by CopyCat',"It is based off kgsenseis' Blooket Hack",'https://github.com/kgsensei/BlooketHack','\nAt the moment it does not work with main.py')

    # Opens the window to kick players, checks window is not currently open
    if event == 'Kick Players':
        if not window1:
            window1 = make_win1()
        else:
            sg.popup("Close your previous Kick window before opening another")

    # Opens the window to bot players, checks window is not currently open
    if event == 'Add Bots':
        if not window3:
            window3 = make_win3()
        else:
            sg.popup("Close your previous Bot window before opening another")

    # Begins the process of adding bots
    # I forgot Continue was a thing...
    if event == 'Flood':
        if len(str(values['gameID'])) != 6:
            print(str(values['gameID']))
            sg.popup("The GameID should be 6 characters") # Checks that the game ID is 6 characters
        else:
            try:
                botsInt = int(values['tempBots'])
                Error = False
            except ValueError:
                sg.popup("The bot number must be an integer")
                Error = True
            if Error == True: # Is false if try caught error
                pass
            else:
                if botsInt > 60:
                    botsInt = 60
                    sg.popup("Bots changed to 60","You can only have a maximum of 60 players in a Blooket game.") # Changes bots to 60
                for i in range(0,botsInt):
                    r = requests.put("https://api.blooket.com/api/firebase/join", data={"id":str(values['gameID']),"name":str(values['botsName'])+' '+str(i)},headers={"Referer":"https://www.blooket.com/"})
                    if r.text == """{"success":false,"msg":"taken"}""": # Identifies Errors
                        sg.popup(str(values['botsName'])+' '+str(i) + " was Taken! Choose a different name!")
                    if r.text == """{"success":false,"msg":"no game"}""":
                        if i > 0:
                            sg.popup("Game Full! " + str(i) + "bots added.")
                            break
                        sg.popup("No game found!")
                        break

    # Opens the Auto Answer Input
    if event == 'Auto':
        if ChromePresent == False:
            continue
        if window5 != None:
            sg.popup('Close your current Auto Answer window to open another.')
            continue
        window5 = make_win5()

    # Starts the Auto Answer
    if event == 'ID2':
        driver=webdriver.Chrome(options=options,executable_path=webdriver_location)
        questionList=[]
        driver.get('https://www.blooket.com/play')
        time.sleep(1)
        # Enters the Name and Pin into the respective places
        gamepinenter=driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/input')
        gamepinenter[0].send_keys(values['gamePin'])
        gamepinjoin=driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[2]')
        gamepinjoin[0].click()
        time.sleep(3)
        # Detects error
        try:
            nameinenter=driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[2]/input')
            nameinenter[0].send_keys(values['gameName'])
            nameinjoin=driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/div/form/div[2]/div')
            nameinjoin[0].click()
        except Exception:
            sg.popup("Error: Invalid Game Pin or Error Joining.\nTry again with a correct Pin / Name")
            driver.close()
            window.close()
            window5 = None
            continue
        sg.popup("\nPress 'OK' When Ready To Start Cheat\n Warning, it may take a while to load")
        # Defines more stuff
        for request in driver.requests:
            if request.response:
                if "https://api.blooket.com/api/games?gameId=" in request.url:
                    jsondata=request.response.body
                    jsondata=jsondata.decode("utf-8")
                    jsondata=json.loads(jsondata)

        for question in jsondata['questions']:
            questionList.append(question["question"])
        # Checks that no question has more than 2 answers
        if checkDouble(questionList):
            sg.popup("The bot cannot answer a question with the same text as another question.\n The bot may glitch a little if this happens.")
        # Starts Answer loop
        StopLoop = False

        # Begins Answer Loop
    if StopLoop == False:
        # Finds the question, gets the answer, checks 3 different paths
        if driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div'):
            try:
                questionShown=driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div')
                questionShown=questionShown[0].get_attribute("textContent")
                for question in jsondata['questions']:
                        if str(question["question"])==questionShown:
                                Answer = (str(question["correctAnswers"][0]))
            except Exception:
                    pass

        elif driver.find_elements_by_xpath('//*[@id="left"]/div/div[1]/div'):
            try:
                questionShown=driver.find_elements_by_xpath('//*[@id="left"]/div/div[1]/div')
                questionShown=questionShown[0].get_attribute("textContent")
                for question in jsondata['questions']:
                        if str(question["question"])==questionShown:
                                Answer = (str(question["correctAnswers"][0]))
            except Exception:
                pass

        elif driver.find_elements_by_xpath('//*[@id="body"]/div[3]/div/div[1]/div'):
            try:
                questionShown=driver.find_elements_by_xpath('//*[@id="body"]/div[3]/div/div[1]/div')
                questionShown=questionShown[0].get_attribute("textContent")
                for question in jsondata['questions']:
                    if str(question["question"])==questionShown:
                        Answer = (str(question["correctAnswers"][0]))
            except Exception:
                pass
        
    # Creates a window with the answer, closes and opens a new window for each Answer
    if Answer == tempAnswer:
        pass
    else:
        if window6 != None:
            window6.close()
        layout6 = [[sg.Text('Answer: ' + Answer,justification='center')],
                   [sg.Button('Auto Answer'), sg.Button('Stop')]]
        window6 = make_win6()

        try:
            tempAnswer = Answer
        except Exception:
            pass

    # Checks for different event flags
    if event == 'Stop':
        StopLoop = True0
        window6.close()
        driver.close()
        
# Closes the window, should effectivly end the program
sys.exit()
