from turtle import *
from Marble import *
from Point import *
import random

colors = ["red", "blue", "green", "yellow", "purple", "black"]

class Game:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.screen = turtle.Screen()
        self.secret = self.secret_code()
        print(self.secret)
        # onlcick function already gives back an x and y
        # create a function that handles click in the game
        # self.screen.onclick(Marble.handle_click)
        self.screen.onclick(self.handle_click)
        self.screen.screensize(970,635)
        self.screen.tracer(10)
        # self.turtle.speed(0)
        # this is track the instances of the play side marbles
        self.data_pmarbles = []
        # this is to track the instances of the status marbles
        self.data_smarbles = []
        # this is to track the clicked marbles from the play side
        self.track_marble = []
        # this is a list to track buttons
        self.track_button = []
        # this is to get the player name
        self.player_name = ''
        self.winners = ''
        self.row = 0
        self.index = 0
        self.board()
        
    def handle_click(self, x, y):
        '''
        This funtion is going to take all the clicks that are heard from the 
        onlick function in the __init__, the parameters are only x and y
        The parameters are going to be pass in to another function such as 
        marble_click that returns true if the x and y matches one of the
        marble instances from self.data_pmarbles

        This function is going to have 3 sub functions in it
        1 check where we are clicking with getclick
        2 if marble is clicked
        3 if button is clicked
        '''
        self.getclick(x, y)

        self.marble_click(x, y)

        if self.quit(x, y):
            turtle.register_shape("quitmsg.gif")
            self.turtle.shape("quitmsg.gif")
            self.turtle.goto(0, 0)
            self.turtle.stamp()
            turtle.exitonclick()
        
        if self.delete(x, y):
            print('pressed on delete')
            self.index = 0
            print(self.index)
            self.status_fill_empty(self.row)
            self.playside_marbles_empty()
            self.data_pmarbles.clear()
            self.playside_marbles()
            self.track_marble.clear()

        if len(self.track_marble) == 4:
            if self.check(x, y):
                # once the check button is pressed check for bull and cows
                bulls, cows = self.compare(self.secret, self.track_marble)
                self.set_pegs(bulls, cows)
                if self.win(bulls):
                    self.write_leader(self.player_name, self.row + 1) 
                    turtle.register_shape("winner.gif")
                    self.turtle.shape("winner.gif")
                    self.turtle.goto(0, 0)
                    self.turtle.stamp()
                    turtle.exitonclick()
                    return
                else:
                    print(f'Round: {self.row + 1} Bulls: {bulls}, Cows: {cows}')
                    self.row += 1
                    if self.row == 10:
                        self.check_lose()
                    else:
                        self.index = 0
                        self.playside_marbles_empty()
                        self.data_pmarbles.clear()
                        self.playside_marbles()
                        self.track_marble.clear()
                    
    def check_lose(self):
        '''
        This function checks if the row is equal to 11 is it is then the secret
        code will be revealed and an image will pop up and the turtle will
        close in 15 seconds
        '''
        string_secret = " ".join(self.secret)
        turtle.register_shape("Lose.gif")
        self.turtle.shape("Lose.gif")
        self.turtle.goto(197.0, 68.0)
        self.turtle.stamp()
        turtle.textinput("Secret Code", string_secret)
        turtle.exitonclick()
        
    def quit(self, x ,y):
        '''
        Make a button that returns true if pressed on, ultimately this 
        function will be use to quit the turtle by using the turtle.bye()
        '''
        if self.track_button[2].clicked_in_region(x, y):
            return True

    def status_fill_empty(self, row):
        '''
        This function is going to parameters row, index. 
        The whole row of status marbles are going to be turned empty.
        We are always going to start at 0 every game. 
        If the index reaches 4 this function render useless untill down in the
        index is reset
        '''
        current_row = self.data_smarbles[row]
        print(len(current_row)- 1)
        for i in range(len(current_row) - 1):
            marble = current_row[i]
            marble.draw_empty()

    def status_fill(self, color, row, index):
        '''
        This function is going to parameters color, row, index. 
        Color is going to turn the current row, and index of the row into the
        given color.
        We are always going to start at 0 every game. 
        If the index reaches 4 this function render useless untill down in the
        run_game we reset the index to 0 and 1 one to the row to start filling
        out marbles again.
        '''
        current_marble = self.data_smarbles[row][index]
        if index <= 4:
            current_marble.set_color(color)
            current_marble.draw()
            self.index += 1

    def marble_click(self, x, y):
        '''
        This function is going to take in an x and y from the handle click
        function then we are going to pass in those x and y into the 
        clicked_in_region method from the marble class
        If the clicked_in_region returns true then we 
        if the color is not in the track_marble list and if the track_marble
        list has less than 4 indexes only then will we append the current
        marble color to track_marble list
        '''
        for i in range(len(self.data_pmarbles)):

            # current marble
            marble = self.data_pmarbles

            # short hand to access track marble list
            track = self.track_marble

            # check if we clicked in a marble
            if marble[i].clicked_in_region(x, y):
                # current marble color
                color = marble[i].get_color()

                if color not in track and len(track) < 4:
                    color = marble[i].color
                    self.track_marble.append(color)
                    marble[i].draw_empty()
                    print(f'Clicked in {color}')
                    print(self.track_marble)
                    self.status_fill(color, self.row, self.index)

    def delete(self, x, y):
        '''
        In this function we are going to pass in an x and y from the 
        handle and this function will return true if coordinates are
        pressed and false if it isnt pressed
        '''
        if self.track_button[1].clicked_in_region(x, y):
            return True
    
    def check(self, x, y):
        '''
        In this function we are going to pass in an x and y from the 
        handle and this function checks if the check mark button is
        pressed on or not.
        If it is pressed then return true
        '''
        if self.track_button[0].clicked_in_region(x, y):
            return True
        
    def set_pegs(self, bulls, cows):
        '''
        This function will set the pegs and it takes in 2 params bulls, and
        cows. The data we are accessing is from self.data_smarble for example
        first row of status marbles the 
        top left peg would be data_smarbles[0][4][0] 
        top right peg would be data_smarbles[0][4][1] 
        bottom left peg would be data_smarbles[0][4][2] 
        bottom right peg would be data_smarbles[0][4][3]
        '''
        # variabl for row of pegs
        peg_row = self.data_smarbles[self.row][4]
        # print(len(f'How many rows:{peg_row}'))
        # go iterate over the b_c marble (pegs) for the given row number
        for i in range(len(peg_row)):
            single_peg = peg_row[i]
            if bulls != 0:
                single_peg.set_color('black')
                single_peg.draw()
                bulls -= 1
            elif cows != 0:
                single_peg.set_color('red')
                single_peg.draw()
                cows -= 1
        print(f'setting pegs finished')

    def getclick(self, x, y):
        '''
        Lets me know where I am clicking on the screen
        '''
        print("I caught you clicking at ({}, {})!".format(x, y))


    def board(self):
        '''
        In this function we are going to draw the whole board starting with
        the status board then teleport down to the bottom to draw the play board,
        then teleport to the left to draw the leader board.
        Finally the buttons will be made and each button will have a gif stamped
        over them because underneath the gifs are instances of marble so that I
        can access the clicked_in_region method
        '''
        self.player_name = turtle.textinput("Text Input", "Enter Name:")
        # draw the status board
        self.turtle.penup()
        self.turtle.goto(-345, 325)
        self.turtle.pendown()
        self.turtle.width(10)
        self.turtle.color('blue')
        self.turtle.forward(400)
        self.turtle.left(-90)
        self.turtle.forward(500)
        self.turtle.left(-90)
        self.turtle.forward(400)
        self.turtle.left(-90)
        self.turtle.forward(500)
        self.turtle.left(-90)

        # draw the play board
        self.turtle.penup()
        self.turtle.goto(-345, -190)
        self.turtle.pendown()
        self.turtle.width(10)
        self.turtle.color('blue')
        self.turtle.forward(680)
        self.turtle.left(-90)
        self.turtle.forward(120)
        self.turtle.left(-90)
        self.turtle.forward(680)
        self.turtle.left(-90)
        self.turtle.forward(120)
        self.turtle.left(-90)
    
        # draw the leader board
        self.read_file()
        self.turtle.penup()
        self.screen.title("Master Mind")
        self.turtle.goto(90, 300)
        self.turtle.pendown()
        self.turtle.write("Leader Board",font=("Arial", 16, "normal"))
        self.turtle.penup()
        
        self.turtle.penup()
        self.turtle.goto(70, 325)
        self.turtle.pendown()
        self.turtle.width(10)
        self.turtle.color('blue')
        self.turtle.forward(260)
        self.turtle.left(-90)
        self.turtle.forward(500)
        self.turtle.left(-90)
        self.turtle.forward(260)
        self.turtle.left(-90)
        self.turtle.forward(500)
        self.turtle.left(-90)
        self.turtle.penup()

        self.turtle.goto(90, 150)
        self.turtle.setheading(-90)
        self.turtle.pendown()
        self.turtle.write(self.winners, align="left", font=("Arial", 16, "normal"))
        self.turtle.penup()
        
        # draw the playside marbles
        self.playside_marbles()

        # draw the status marbles
        self.status_board()

        turtle.register_shape("checkbutton.gif")
        turtle.register_shape("xbutton.gif")
        turtle.register_shape("quit.gif")
        
        # check button
        self.buttons(90, -265, 'green')
        self.turtle.shape("checkbutton.gif")
        self.turtle.goto(90, -265)
        self.turtle.stamp()
        
        # delete button
        self.buttons(150, -265, 'red')
        self.turtle.shape("xbutton.gif")
        self.turtle.goto(150, -265)
        self.turtle.stamp()
        
        # quit button
        self.buttons(270, -265, 'red')
        self.turtle.shape("quit.gif")
        self.turtle.goto(270, -255)
        self.turtle.stamp()

        self.turtle.hideturtle()
        
    def read_file(self):
        '''
        This function will read a file and save it as string so we can
        add it to the leaer board
        This function will also try to read a file, if that file is not
        found then it will append to the error log about the error
        also if the error log is not there then it will also create a new
        error_log.txt
        Finally it will make a new leaderboard.txt if there isn't one then
        it will display the leaderboard_error.gif if a new leaderboard.txt
        was just created.
        '''
        try:
            with open('leaderboard.txt', 'r') as infile:
                self.winners = infile.read()
                
        except FileNotFoundError as error:

            with open('error_log.txt', 'a') as file:
                file.write(f"Could not find file: {error}")
            
            turtle.register_shape("leaderboard_error.gif")
            self.turtle.shape("leaderboard_error.gif")
            self.turtle.penup()
            self.turtle.goto(190.0, 250.0)
            self.turtle.stamp()
            with open('leaderboard.txt', 'w') as new_file:
                pass 

    def buttons(self, x, y, color):
        '''
        This function is where we are going to make buttons of check
        delete and quit
        This function takes in an x and y coord and every button is going to
        be an instance of the marble class to utilize the clicked_in_region
        '''
        button = Marble(Point(x, y), color)
        button.draw()
        self.track_button.append(button)

    def playside_gifs(self, x, y):
        '''
        This function will add the gifs from the local directory
        It will take in 3 parameters position x and y and 
        the absolute file name.
        '''
        # should start implementing gifs over here
        # self.screen.addshape(checkPath)
        self.turtle.shape(checkPath)
        self.turtle.goto(x, y)

    def playside_marbles_empty(self):
        '''
        This function tsets all the play side marbles to white and redraws them
        white. Goes over the length of the data_pmarbles and draws them empty
        '''
        for i in range(len(self.data_pmarbles)):
            marble = self.data_pmarbles[i]
            marble.draw_empty()

    def playside_marbles(self):
        '''
        This function will draw 6 marbles at the bottone where the play is
        starting the coordinate for the play board starts at (-310, -265)
        for references
        When we make each marble we are going to space each other 60 away
        '''
        # this coordinate is going to be same for the whole row
        Y_CORD = -265
        # this x coordinate is going change
        x_cord = -300
        # need a for loop to draw 6 marbles 
        # within each loop add 60 to the x and change the colors
        for i in range(6):
            single_marble = Marble(Point(x_cord, Y_CORD), colors[i])  
            # we need to keep track of the instances of the play side marbles
            self.data_pmarbles.append(single_marble)
            single_marble.draw()
            x_cord += 60

    def status_board(self):
        '''
        This function will drow out four empty marbles that colors will be
        filled in to and 4 marbles on the side that will represent the bulls
        and cows
        This function will also make all 10 rows
        '''
        # these x and y start from the first marble from the row up top 
        # only y is gonna change becuase we have to change each row
        y_cord = 270
        # x is going to be a constant only for this function
        X_CORD = -300

        for i in range(10):
            self.status_marbles(X_CORD, y_cord)
            y_cord -= 48

    def status_marbles(self, x, y):
        '''
        This function only makes the status marbles for one row and there
        are 4 marbles in one row then after making the four marble it will
        make the bulls and cows marble to the right of it.
        '''
        row = []
        b_c_row = []
        # making the 4 marlbes that will light up
        for i in range(4):
            single_marble = Marble(Point(x, y), 'white', 20)
            row.append(single_marble)
            single_marble.draw_empty()
            x += 60
        # bulls and cows y coordinate
        bc_y = y + 26
        # now make 2 rows of bulls and cows marbles
        for f in range(2):
            # variable to append bulls and cows marble instances
            data_bc = self.b_c_marbles(x, bc_y)
            b_c_row.extend(data_bc)
            bc_y -= 15
        row.append(b_c_row)
        self.data_smarbles.append(row)

    def b_c_marbles(self, x, y):
        '''
        AKA bulls and cows marbles
        This function is going to be used in the status board, and the sole
        purpose is to only draw out 2 marbles

        This funtion also takes in 2 parameters x and y that are passed in 
        status_board

        This function is going to return a list that we will append to row in
        the function status marbles.
        '''
        # data of 2 bulls and cows marbles
        twobc = []

        # we are going to make the top row of the 2x2 first
        for i in range(2):
            b_c_marble = Marble(Point(x, y), 'white', 5)
            twobc.append(b_c_marble)
            b_c_marble.draw_empty()
            x += 15
        return twobc

    def secret_code(self):
        '''
        In this function we are going to make a randomized sequence of 4 
        colors nad there can be no repeats. Returns an array of 4 colors.
        '''
        return random.sample(colors, 4)

    def user_choice(self):
        '''
        This function is where I want the user to input their choices via 
        terminal, so in the program the user inputs 4 choices and then it,
        will be compile into an array for comparison later
        '''
        userChoices = []

        # allow the user to make inputs 1 through 4
        for i in range(4):
            choice = input(f"Enter choice {i + 1} of 4: ").lower()
            userChoices.append(choice)

        return userChoices
    
    def compare(self, secret, user):
        '''
        This function also takes to parameters that are lists, secret from
        secret_code and user from user_choice which is also another list.

        This function is where I want to compare the users choice with the
        secret code, if user choice matches secret code in the same position
        then in the bull counter add 1. If no bulls but there was a matching
        color not in the same position add 1 to the cow counter.

        This function should return 2 numbers under the names of bull and cow
        '''
        # list of bulls and cows
        bulls = 0
        cows = 0
        # iterate over user choices 
            # if current user choice is the same position as secret
                # bull add 1 
            #else if user choice is in secret 
                # cow add 1 
        for i in range(len(user)):
            if user[i] == secret[i]:
                bulls += 1 
            elif user[i] in secret:
                cows += 1 

        return bulls, cows

    def win(self, bull):
        '''
        This function takes in 1 paramenter which are numbers, and they
        come from the compare funtion.
        If bull is equal to 4 then you win the game if no then keep playing
        This function is going to be used for another function that will keep
        the game going is false
        '''
        if bull == 4:
            return True
        else:
            return False
    
    def write_leader(self, name, rounds):
        '''
        This function takes in 2 parameters which is an input that is already
        in string form. If there isn't a file name with leader board then this
        function automatically writes and appends names of the names of the
        winners.
        '''
        rounds = str(rounds)
        with open('leaderboard.txt', 'a') as file:
            file.write(f'{name}:  Rounds {rounds}\n')
            print('File appended successfully!')

    def logic_game(self):
        '''
        This is only the logic part of the game some think of playing this
        via only terminal!

        In this game its going to be 10 rounds so every round that isnt won
        we will go up until the 10th round.

        '''

        # get the secret code
        secret_code = self.secret
        print(secret_code)

        # start round with while loop that is less tha 10 because 10 rounds
            # get user input
            # compare user input with secret code 
            # check if game is won or nah
                # if gmae isnt won print the amount of bulls and cows
                # make a text file and allow winner to write their name 
        # once the loop ends and game ins't won break out of the function
        # print you lose or something

        for i in range(10):
            user_choice = self.user_choice()
            bulls, cows = self.compare(secret_code, user_choice)
            if self.win(bulls):
                # leader board function
                print('YOU WON')
                winner_name = input('Enter your name: ')
                self.write_leader(winner_name, i + 1 )
                return
            else:
                print(f'Round: {i + 1} Bulls: {bulls}, Cows: {cows}')
        
        print(f'You Lose!, The secret code was {secret_code}')
        return

def main():
    new_game = Game()
    print(new_game.winners)
    turtle.done()

if __name__ == "__main__":
    main()
