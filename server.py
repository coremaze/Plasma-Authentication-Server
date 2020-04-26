from flask import Flask, request
from enum import Enum
from encryption import *
import platform
from datetime import datetime

if platform.system() == 'Linux':
    LOG_PATH = '/var/log/picroma-authentication.log'
else:
    LOG_PATH = 'picroma-authentication.log'

Activation = Enum('Activation', 'Logout Activate Login Validate Deactivate')
SHEET_PLX = 'sheet.plx'

app = Flask(__name__)

def Log(message):
    now = str(datetime.now())
    fmtstring = f'[{now}] {message}'
    print(fmtstring)
    with open(LOG_PATH, 'a') as f:
        f.write(fmtstring)
        f.write('\n')
    

def AttemptActivation(encryptedSessionID, activationType):
    sessionID = decrypt(unhexdump(encryptedSessionID), PLASMA_CLIENT_KEY)
    serial, machineID = sessionID[:-160].decode(), sessionID[-160:]
    machineID = decrypt(machineID, PLASMA_SERVER_KEY)
    ip = request.remote_addr
    Log(f'{ip}: Activation: {activationType.name}')
    Log(f'{ip}: Serial: {serial}')
    Log(f'{ip}: Decrypted machine ID: {machineID}')
    with open(SHEET_PLX, 'rb') as f:
        plx = f.read()
    encrypted_plx = encrypt(plx, machineID)
    return encrypted_plx


@app.route('/LS/Activation/Logout/')
def Logout():
    return AttemptActivation(request.args.get('id'), Activation.Logout)

@app.route('/LS/Activation/Activate/')
def Activate():
    return AttemptActivation(request.args.get('id'), Activation.Activate)

@app.route('/LS/Activation/Login/')
def Login():
    return AttemptActivation(request.args.get('id'), Activation.Login)

@app.route('/LS/Activation/Validate/')
def Validate():
    return AttemptActivation(request.args.get('id'), Activation.Validate)

@app.route('/LS/Activation/Deactivate/')
def Deactivate():
    return AttemptActivation(request.args.get('id'), Activation.Deactivate)

if __name__ == '__main__':
    app.run(port=80)
