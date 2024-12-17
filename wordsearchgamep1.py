import string
import random
import tkinter as tk
from tkinter import messagebox

# Configuration Data
config_data = {
    'levels': {
        1: {'name': 'Mini', 'words': 5},
        2: {'name': 'Normal', 'words': 10},
        3: {'name': 'Pro', 'words': 10},
        4: {'name': 'Pro Max', 'words': 20}
    },
    'player': {
        'level': 3,
        'name': 'Player',
        'score': 0
    }
}

# Global Variables
wordPressed = ''
previous = [0, 0]
route = [0, 0]

class Square:
    def __init__(self):
        self.status = False
        self.filled = False
        self.char = ''

def gameHeader(root, timerVar):
    game_header = tk.Frame(root)
    game_header.pack(fill=tk.X, side=tk.TOP)

    heading = tk.Label(game_header, text='Word Search Game', font=('Helvetica', 23, 'bold'), fg='blue')
    heading.pack(expand=True, fill=tk.X, pady=12)

    timer_label = tk.Label(game_header, text="Time Left: ", font=('Helvetica', 12, 'bold'))
    timer_label.pack(side=tk.LEFT, padx=10)
    timer_display = tk.Label(game_header, textvariable=timerVar, font=('Helvetica', 12, 'bold'), fg='red')
    timer_display.pack(side=tk.LEFT)

def gameFooter(root):
    game_footer = tk.Frame(root)
    game_footer.pack(fill=tk.X, side=tk.BOTTOM, pady=12)

    footer = tk.Label(game_footer, text='(C)2024')
    footer.pack(expand=True, fill=tk.X, pady=0)

def startGame(root, levelNum, size, numWords):
    frame1 = tk.Frame(master=root, bg="red")
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=20, pady=12)

    frame2 = tk.Frame(master=root)
    frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=12)

    frame3 = tk.Frame(master=root)
    frame3.pack(fill=tk.BOTH, side=tk.RIGHT, padx=20, pady=30)

    currScore = tk.StringVar()
    currScore.set(0)

    wordList = random.sample(
        ['HELLO', 'WORLD', 'PYTHON', 'TKINTER', 'GAME', 'JAVA', 'SEARCH', 'COMPUTER', 'ALGORITHM', 'CODING'],
        numWords
    )
    foundWords = set()

    arr = [[Square() for _ in range(size)] for _ in range(size)]
    button = [[None for _ in range(size)] for _ in range(size)]
    directionArr = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

    timerVar = tk.StringVar()
    timerVar.set("30")

    def startTimer():
        time_left = int(timerVar.get())
        if time_left > 0:
            timerVar.set(str(time_left - 1))
            root.after(1000, startTimer)  # Call startTimer again after 1 second
        else:
            endGame()  # End the game when the timer reaches 0

    def endGame():
        messagebox.showinfo("Time's Up!", f"Time's up! Your final score: {config_data['player']['score']}")
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            root.destroy()
            main()
        else:
            root.quit()

    tk.Label(master=frame3, text="Score:", font=('Helvetica', 12, 'bold')).grid(row=0, column=0)
    tk.Label(master=frame3, textvariable=currScore, font=('Helvetica', 12, 'bold')).grid(row=0, column=1)

    def fill(x, y, word, direction):
        for i in range(len(word)):
            arr[x + direction[0] * i][y + direction[1] * i].char = word[i]
            arr[x + direction[0] * i][y + direction[1] * i].filled = True

    def wordPlace(word):
        placed = False
        attempts = 100
        while not placed and attempts > 0:
            x = random.randrange(0, size)
            y = random.randrange(0, size)
            direction = random.choice(directionArr)

            # Check boundaries
            if (x + len(word) * direction[0] > size - 1 or x + len(word) * direction[0] < 0 or
                y + len(word) * direction[1] > size - 1 or y + len(word) * direction[1] < 0):
                attempts -= 1
                continue

            # Check for conflicts
            conflict = False
            for i in range(len(word)):
                nx, ny = x + direction[0] * i, y + direction[1] * i
                if arr[nx][ny].filled and arr[nx][ny].char != word[i]:
                    conflict = True
                    break

            if not conflict:
                fill(x, y, word, direction)
                placed = True

        return placed

    def checkWord():
        global wordPressed
        if wordPressed in wordList and wordPressed not in foundWords:
            foundWords.add(wordPressed)
            config_data['player']['score'] += 1
            currScore.set(config_data['player']['score'])
        wordPressed = ''
        previous[0] = 0
        previous[1] = 0
        updateWordListDisplay()

    def updateWordListDisplay():
        for widget in frame2.winfo_children():
            widget.destroy()

        tk.Label(frame2, text="Words to Find:", font=('Helvetica', 12, 'bold')).grid(row=0)
        for idx, word in enumerate(wordList):
            color = 'green' if word in foundWords else 'black'
            tk.Label(frame2, text=word, font=('Helvetica', 12), fg=color).grid(row=idx + 1)

        tk.Button(frame2, text="Check Word", height=1, width=15, anchor='c', bg="#70889c", font=('Helvetica', 10),
                  fg='white', command=checkWord).grid(row=len(wordList) + 1, pady=(10, 0))

    def buttonPress(x, y):
        global wordPressed, previous, route
        newPressed = [x, y]

        if len(wordPressed) == 0:
            previous = newPressed
            wordPressed = arr[x][y].char
            button[x][y].configure(bg='yellow', fg='#255059')
        elif len(wordPressed) == 1 and abs(x - previous[0]) <= 1 and abs(y - previous[1]) <= 1 and newPressed != previous:
            wordPressed += arr[x][y].char
            button[x][y].configure(bg='yellow', fg='#255059')
            route = [x - previous[0], y - previous[1]]
            previous = [x, y]
        elif len(wordPressed) > 1 and x - previous[0] == route[0] and y - previous[1] == route[1]:
            wordPressed += arr[x][y].char
            button[x][y].configure(bg='yellow', fg='#255059')
            previous = [x, y]

    for word in wordList:
        wordPlace(word)

    for x in range(size):
        for y in range(size):
            if not arr[x][y].filled:
                arr[x][y].char = random.choice(string.ascii_uppercase)
            button[x][y] = tk.Button(frame1, text=arr[x][y].char, bg='#255059', fg='white', width=4, height=2,
                                     relief=tk.FLAT, command=lambda x=x, y=y: buttonPress(x, y))
            button[x][y].grid(row=x, column=y)

    updateWordListDisplay()
    startTimer()

def main():
    root = tk.Tk()
    root.title("Word Search Game")

    timerVar = tk.StringVar()
    timerVar.set("30")  # Initialize the timer to 30 seconds

    gameHeader(root, timerVar)

    size = 8
    levelNum = 3
    numWords = config_data['levels'][levelNum]['words']

    startGame(root, levelNum, size, numWords)
    gameFooter(root)
    root.mainloop()

if __name__ == '__main__':
    main()
