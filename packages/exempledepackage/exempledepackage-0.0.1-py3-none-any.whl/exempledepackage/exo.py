from turtle import *
from math import sin
def polygone(n):
    n = int(input(print("Veuillez entrer le nombre de côtés du polygone: ")))
    for i in range(n):
        forward(10*n)
        left(360/n)
        
    exitonclick()

def simuliutde(n):
    n=int(input("Entrer le nombre de côté de la spirale"))
    for i in range(n):
        forward(5 + i*5)
        left(45)

    exitonclick()

def poly():
    up()
    goto(-200, (1/100)*(-200)**2)
    down()
    for i in range(400):
        x = i - 200;
        goto(x,(1/100)*x**2)

    exitonclick()

def sinus():
    up()
    x = -300
    y = (100)*sin((1/20)*(-300))
    goto(x, y)
    down()
    for i in range(600):
        x = i - 300
        y = (100)*sin((1/20)*x)
        goto(x, y)

    exitonclick()



def triangledeSierpinski():
    up()
    goto(0, -200)
    down()
    speed(10)
    for i in range(3):
        color("green")
        forward(512)
        left(120)

        for i in range(3):
            color("blue")
            forward(256)
            left(120)

            for i in range(3):
                color("yellow")
                forward(128)
                left(120)

                for i in range(3):
                    color("red")
                    forward(64)
                    left(120)

                    for i in range(3):
                        color("green")
                        forward(32)
                        left(120)
                        
    exitonclick()




