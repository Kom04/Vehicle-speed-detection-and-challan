from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from detection import detect
from traffic_detection import traffic_detect
import os
from livevehicle import video
from alpr_video import *
from plate_video import video_plate
import webbrowser
#ip based live cameras and database of registered vehicles
def registered():
	global screen5
	screen5=Toplevel(main)
	screen5.title("REGISTERED VEHICLE OWNERS INFO")
	screen5.geometry("500x400")
	screen5.iconbitmap(r'cctv_Glf_icon.ico')
	mydb = mysql.connector.connect(user='root', password='898433',
                              host='localhost', database='cubein',
                              auth_plugin='mysql_native_password')
	mycursor = mydb.cursor()
	sql="SELECT * FROM vehicle_database"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	for index, dat in enumerate(myresult):
	        Label(screen5, text=dat[0]).grid(row=index+1, column=0)
	        Label(screen5, text=dat[1]).grid(row=index+1, column=1)
	        Label(screen5, text=dat[2]).grid(row=index+1, column=2)
	        Label(screen5, text=dat[3]).grid(row=index+1, column=3)
	        Label(screen5, text=dat[4]).grid(row=index+1, column=4)
	        Label(screen5, text=dat[5]).grid(row=index+1, column=5)

def issued():
	global screen6
	screen6=Toplevel(main)
	screen6.title("PEOPLE WHO ARE OVERSPEEDING")
	screen6.geometry("500x400")
	screen6.iconbitmap(r'cctv_Glf_icon.ico')

	mydb = mysql.connector.connect(user='root', password='898433',
                              host='localhost', database='cubein',
                              auth_plugin='mysql_native_password')
	mycursor = mydb.cursor()
	sql="SELECT * FROM vehicle_database a WHERE a.plate IN(SELECT plate FROM defaulters)"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	for index, dat in enumerate(myresult):
	        Label(screen6, text=dat[0]).grid(row=index+1, column=0)
	        Label(screen6, text=dat[1]).grid(row=index+1, column=1)
	        Label(screen6, text=dat[2]).grid(row=index+1, column=2)
	        Label(screen6, text=dat[3]).grid(row=index+1, column=3)
	        Label(screen6, text=dat[4]).grid(row=index+1, column=4)
	        Label(screen6, text=dat[5]).grid(row=index+1, column=5)
def fine():
	os.system("python send_challan.py o.1MV4C5yZGVmoAgi13BsoZhwpAorPGc8u note ujvwiBUxiX6sjA0ZMWiuK4")
def database():
	global screen3
	screen3=Toplevel(main)
	screen3.title("GOVERNMENT DATABASE")
	screen3.geometry("500x400")
	screen3.iconbitmap(r'cctv_Glf_icon.ico')
	Label(screen3,text="").pack()
	y=Label(screen3, text="Welcome to Government Database for vehicle",font=60)
	y.pack()
	Label(screen3,text="").pack()    
	Button(screen3,text="Info of All registered vehicle",width=30,height=1,command=registered,bg='black',fg='white',borderwidth=3).pack()
	Label(screen3,text="").pack()

	Label(screen3,text="").pack()
	Button(screen3,text="Vehicle to whom challan is issued",width=30,height=1,command=issued,bg='black',fg='white',borderwidth=3).pack()
	Label(screen3,text="").pack()
	Label(screen3,text="").pack()

	Button(screen3,text="send fine to all numbers",width=30,height=1,command=fine,bg='black',fg='white',borderwidth=3).pack()
	Label(screen3,text="").pack()
	Label(screen3,text="").pack()
def challan():
	os.system("python all_vehicle.py o.1MV4C5yZGVmoAgi13BsoZhwpAorPGc8u note ujvwiBUxiX6sjA0ZMWiuK4")
def smart():
	global screen4
	screen4=Toplevel(main)
	screen4.title("Smart Traffic management")
	screen4.geometry("400x300")
	screen4.iconbitmap(r'cctv_Glf_icon.ico')
	Label(screen4,text="").pack()
	y=Label(screen4, text="Welcome to Smart traffic management")
	y.pack()
	Label(screen4,text="using vehicle detection").pack()
	Label(screen4,text="").pack()   

	Button(screen4,text="Vehicle Detection",width=40,height=1,command=detect,bg='black',fg='white',borderwidth=3).pack()
	Label(screen4,text="").pack()

	Label(screen4,text="").pack()
	Label(screen4,text="click below to see smart traffic").pack()
	Label(screen4,text="management").pack()


	Button(screen4,text="Smart Traffic management",width=40,height=1,command=traffic_detect,bg='black',fg='white',borderwidth=3).pack()
	Label(screen4,text="").pack()
	Label(screen4,text="").pack()
def speed():
	global screen2
	screen2=Toplevel(main)
	screen2.title("NEM-VISION")
	screen2.geometry("500x400")
	screen2.iconbitmap(r'cctv_Glf_icon.ico')
	Label(screen2,text="").pack()
	y=Label(screen2, text="WELCOME TO VEHICLE PATROLLING PORTAL",font=60)
	y.pack()
	Label(screen2,text="").pack()    
	Button(screen2,text="Live video patrolling",width=30,height=1,command=video,bg='black',fg='white',borderwidth=3).pack()
	Label(screen2,text="").pack()
	Label(screen2, text="Click below to find out how our cutting edge technology").pack()
	Label(screen2,text="is controlling the traffic").pack()
	Label(screen2,text="").pack()
	Button(screen2,text="Vehicle detection and traffic management",width=40,height=1,command=smart,bg='black',fg='white',borderwidth=3).pack()
	Label(screen2,text="").pack()
	Label(screen2, text="Click below to ").pack()
	Label(screen2,text="find whether car is overspeeding or not").pack()
	Label(screen2,text="").pack()
	Button(screen2,text="Speed detection and challan",width=30,height=1,command=challan,bg='black',fg='white',borderwidth=3).pack()
	Label(screen2,text="").pack()

def plate_detect():
	os.chdir("/project/computervision/garbage detection/pyPushBullet-master/vehicle/model-20191217T031955Z-001/model/models/research/object_detection")
	os.system('cmd /k "activate tense"')
	#os.system("python vehicle_video.py")
def plate():
	global screen3
	screen3=Toplevel(main)
	screen3.title("NUMBER PLATE RECOGNITION")
	screen3.geometry("500x400")
	screen3.iconbitmap(r'cctv_Glf_icon.ico')
	Label(screen3,text="").pack()
	y=Label(screen3, text="NUMBER PLATE RECOGNITION Portal",font=60)
	y.pack()
	Label(screen3,text="").pack()    
	Button(screen3,text="Video to recognize number plate",width=30,height=1,command=video_plate ,bg='black',fg='white',borderwidth=3).pack()
	Label(screen3,text="").pack()
	Label(screen3,text="").pack()

	Button(screen3,text="Number plate recognition",width=30,height=1,command=main_plate,bg='black',fg='white',borderwidth=3).pack()
	Label(screen3,text="").pack()
	

	Label(screen3,text="Click below to see how the number ").pack()
	Label(screen3,text=" plate recognition work through detection").pack()

	Button(screen3,text="Number Plate Detection",width=30,height=1,command=plate_detect,bg='black',fg='white',borderwidth=3).pack()
	Label(screen3,text="").pack()
	Label(screen3,text="").pack()
def traffic_rates():
	webbrowser.open('https://www.acko.com/articles/traffic-rules-violations/changes-in-fines-and-penalties-for-violators/')
	
global main
main=Tk()
main.title("NEM-VISION")
main.geometry("450x400")
main.iconbitmap(r'cctv_Glf_icon.ico')

#create a menubar
menubar=Menu(main)
main.config(menu=menubar)

#create the submenu
subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label='Open',command=traffic_rates)
subMenu.add_command(label='Exit',command=quit)

menubar.add_command(label='Exit',command=quit)
#adding a label
x=Label(main, text="NEM-VISION",font=100)
x.pack()
#adding a button
Label(main,text="A Vehicle surveillance Basestation").pack()
Label(main,text="").pack()


Button(main,text="Govt Database",width=30,command=database,borderwidth=6,bg='black',fg='white').pack()
Label(main,text="").pack()
Label(main,text="").pack()
Button(main,text="Vehicle patrolling",width=20,command=speed,borderwidth=3,bg='#000fff000',fg='black').pack()
Label(main,text="").pack()
"""Button(main,text="Recognize face from nearby cameras",width=50,command=faceid).pack()
Label(main,text="").pack()
Button(main,text="Weapon detection",width=50,command=crime).pack()"""
Button(main,text="Vehicles Number Plate",width=20,command=plate,borderwidth=3,bg='red',fg='black').pack()
Label(main,text="").pack()
Label(main,text="").pack()

main.mainloop()