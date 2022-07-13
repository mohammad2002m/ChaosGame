import math
import pygame , sys
from InputBox import InputBox
from Button import Button
import random

pygame.init()

WIDTH , HEIGHT = (700 , 700)
BORDER_HEIGHT = 5
CIRCLES_RADIUS = 1
RANGE = 620
SIDE = 300


screen = pygame.display.set_mode((700, 700))
Border = pygame.Rect(0 , 625, WIDTH , BORDER_HEIGHT)

#exit
#start button
#stop button
#clear button
#Counter

#number of starting points
#ratio of distance
#Speed/FrameRate

#Point
MainPoints = []
Points = []
prev = -1
rule = False
Counter = 0
frame_rate = 1000
ColorsP = []
ColorsR = []


COUNTER_FONT = pygame.font.SysFont('comicsans', 20)

def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

def check(text):
    text2 = ""
    for char in text:
        if char != ' ':
            text2 += char

    arr = text2.split(',')
    for number in arr:
        if not number.isnumeric():
            return False

    return True

def get_array(text):
    text2 = ""
    for char in text:
        if char != ' ':
            text2 += char

    arr = text2.split(',')
    res = []
    for number in arr:
        res.append(int(number))

    for i in range(1 , len(res)):
        res[i] += res[i - 1]
    return res

def get_index(number , arr):
    # I could implement binary search since arr[i] > arr[i - 1]
    for i in range(0 , len(arr)):
        if (number <= arr[i]):
            return i

    print(number , arr)
    


def DrawPoint(NumberOfPoints , distance , arr):
    global Points , MainPoints , prev , first , Counter
    #clear

    n = NumberOfPoints

    center = pygame.Vector2(WIDTH / 2 , 350)

    if len(MainPoints) < NumberOfPoints:
        ang = 1.5 * math.pi + (len(MainPoints) - 1) * 2 * math.pi / n
        if (n % 2 == 0):
            ang = math.pi / n + (len(MainPoints) - 1) * 2 * math.pi / n

        x = SIDE * math.cos(ang) + center.x
        y = SIDE * math.sin(ang) + center.y
        MainPoints.append(pygame.Vector2(x , y))

    elif len(Points) == 0:
        first = True
        x = random.randint(0 , RANGE)
        y = random.randint(0 , RANGE)
        Points.append(pygame.Vector2(x , y))

    else:
        number = random.randint(1 , arr[-1])
        index = get_index(number , arr)
        if rule == True:
            while index == prev:
                number = random.randint(1 , arr[-1])
                index = get_index(number , arr)

            prev = index

        
        print(type(index))

        x = Points[-1].x + MainPoints[index].x
        y = Points[-1].y + MainPoints[index].y

        x *= distance
        y *= distance

        print(distance ,x , y)

        Points.append(pygame.Vector2(x , y))
    
    Counter += 1


def DrawAndRender(StartButton , RuleButton , ClearButton , ExitButton , MainPoints , Points , input_boxes):
    global Counter
    screen.fill((30 , 30 , 30))

    StartButton.draw(screen)
    RuleButton.draw(screen)
    ClearButton.draw(screen)
    ExitButton.draw(screen)

    pygame.draw.rect(screen, pygame.Color("white") , Border)
    screen.blit(COUNTER_FONT.render(str(Counter) , 1 ,  pygame.Color("white")) , (5 , 5))

    #Draw The Screen
    for box in input_boxes:
        box.draw(screen)


    for i in range(0 , len(MainPoints)):
        P = MainPoints[i]
        pygame.draw.circle(screen, pygame.Color('white') , (P.x , P.y) , CIRCLES_RADIUS , 0)


    for i in range(0 , len(Points)):
        P = Points[i]
        pygame.draw.circle(screen, pygame.Color('white') , (P.x , P.y) , CIRCLES_RADIUS , 0)


    pygame.display.update()

    pass

def main():
    global Points , MainPoints , rule , first , frame_rate , Counter

    clock = pygame.time.Clock()
    Points = []
    MainPoints = []

    screen.fill((30, 30, 30))

    #Text boxes
    numberOfpoints = InputBox(10, WIDTH - 60, 150, 55 , "3")
    distance = InputBox(170, WIDTH - 60, 150, 55 , "0.5")
    possibilites = InputBox(330, WIDTH - 60, 150, 55 , "1,1,1")
    input_boxes = [numberOfpoints, distance , possibilites]

    #Buttons
    StartButton = Button(pygame.Color("white"), 490 , WIDTH - 60, 75, 25 , "Start")
    RuleButton = Button(pygame.Color("red"), 490 , WIDTH - 30, 75, 25 , "Cons")
    ClearButton = Button(pygame.Color("white"), 570 , WIDTH - 60, 75, 25 , "Clear")
    ExitButton = Button(pygame.Color("white"), 570 , WIDTH - 30, 75, 25 , "Exit")

    #Counter
    Counter = 0
    DrawNext = False

    while True:
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)

            if ExitButton.isOver(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()

            if StartButton.isOver(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and DrawNext == False:
                if (numberOfpoints.text.isnumeric() and is_float(distance.text)) and check(possibilites.text) and len(get_array(possibilites.text)) == int(numberOfpoints.text):
                    DrawNext = True

            if ClearButton.isOver(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                main()

            if RuleButton.isOver(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and DrawNext == False:
                rule = not rule
                if RuleButton.color == pygame.Color("red"):
                    RuleButton = Button(pygame.Color("green"), 490 , WIDTH - 30, 75, 25 , "Cons")
                else:
                    RuleButton = Button(pygame.Color("red"), 490 , WIDTH - 30, 75, 25 , "Cons")
                
        
        if DrawNext == True:
                DrawPoint(int(numberOfpoints.text) , float(distance.text) , get_array(possibilites.text))

        DrawAndRender(StartButton , RuleButton , ClearButton , ExitButton , MainPoints , Points , input_boxes)

        


main()