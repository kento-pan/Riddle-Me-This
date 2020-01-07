import PySimpleGUI as sg
import pyAesCrypt
import os


def encrypt():

    buffer_size = 64 * 1024
    og_filename = os.path.basename(path_to_og_file)

    if len(encryption_password) >= 1:
        try:
            pyAesCrypt.encryptFile(path_to_og_file, os.path.join(save_encrypted_file_to, og_filename + ".riddle"), encryption_password, buffer_size)
            sg.popup("File encrypted.")
        except IOError:
            sg.popup("File not found or permission denied. Please choose another directory to save the file.", title="Oh snap!")
        #  except PermissionError as error:  PermissionError not caught for whatever reason. Have to look into it.
        #  sg.popup(error, title="Oh snap!") \site-packages\pyAesCrypt\crypto.py", line 92
    else:
        sg.popup("Please choose a password.", title="Oh snap!")


def decrypt():

    buffer_size = 64 * 1024
    encrypted_file_sans_path = os.path.basename(path_to_encrypted_file)
    decrypted_file = encrypted_file_sans_path.replace(".riddle", "")

    if ".riddle" in path_to_encrypted_file:
        try:
            pyAesCrypt.decryptFile(path_to_encrypted_file, os.path.join(save_decrypted_file_to, decrypted_file), decryption_password, buffer_size)
            sg.popup("File decrypted.")
        except ValueError as ve:  # Checks if the password is correct or if the file is corrupted.
            sg.popup(ve, title="Oh snap!")
        except IOError:
            sg.popup("Permission denied. Please choose another directory to save the file.", title="Oh snap!")
    else:
        sg.popup("Please choose an encrypted .riddle file.", title="Oh snap!")


# GUI theme and layout
sg.theme("BrownBlue")

layout = [[sg.Text("Encryption")],
          [sg.Text("Choose the file you want to encrypt:  "), sg.In(), sg.FileBrowse()],
          [sg.Text("Save file to:                                     "), sg.In(), sg.FolderBrowse()],
          [sg.Text("Create a password for your file:         "), sg.InputText(), sg.Button("Encrypt")],
          [sg.Text("_"*86)],
          [sg.Text("Decryption")],
          [sg.Text("Choose the file you want to decrypt:  "), sg.In(), sg.FileBrowse()],
          [sg.Text("Save file to:                                     "), sg.In(), sg.FolderBrowse()],
          [sg.Text("Enter the password:                         "), sg.InputText(), sg.Button("Decrypt")],
          [sg.Button("Quit")],
          [sg.Text("")]]

# Create the Window
window = sg.Window("Riddle me this", layout, icon="protec.ico")

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    path_to_og_file = values[0]
    save_encrypted_file_to = values[1]
    encryption_password = values[2]
    path_to_encrypted_file = values[3]
    save_decrypted_file_to = values[4]
    decryption_password = values[5]

    if event in (None, "Quit"):  # if user closes window or clicks cancel
        break

    # Encryption
    if event == "Encrypt":
        encrypt()
    # Decryption
    if event == "Decrypt":
        decrypt()

window.close()
