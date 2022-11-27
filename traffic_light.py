import turtle
import time
import cv2

def traffic(num1,num2,num3):
	wn=turtle.Screen()
	#Label(wn,text='hi')
	wn.title("Smart traffic management")
	wn.bgcolor("black")
	#draw box around the stoplight
	pen=turtle.Turtle()
	pen.color("yellow")
	pen.width(3)
	pen.hideturtle()
	pen.penup()
	pen.goto(-30,60)
	pen.pendown()
	pen.fd(60)
	pen.rt(90)
	pen.fd(120)
	pen.rt(90)
	pen.fd(60)
	pen.rt(90)
	pen.fd(120)

	#red light
	red1=turtle.Turtle()
	red1.shape("circle")
	red1.color("white")
	red1.penup()
	red1.goto(0,40)

	yellow1=turtle.Turtle()
	yellow1.shape("circle")
	yellow1.color("white")
	yellow1.penup()
	yellow1.goto(0,0)

	green1=turtle.Turtle()
	green1.shape("circle")
	green1.color("white")
	green1.penup()
	green1.goto(0,-40)

	while True:
		yellow1.color("white")
		red1.color("red")
		time.sleep(num1)

		red1.color("white")
		green1.color("green")
		time.sleep(num2)

		green1.color("white")
		yellow1.color("yellow")
		time.sleep(num3)


	wn.mainloop()
if __name__=='__traffic__':
	traffic()