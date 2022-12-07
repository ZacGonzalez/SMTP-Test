# Import Statements
import PySimpleGUI as sg
import smtplib
from email.mime.text import MIMEText
from email.utils import make_msgid
import ssl
import sys


# Theme
sg.theme('LightBrown1')

# Define the window's contents
layout = [[sg.Text("Server Name:", font=('Times New Roman', 12), size=(20, 1)), sg.Input()],
          [sg.Text("Port:", font=('Times New Roman', 12), size=(20, 1)), sg.Input()],
          [sg.Text("Email:", font=('Times New Roman', 12), size=(20, 1)), sg.Input()],
          [sg.Text("Username:", font=('Times New Roman', 12), size=(20, 1)),
          sg.Input("", s=(45, 1), disabled=False, k="-USR-")],
          [sg.T("Password:", font=('Times New Roman', 12), size=(20, 1)),
          sg.Input("", s=(45, 1), disabled=False, k="-PASS-")],
          [sg.Text("Recipient Email:", font=('Times New Roman', 12), size=(20, 1)), sg.Input()],
          [sg.Text("Subject:", font=('Times New Roman', 12), size=(20, 1)), sg.Input()],
          [sg.Text("Message:", font=('Times New Roman', 12), size=(20, 1)), sg.Input(do_not_clear = False)],
          [sg.T("       "), sg.Checkbox("No Auth", font = ('Times New Roman', 12), key = '-NOAUTH-',
          default = False, enable_events = True), sg.T("                                                         "),
          sg.Button('Test', font=('Times New Roman', 18), size=(10, 1))],
          [sg.Output(size = (65, 10), key = '-OUTPUT-'), sg.Button('Clear', font = ('Times New Roman', 12), key = "-CLEAR-")]]

# Create the window
window = sg.Window('SMTP Test', layout)  # , grab_anywhere = True)

# Display and interact with the Window using an Event Loop
while True:

    event, values = window.read()

    # See if user wants to quit or window was closed
    if event == None:
        break

    elif event == '-CLEAR-':
        window['-OUTPUT-']('')

    if values['-NOAUTH-'] == True:
        window['-USR-'].Update(visible = False)
        window['-PASS-'].Update(visible = False)

    if values['-NOAUTH-'] == False:
        window['-USR-'].Update(visible = True)
        window['-PASS-'].Update(visible = True)

    if values[5] != "":

        # Try statement in case of error
        try:

                # If Port is 25
                if values[1] != '465' and values[1] != '587':

                    # Make MSG ID
                    ID = make_msgid()

                    msg = MIMEText(values[4])

                    # me = Sender Address, you = Recipient Address
                    me = values[2]
                    you = values[3]

                    # Message Structure
                    msg['message-id'] = ID
                    msg['Subject'] = values[4]
                    msg['From'] = me
                    msg['To'] = you

                    # Send the message via the SMTP server
                    s = smtplib.SMTP(values[0])
                    s.sendmail(me, you, msg.as_string())
                    s.quit

                else:

                    # Message contents with port and app password
                    message = "Subject: " + values[4] + "\n" + "\n" + values[5]
                    usrname = values['-USR-']
                    app_password = values['-PASS-']

                    context = ssl.create_default_context()

                    # If Port = 465
                    if values[1] == '465':
                        # SSL Command
                        with smtplib.SMTP_SSL(values[0], 465, context=context) as server:
                            server.login(usrname, app_password)
                            server.sendmail(values[2], values[3], message)

                    # If Port = 587
                    if values[1] == '587':
                        # STARTTLS
                        with smtplib.SMTP(values[0], 587) as server:
                            server.starttls(context=context)  # Secure connection with TLS
                            server.login(usrname, app_password)
                            server.sendmail(values[2], values[3], message)


        # If there is an error
        except:

            print (sys.exc_info()[0])

        # If there is no error
        else:

            sg.popup('Message Sent', text_color='green')
            print('Message Sent')


            if values[1] != '465' and values[1] != '587':

                print('Message ID:' + "\n" + ID)

# Finish up by removing from the screen
window.close()


