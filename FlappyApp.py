import tkinter as tk
import random
from PIL import Image, ImageTk

print("Hello Bellolo")
"""
TODO: 
- Add a score counter
- Add more characters
- Add a game over screen
- Add a start screen (includes character selection, etc.)
BONUS TODO:
- Add a high score counter
- Add a jump sound
- Add a game over sound
- Add a settings screen (to disable sound, change background, etc.)
- Add a background music
POSSIBLE OPTIMIZATIONS:
- Improve hitbox for character (especially if they aren't rectangular)
"""

# Game settings
WIDTH = 800
HEIGHT = 800
GRAVITY = 0.1
JUMP_POWER = 2.9
BACKGROUND_LIST = []
BACKGROUND_SPEED = 1  # Adjust the speed of background movement

root = tk.Tk()
root.title("Flappy App")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

happyVelocity = 0


def jump_ending_animation():
    canvas.itemconfig(happy, image=happyUp)


def jump(event):
    if gameIsRunning:
        if event.char == " ":
            global happyVelocity
            happyVelocity = -JUMP_POWER
            canvas.itemconfig(happy, image=happyDown)
            canvas.after(100, jump_ending_animation)


root.bind("<Key>", jump)

# original_bg = tk.PhotoImage(file="assets/background.png")
# original_bg_flipped = tk.PhotoImage(file="assets/background_flipped.png")

original_bg = Image.open("assets/background.png")
original_bg_flipped = Image.open("assets/background_flipped.png")

original_bg = original_bg.resize((original_bg.width, HEIGHT))
original_bg_flipped = original_bg_flipped.resize((original_bg_flipped.width, HEIGHT))

BACKGROUND_WIDTH = original_bg.width

bg = ImageTk.PhotoImage(original_bg)
bg_flipped = ImageTk.PhotoImage(original_bg_flipped)

# Create the background
BACKGROUND_LIST.append(canvas.create_image(0, 0, anchor="nw", image=bg))
BACKGROUND_LIST.append(
    canvas.create_image(bg.width(), 0, anchor="nw", image=bg_flipped)
)

gameIsRunning = True

happyUp = Image.open("assets/happyUp.png")
happyDown = Image.open("assets/happyDown.png")
happyFalling = Image.open("assets/happyFalling.png")
happyUp = happyUp.resize((80, 50))
happyDown = happyDown.resize((80, 50))
happyFalling = happyFalling.resize((80, 50))
happyUp = ImageTk.PhotoImage(happyUp)
happyDown = ImageTk.PhotoImage(happyDown)
happyFalling = ImageTk.PhotoImage(happyFalling)

happy = canvas.create_image(100, HEIGHT / 2, anchor="center", image=happyUp)

coordsOfHappy = canvas.bbox(happy)


def moveCircle():
    if not gameIsRunning:
        return

    coordsOfHappy = canvas.bbox(happy)
    # print(coordsOfCircle)

    # Gravity
    global happyVelocity
    happyVelocity += GRAVITY

    canvas.move(
        happy, 0, happyVelocity
    )  # Move the circle right by 0 and down by 1 pixel : Simulating gravity

    if coordsOfHappy[3] > HEIGHT or coordsOfHappy[1] < 0:
        gameOver()
        return

    # coordsOfCircle[0] is left, coordsOfCircle[1] is top, coordsOfCircle[2] is right, coordsOfCircle[3] is bottom
    # coords[0] is left, coords[1] is top, coords[2] is right, coords[3] is bottom

    for pipe in listOfPipes:  # pipe = [top_pipe, bottom_pipe]
        top_pipe_coords = canvas.coords(pipe[0])
        bottom_pipe_coords = canvas.coords(pipe[1])
        point_given = pipe[2]

        if point_given == False and coordsOfHappy[0] > top_pipe_coords[2]:
            pipe[2] = True
            updateScoreCount()

        # Checks if the left side of the bird is to the left of the right side of the top pipe.
        # Checks if the right side of the bird is to the right of the left side of the top pipe
        # Checks if the bottom of the bird is below the bottom side of the top pipe.
        # Checks if the top side of bird is above the bottom side of the top pipe.
        if (
            coordsOfHappy[0] < top_pipe_coords[2]
            and coordsOfHappy[2] > top_pipe_coords[0]
            and coordsOfHappy[1] < top_pipe_coords[3]
            and coordsOfHappy[3] > top_pipe_coords[1]
        ) or (
            coordsOfHappy[0] < bottom_pipe_coords[2]
            and coordsOfHappy[2] > bottom_pipe_coords[0]
            and coordsOfHappy[1] < bottom_pipe_coords[3]
            and coordsOfHappy[3] > bottom_pipe_coords[1]
        ):
            canvas.itemconfig(happy, image=happyFalling)
            gameOver()
            return
    root.after(20, moveCircle)


# Create the pipes
listOfPipes = []  # List of all the pipes


def spawnNewPipe(xOfPipe, widthOfPipe, gapPosition, gapOfPipe, bottomOfTheTopPipe):
    top_pipe = canvas.create_rectangle(
        xOfPipe, 0, xOfPipe + widthOfPipe, gapPosition, fill="darkgreen"
    )
    bottom_pipe = canvas.create_rectangle(
        xOfPipe,
        gapPosition + gapOfPipe,
        xOfPipe + widthOfPipe,
        HEIGHT,
        fill="darkgreen",
    )
    listOfPipes.append([top_pipe, bottom_pipe, False])


xOfPipe = 800
widthOfPipe = 50
gapOfPipe = 120
gapPosition = HEIGHT / 2 - gapOfPipe / 2
bottomOfTheTopPipe = 500
gapBetweenPipesHorizontally = 300


def movePipes():
    if not gameIsRunning:
        return

    canvas.tag_raise(score_text)

    global gapPosition
    gapPosition = random.randint(int(gapOfPipe * 0.5), int(HEIGHT - gapOfPipe * 1.5))
    if len(listOfPipes) == 0:
        spawnNewPipe(xOfPipe, widthOfPipe, gapPosition, gapOfPipe, bottomOfTheTopPipe)
    elif canvas.coords(listOfPipes[-1][0])[0] < WIDTH - gapBetweenPipesHorizontally:
        spawnNewPipe(xOfPipe, widthOfPipe, gapPosition, gapOfPipe, bottomOfTheTopPipe)

    listOfPipesCopy = listOfPipes.copy()
    for pipe in listOfPipesCopy:
        if canvas.coords(pipe[0])[2] < 0:
            canvas.delete(pipe[0])
            canvas.delete(pipe[1])
            if pipe in listOfPipes:
                listOfPipes.remove(pipe)
        else:
            canvas.move(pipe[0], -1, 0)
            canvas.move(pipe[1], -1, 0)
    root.after(10, movePipes)


def moveBackground():
    if not gameIsRunning:
        return
    for background in BACKGROUND_LIST:
        canvas.move(
            background, -BACKGROUND_SPEED, 0
        )  # Moves canvas horizontally to the left by subtracting the x coordinate

        bg_coords = canvas.bbox(background)  # Retrieves background coordinates

        if bg_coords[2] <= 0:  # Checks if the background image is set to the left edge
            canvas.moveto(
                background, BACKGROUND_WIDTH, 0
            )  # Moves background horizontally right
            print("Background moved to the right edge")
    root.after(20, moveBackground)


def game_over_animation():
    global happyVelocity
    global gameIsRunning
    if gameIsRunning:
        return
    if canvas.coords(happy)[1] < HEIGHT:  # If happy is not at the bottom of the screen
        happyVelocity += GRAVITY
        canvas.move(happy, 0, happyVelocity)
        root.after(20, game_over_animation)


def gameOver():
    global gameIsRunning
    gameIsRunning = False
    game_over_text = canvas.create_text(
        400, 350, text="GAME OVER", fill="red", font=("Impact", 50)
    )
    game_over_animation()

    def game_over_btn_click():
        global score
        score = 0
        canvas.itemconfig(score_text, text="Score: " + str(score))
        global gameIsRunning
        global happyVelocity

        gameIsRunning = True

        for pipe in listOfPipes:
            canvas.delete(pipe[0])
            canvas.delete(pipe[1])
        listOfPipes.clear()

        happyVelocity = 0
        canvas.moveto(happy, 100, HEIGHT / 2)
        canvas.itemconfig(happy, image=happyUp)

        canvas.delete(game_over_text)
        game_over_btn.destroy()

        startGame()

    # create a button
    game_over_btn = tk.Button(
        canvas,
        width=20,
        height=2,
        text="Play Again",
        bd="5",
        padx=0,
        pady=0,
        command=game_over_btn_click,
    )
    game_over_btn_window = canvas.create_window(
        WIDTH / 2, HEIGHT / 1.8, anchor="center", window=game_over_btn
    )


score = 0
score_text = canvas.create_text(
    400, 50, text="Score: " + str(score), fill="white", font=("Impact", 30)
)


def updateScoreCount():
    global score
    score += 1
    canvas.itemconfig(score_text, text="Score: " + str(score))


def startGame():
    moveCircle()
    moveBackground()
    movePipes()


once = True


def btn_click():
    startGame()
    btn.destroy()


# Create a Button
btn = tk.Button(
    canvas,
    width=20,
    height=5,
    text="Start",
    bd="5",
    padx=0,
    pady=0,
    font="Impact",
    command=btn_click,
)
btn_window = canvas.create_window(WIDTH / 2, HEIGHT / 1.8, anchor="center", window=btn)


root.mainloop()
