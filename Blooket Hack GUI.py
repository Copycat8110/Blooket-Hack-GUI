# Imports necessary packages
try:
    import requests,json
    import PySimpleGUI as sg
    import sys
    import math
    import pprint
except Exception:
    import os
    print("Installing required packages")
    os.system("pip install requests")
    os.system("pip install PySimpleGUI")
    import requests,json
    import PySimpleGUI as sg

# Sets color; defines place
sg.theme('DarkAmber')
def place(elem):
    return sg.Column([[elem]], pad=(0,0))

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
            [sg.Button('Add Bots'), sg.Button('Kick Players'), sg.Button('Information')]
         ]
    return sg.Window('Blooket Hack GUI', layout4, finalize=True, size=(290, 75))

# Creates Windows, sets up Window 4 as the main one
window1, window2, window3, window4 = None, None, None, make_win4()

# Event Loop
while True:
    window, event, values = sg.read_all_windows()
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
                    
# Closes the window, should effectivly end the program
sys.exit()


	
