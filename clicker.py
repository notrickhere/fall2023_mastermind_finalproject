import turtle
from Point import *
'''
    Lab 3 Warm-up exercise: Event-driven programming pt 1: call-back functions
    99% of the time, we avoid global variables, but for this exercise
    it makes sense to define ONE pen/turtle we'll use across all functions
'''

_pen = turtle.Turtle()
    
def get_click(x, y):
    print("I caught you clicking at ({}, {})!".format(x, y))
    newPoint = Point(x,y)
    print('This is my new points ', newPoint.get_x(), newPoint.get_y())

def main():
    global _pen # tell main we're using the global pen
    screen = turtle.Screen()
    screen.screensize(635, 635)
    
    screen.onclick(get_click) # register your event handler
    
    _pen.circle(100) # draw a circle using the global pen

    turtle.done()
    
    # The turtle event loop continues from here, sort of like a
    # while True: until we exit the program

main()