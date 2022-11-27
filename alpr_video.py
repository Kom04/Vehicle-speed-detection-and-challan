#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import argparse
import io
import json
import time
from tkinter import *
import requests
from PIL import Image
import mysql.connector
import cv2


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        'Read license plates from a video and output the result as JSON.',
        epilog=
        'For example: python alpr_video.py --api MY_API_KEY --start 900 --end 2000 --skip 3 "/path/to/cars.mp4"'
    )
    parser.add_argument('--api', help='Your API key.', default='3f9be9eec715ee5b859b5e9972a97504616896fe')
    parser.add_argument('--start',
                        help='Start reading from this frame.',
                        default=3)
    parser.add_argument('--end', help='End reading after this frame.', default=100)
    parser.add_argument('--skip', help='Read 1 out of N frames.', default=4)
    #parser.add_argument('FILE', help='Path to video.')
    return parser.parse_args()
def graphic(res):
    master = Tk()
    master.title("Number Plates of the overspeeding cars")
    master.geometry("400x200")
    master.iconbitmap(r'cctv_Glf_icon.ico')
    listbox = Listbox(master,bg='black',fg='white',width=20)
    listbox.pack()

    listbox.insert(END, "Plates detected")

    for item in res:
        listbox.insert(END, item)

    mainloop()

def main_plate():
    mydb = mysql.connector.connect(user='root', password='898433',
                              host='localhost', database='cubein',
                              auth_plugin='mysql_native_password')
    mycursor = mydb.cursor()
    sql = "DELETE FROM defaulters"

    mycursor.execute(sql)
    args = parse_arguments()
    result = []
    cap = cv2.VideoCapture("test3.mp4")
    frame_id = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        frame_id += 1
        if args.skip and frame_id % args.skip != 0:
            continue
        if args.start and frame_id < args.start:
            continue
        if args.end and frame_id > args.end:
            break
        #print('Reading frame %s' % frame_id)
        imgByteArr = io.BytesIO()
        im = Image.fromarray(frame)
        im.save(imgByteArr, 'JPEG')
        imgByteArr.seek(0)
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=imgByteArr),
            headers={'Authorization': 'Token ' + args.api})
        result.append(response.json())
        
        #cv2.putText(frame, "plates: " + str(response), (0,frame.shape[0] -40), cv2.FONT_HERSHEY_TRIPLEX, 0.7,  (255,255,255), 1)
        #print("\n")
        time.sleep(1)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
    
    with open('plates.json', 'w') as json_file:
        json.dump(result, json_file)
    m=json.dumps(result, indent=2)
    #print(m)
    
    x=[]
    y=[]
    res=[]
    with open('plates.json') as json_file:
        data = json.load(json_file)

        for i in range(len(data)-1):
            #print(data[i])
            #print('\n')
            for key,value in data[i].items():
                #print(key,value)
                if key=='results':
                    for key1,value1 in value[0].items():
                        #print('key1:',key1,value1)
                        if key1=='plate':
                            #print("plate:",value1)
                            x.append(value1)
                            #print('\n')
                            
                    [res.append(i) for i in x if i not in res]
        print(res)
        for i in res:
            sql = "INSERT INTO defaulters (plate,speed) VALUES (%s, %s)"
            val = (i, 'overspeeding')
            mycursor.execute(sql, val)
            sql1="SELECT * FROM vehicle_database a WHERE a.plate IN(SELECT plate FROM defaulters)"
            mycursor.execute(sql1)
            myresult = mycursor.fetchall()
            print(myresult)


            mydb.commit()

            print(mycursor.rowcount, "record inserted.")
        ticket=myresult[0]
        print(str(ticket[4]))
        #y.append(str(ticket[4]))
        #data(y)
        graphic(res)
        
    """for key,value in x[0].items():
                    #print(key)
                    if key=='results':
                        for key1,value1 in value[0].items():
                            #print(key1)
                            if key1=='plate':
                                print("plate:",value1)"""
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main_plate__':
    main_plate()
