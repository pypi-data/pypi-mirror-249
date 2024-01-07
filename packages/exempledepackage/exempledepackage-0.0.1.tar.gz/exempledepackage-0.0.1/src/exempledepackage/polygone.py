from turtle import *
from math import *

def triangledeSierpinski():
    up()
    goto(-200, -200)
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

def polygone(n, long):
    up()
    goto(-200, -200)
    down()
    speed(500)
    width(3)
    for i in range(n):
        forward(32*long)
        left(360/n)
        for i in range(n):
            forward(16*long)
            left(360/n)
            for i in range(n):
                forward(8*long)
                left(360/n)
                for i in range(n):
                    forward(4*long)
                    left(360/n)
                    for i in range(n):
                        forward(4*long)
                        left(360/n)
                        
    
    exitonclick()
polygone(5, 8)
