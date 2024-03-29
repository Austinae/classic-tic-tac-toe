import sys, pygame
from test import *
import random

pygame.init()

size = width, height = 500, 500
white = 255, 255, 255
black = 0, 0, 0

screen = pygame.display.set_mode(size)

gameRunning = True

circleSize = 60
thickness = 5

thirdwidth = width/3
thirdheight = height/3

centerx = int(thirdwidth/2)
centery = int(thirdheight/2)

cross_offset = 30

circles = []
crosses = []

player1 = "circle"
player2 = "cross"

player1score = 0
player2score = 0

player = player1

# label to show score
font = pygame.font.Font(None, 30)
scoretext = font.render("P1 (O):" + str(player1score)+"   P2 (X):" + str(player2score), 1, black)

class Circle:
    def __init__(self, surface, color, center, radius, width):
        self.surface = surface
        self.color = color
        self.center = center
        self.radius = radius
        self.width = width

    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.center, self.radius, self.width)


class Cross:
    def __init__(self, surface, color, x, y, width):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.lines = []
        self.length = 100

    def draw(self):
        pygame.draw.line(self.surface, self.color, (self.x, self.y), (self.x + self.length, self.y + self.length), thickness)
        pygame.draw.line(self.surface, self.color, (self.x + self.length, self.y), (self.x, self.y + self.length), thickness)


class Board:
    def __init__(self):
        self.board = {(0, 0): None, (0, 1): None, (0, 2): None, (1, 0): None, (1, 1): None, (1, 2): None, (2, 0): None, (2, 1): None, (2, 2): None}

    def isMoveValid(self, x, y):
        for square in self.board:
            if square[0] == x and square[1] == y and self.board[(x, y)] is None:
                return True
        return False

    def move(self, x, y, player):
        self.board[(x, y)] = player

    def isWinner(self):
        squares = []
        # check vertical squares
        for i in range(3):
            for j in range(3):
                squares.append(self.board[(i, j)])
            if len(set(squares)) == 1:
                if squares[0] is not None:
                    return True
            squares = []
        # check horizontal squares
        for i in range(3):
            for j in range(3):
                squares.append(self.board[(j, i)])
            if len(set(squares)) == 1:
                if squares[0] is not None:
                    return True
            squares = []
        # check diagonal squares
        # top left bottom right
        for i in range(3):
            squares.append(self.board[(i, i)])
        if len(set(squares)) == 1:
            if squares[0] is not None:
                return True
        squares = []
        # bottom left top right
        j = 2
        for i in range(3):
            squares.append(self.board[(i, j)])
            j -= 1
        if len(set(squares)) == 1:
            if squares[0] is not None:
                return True
        return False


    def empty(self):
        self.board = {(0, 0): None, (0, 1): None, (0, 2): None, (1, 0): None, (1, 1): None, (1, 2): None, (2, 0): None, (2, 1): None, (2, 2): None}


def drawObjects(circles, crosses):
    # this is the board
    pygame.draw.rect(screen, black, (thirdwidth, 0, thickness, height))
    pygame.draw.rect(screen, black, (thirdwidth*2, 0, thickness, height))
    pygame.draw.rect(screen, black, (0, thirdheight, width, thickness))
    pygame.draw.rect(screen, black, (0, thirdheight*2, width, thickness))
    for circle in circles:
        circle.draw()
    for cross in crosses:
        cross.draw()

board = Board()

def buttonDownLogic(board, player, circles, crosses, player1score, player2score, scoretext):
    x, y = pygame.mouse.get_pos()
    w = 0
    z = 0
    if x // int(thirdwidth) == 0:
        w = 0
        x = 1
    else:
        w = x // int(thirdwidth)
        x = (x // int(thirdwidth)) * 2 + 1

    if y // int(thirdheight) == 0:
        z = 0
        y = 1
    else:
        z = y // int(thirdheight)
        y = (y // int(thirdheight)) * 2 + 1

    if board.isMoveValid(w, z):
        if player == player1:
            circles.append(Circle(screen, black, (centerx * x, centery * y), circleSize, thickness))
        else:
            crosses.append(
                Cross(screen, black, w * int(width / 3) + cross_offset, z * int(height / 3) + cross_offset, thickness))
        board.move(w, z, player)
        if board.isWinner():
            print(player, "is the winner")
            if player == player1:
                player1score += 1
            else:
                player2score += 1
            scoretext = font.render("P1 (O):" + str(player1score) + "   P2 (X):" + str(player2score), 1, black)
            board.empty()
            circles = []
            crosses = []
        elif None not in board.board.values():
            print("It is a draw")
            board.empty()
            circles = []
            crosses = []
        if player == player1:
            player = player2
        else:
            player = player1
    return board, player, circles, crosses, player1score, player2score, scoretext


if __name__ == '__main__':
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player == player1:
                    board, player, circles, crosses, player1score, player2score, scoretext = buttonDownLogic(board, player, circles, crosses, player1score, player2score, scoretext)

        # random bot moves
        if player == player2:
            options = []
            for square in board.board:
                if board.board[square] is None:
                    options.append(square)
            botMove = random.choice(options)
            board.move(botMove[0], botMove[1], player)
            crosses.append(
                Cross(screen, black, botMove[0] * int(width / 3) + cross_offset, botMove[1] * int(height / 3) + cross_offset, thickness))
            if board.isWinner():
                print(player, "is the winner")
                if player == player1:
                    player1score += 1
                else:
                    player2score += 1
                scoretext = font.render("P1 (O):" + str(player1score) + "   P2 (X):" + str(player2score), 1,
                                        black)
                board.empty()
                circles = []
                crosses = []
            elif None not in board.board.values():
                print("It is a draw")
                board.empty()
                circles = []
                crosses = []
            player = player1

        screen.fill(white)
        drawObjects(circles, crosses)
        screen.blit(scoretext, (0, 0))

        pygame.display.flip()
