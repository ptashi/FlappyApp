import tkinter as tk 
import random
import time

# Game settings
WIDTH = 800
HEIGHT = 800
GRAVITY = 0.1
JUMP_POWER = 2.5

root = tk.Tk()
root.title("Flappy App")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

circleVelocity = 0

def keyPressed(event):
    if event.char == " ":
        global circleVelocity
        circleVelocity = -JUMP_POWER
 
root.bind("<Key>", keyPressed)

# Create the circle
circle = canvas.create_oval(42, 70, 92, 100, fill="red")

gameIsRunning = True


def moveCircle():
    global gameIsRunning
    global circleVelocity
    
    if not gameIsRunning:
        return
    coordsOfCircle = canvas.coords(circle)

    # Gravity
    circleVelocity += GRAVITY 

    canvas.move(circle, 0, circleVelocity) # Move the circle right by 0 and down by 1 pixel : Simulating gravity

    
    if coordsOfCircle[3] > HEIGHT or coordsOfCircle[1] < 0:
        gameIsRunning = False
        canvas.create_text(400, 400, text="GAME OVER", fill="red", font=("Impact", 40))
        return
    
    coordsOfCircle = canvas.coords(circle)
    
    # coordsOfCircle[0] is left, coordsOfCircle[1] is top, coordsOfCircle[2] is right, coordsOfCircle[3] is bottom
    # coords[0] is left, coords[1] is top, coords[2] is right, coords[3] is bottom
    
    for pipe in listOfPipes: # pipe = [top_pipe, bottom_pipe]
        top_pipe_coords = canvas.coords(pipe[0])
        bottom_pipe_coords = canvas.coords(pipe[1])
        
     # Checks if the left side of the bird is to the left of the right side of the top pipe.
    # Checks if the right side of the bird is to the right of the left side of the top pipe
    # Checks if the bottom of the bird is below the bottom side of the top pipe.
    # Checks if the top side of bird is above the bottom side of the top pipe.
        if (coordsOfCircle[0] < top_pipe_coords[2]  and coordsOfCircle[2] > top_pipe_coords[0] and
            coordsOfCircle[1] < top_pipe_coords[3]  and coordsOfCircle[3] > top_pipe_coords[1]) or \
           (coordsOfCircle[0] < bottom_pipe_coords[2]  and coordsOfCircle[2] > bottom_pipe_coords[0] and
            coordsOfCircle[1] < bottom_pipe_coords[3]  and coordsOfCircle[3] > bottom_pipe_coords[1]):
         gameIsRunning = False
         canvas.create_text(400, 400, text="GAME OVER", fill="red", font=("Impact", 40))
         return
    root.after(20, moveCircle)



# Create the pipes
listOfPipes = [] # List of all the pipes , data formar = [ [top_pipe, bottom_pipe], [top_pipe, bottom_pipe], ... ]

def spawnNewPipe(xOfPipe, widthOfPipe, gapPosition, gapOfPipe, bottomOfTheTopPipe):
    top_pipe = canvas.create_rectangle(xOfPipe, 0, xOfPipe + widthOfPipe, gapPosition, fill="darkgreen")
    bottom_pipe = canvas.create_rectangle(xOfPipe, gapPosition + gapOfPipe, xOfPipe + widthOfPipe, HEIGHT, fill="darkgreen")
    listOfPipes.append([top_pipe, bottom_pipe])

xOfPipe = 800
widthOfPipe = 50
gapPosition = 300
gapOfPipe = 100
bottomOfTheTopPipe = 500
gapBetweenPipes = 300

def movePipes():
    global gapPosition
    if not gameIsRunning:
        return
    
    if len(listOfPipes) == 0:
        spawnNewPipe(xOfPipe, widthOfPipe, gapPosition, gapOfPipe, bottomOfTheTopPipe)
    elif canvas.coords(listOfPipes[-1][0])[0] < WIDTH - gapBetweenPipes:
        gapPosition = random.randint(100,600)
        spawnNewPipe(xOfPipe, widthOfPipe, gapPosition, gapOfPipe, bottomOfTheTopPipe)

    for pipe in listOfPipes:
        for pipePart in pipe:
            if canvas.coords(pipePart)[2] < 0:
                canvas.delete(pipePart)
                listOfPipes.remove(pipe)
                break
            else:
                canvas.move(pipePart, -1, 0)
    
    root.after(10, movePipes)

def gameOver():
    root.unbind("<space>")
    gameIsRunning = False
    
    canvas.create_text(400, 400, text="GAME OVER", fill="red", font=("Impact", 40))


moveCircle()
movePipes()
root.mainloop()

