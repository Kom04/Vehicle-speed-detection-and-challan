from requests.exceptions import HTTPError
from requests.exceptions import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import mysql.connector
from requests.auth import HTTPBasicAuth
from websocket import create_connection
import argparse
import sys
import os
import json
import requests
HOST = "https://api.pushbullet.com/v2"


class PushBullet():
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def _request(self, method, url, postdata=None, params=None, files=None):
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "User-Agent": "pyPushBullet"}

        if postdata:
            postdata = json.dumps(postdata)

        r = requests.request(method,
                             url,
                             data=postdata,
                             params=params,
                             headers=headers,
                             files=files,
                             auth=HTTPBasicAuth(self.apiKey, ""))

        r.raise_for_status()
        return r.json()

    def getDevices(self):
        """ Get devices
            https://docs.pushbullet.com/v2/devices

            Get a list of devices, and data about them.
        """

        return self._request("GET", HOST + "/devices")["devices"]

    def pushNote(self, recipient, title, body, recipient_type="device_iden"):

        data = {"type": "note",
                "title": title,
                "body": body}

        data[recipient_type] = recipient
        #data['title']="Threat Detected"

        return self._request("POST", HOST + "/pushes", data)
def getDevices(args):
    p = PushBullet(args.api_key)
    devices = p.getDevices()
    if args.json:
        print(json.dumps(devices))
        return
    for device in devices:
        if "manufacturer" in device:
            print("%s %s %s" % (device["iden"],
                            device["manufacturer"],
                            device["model"]))
        else:
            print(device["iden"])
def challan():
    mydb = mysql.connector.connect(user='root', password='898433',
                              host='localhost', database='cubein',
                              auth_plugin='mysql_native_password')
    mycursor = mydb.cursor()
    sql="SELECT * FROM vehicle_database a WHERE a.plate IN(SELECT plate FROM defaulters)"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    ticket=myresult[0]
    return ticket[1],ticket[4],ticket[5]
x,y,z=challan()
def pushNote(args):
    p = PushBullet(args.api_key)
    args.title='Fined for overspeeding'
    args.body=str(x)+' with lisenced vehicle number- '+str(z)+' fined for Rs 5000 for overspeeding.The fine is sent to your number- '+str(y)

    note = p.pushNote(args.device, args.title, " ".join(args.body))
    if args.json:
        print(json.dumps(note))
        return
    if args.device and args.device[0] == '#':
        print("Note broadcast to channel %s" % (args.device))
    elif not args.device:
        print("Note %s sent to all devices" % (note["iden"]))
    else:
        print("Note %s sent to %s" % (note["iden"], note["target_device_iden"]))



parser = argparse.ArgumentParser()
parser.add_argument("--json", default=False, action="store_const", const=True)
parser.add_argument("api_key")
subparser = parser.add_subparsers(dest="type")

getdevices = subparser.add_parser("getdevices", help="Get a list of devices")
getdevices.set_defaults(vars=getDevices)


note = subparser.add_parser("note", help="Send a note")
note.add_argument('device', type=str, help="Device ID")
#note.add_argument('title')
#note.add_argument('body', nargs=argparse.REMAINDER)
note.set_defaults(vars=pushNote)
args = parser.parse_args()
args.vars(args)