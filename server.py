from flask import Flask, request
from enum import Enum
from encryption import *

Activation = Enum('Activation', 'Logout Activate Login Validate Deactivate')
SHEET_PLX = 'sheet.plx'

app = Flask(__name__)


def AttemptActivation(encryptedSessionID, activationType):
    sessionID = decrypt(unhexdump(encryptedSessionID), PLASMA_CLIENT_KEY)
    serial, machineID = sessionID[:16].decode(), sessionID[16:]
    machineID = decrypt(machineID, PLASMA_SERVER_KEY)
    print(f'ACTIVATION: {activationType.name}\nSERIAL: {serial}\nMACHINE: {machineID}')
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
