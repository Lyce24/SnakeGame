from tkinter import *
from Game import Game, Agent
from geometry import Point2D, Vector2D
import math
import random
import time


class Bonus(Agent):
    WIDTH = 1.0
    LENGTH = 1.0

    def __init__(self, world, snake):
        self.length = self.LENGTH
        self.width = self.WIDTH
        xoffset = random.uniform(-0.8, 0.4)
        yoffset = random.uniform(-0.8, 0.8)
        self.snake = snake
        self.world = world
        position = world.bounds.point_at((xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        Agent.__init__(self, position, world)

    def color(self):
        return "#B0ABA8"

    def shape(self):
        p1 = self.position + Vector2D(self.width / 2.0, self.length / 2.0)
        p2 = self.position + Vector2D(-self.width / 2.0, self.length / 2.0)
        p3 = self.position + Vector2D(-self.width / 2.0, -self.length / 2.0)
        p4 = self.position + Vector2D(self.width / 2.0, -self.length / 2.0)
        return [p1, p2, p3, p4]

    def update(self):
        if ((self.position.x - self.snake.position.x) ** 2 + (
                self.position.y - self.snake.position.y) ** 2) ** 0.5 < 0.8:
            new_position = self.world.bounds.point_at((random.uniform(-0.7, 0.4) + 1.0) / 2.0,
                                                      (random.uniform(-0.6, 0.6) + 1.0) / 2.0)
            self.position = new_position
            self.position = Point2D(new_position.x, new_position.y)
            self.world.score += 1
            self.world.snake.speed += 0.005
            if not self.world.followers:
                self.world.followers.append(Followers(self.world, self.world.snake))
                self.world.followers.append(Followers(self.world, self.world.followers[-1]))
                self.world.followers.append(Followers(self.world, self.world.followers[-1]))
            else:
                self.world.followers.append(Followers(self.world, self.world.followers[-1]))
                self.world.followers.append(Followers(self.world, self.world.followers[-1]))
                self.world.followers.append(Followers(self.world, self.world.followers[-1]))


class Snake(Agent):
    START_X = -0.8
    START_Y = 0.8

    def __init__(self, world):
        self.world = world
        self.speed = 0.3
        xoffset = self.START_X
        yoffset = self.START_Y
        self.towards = None
        self.dx = 0
        self.dy = 0
        self.status = 0
        self.color_choice = 'y'
        self.heading = Vector2D(self.dx, self.dy)
        position = world.bounds.point_at((xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        self.old_position = position
        Agent.__init__(self, position, world)

    def color(self):
        if self.color_choice == 'y':
            return "#FFCF00"
        elif self.color_choice == 'g':
            return '#B0FF00'
        elif self.color_choice == 'o':
            return '#FF4F00'

    def shape(self):
        p1 = self.position + Vector2D(0.5, -0.5)
        p2 = self.position + Vector2D(0.5, 0.5)
        p3 = self.position + Vector2D(-0.5, 0.5)
        p4 = self.position + Vector2D(-0.5, -0.5)
        return [p1, p2, p3, p4]

    def move_down(self):
        self.towards = 's'

    def move_up(self):
        self.towards = 'w'

    def move_right(self):
        self.towards = 'd'

    def move_left(self):
        self.towards = 'a'

    def update(self):
        index = 0
        if self.world.bad_followers:
            for followers in self.world.bad_followers:
                x = ((self.position.x - followers.position.x) ** 2 + (
                        self.position.y - followers.position.y) ** 2) ** 0.5
                if 0.0 < x < 0.85:
                    index = 1

        if self.world.game_mode == 1 or self.world.game_mode == 3:
            if len(self.world.followers) >= 5:
                for followers in self.world.followers[4:]:
                    x = ((self.position.x - followers.position.x) ** 2 + (
                            self.position.y - followers.position.y) ** 2) ** 0.5
                    if 0.0 < x < 0.85:
                        index = 1
        if index == 1:
            self.status = 1
        else:
            if self.position.x >= 13.3 or self.position.x <= -27.0:
                self.status = 1
            elif self.position.y >= 19.5 or self.position.y <= -19.5:
                self.status = 1
            else:
                if self.towards == 's':
                    self.dx = 0
                    self.dy = -1.5
                elif self.towards == 'w':
                    self.dx = 0
                    self.dy = 1.5
                elif self.towards == 'a':
                    self.dx = -1.5
                    self.dy = 0

                elif self.towards == 'd':
                    self.dx = 1.5
                    self.dy = 0

                elif self.towards is None:
                    self.dx = 0
                    self.dy = 0

                self.old_position = self.position
                self.heading = Vector2D(self.dx, self.dy)
                new_position = self.position + self.heading * self.speed
                self.position = new_position
                self.position = Point2D(new_position.x, new_position.y)


class Bad_Snake(Agent):
    START_X = random.uniform(-0.7, 0.4)
    START_Y = random.uniform(-0.7, 0.7)

    def __init__(self, world):
        self.world = world
        self.speed = 0.33
        xoffset = self.START_X
        yoffset = self.START_Y
        self.dx = random.uniform(-2.0, 2.0)
        self.dy = random.uniform(-2.0, 2.0)
        self.color_choice = 'b'
        self.heading = Vector2D(self.dx, self.dy)
        self.status = 0
        position = world.bounds.point_at((xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        self.old_position = position
        Agent.__init__(self, position, world)

    def color(self):
        return '#FF0080'

    def shape(self):
        p1 = self.position + Vector2D(0.5, -0.5)
        p2 = self.position + Vector2D(0.5, 0.5)
        p3 = self.position + Vector2D(-0.5, 0.5)
        p4 = self.position + Vector2D(-0.5, -0.5)
        return [p1, p2, p3, p4]

    def check(self):
        if self.position.x >= 13.3:
            self.dx = -self.dx

        elif self.position.x <= -27.0:
            self.dx = -self.dx

        elif self.position.y >= 19.5:
            self.dy = -self.dy

        elif self.position.y <= -19.5:
            self.dy = -self.dy

    def update(self):
        index = 0
        for followers in self.world.followers:
            x = ((self.position.x - followers.position.x) ** 2 + (
                    self.position.y - followers.position.y) ** 2) ** 0.5
            if 0.0 < x < 0.85:
                index = 1
                self.world.score += 5

        if index == 1:
            self.leave()
            for followers in self.world.bad_followers:
                followers.leave()
            self.world.bad_followers.clear()

        else:
            if self.world.snake.status == 1:
                self.leave()
            else:
                self.check()
                self.old_position = self.position
                self.heading = Vector2D(self.dx, self.dy)
                new_position = self.position + self.heading * self.speed
                self.position = new_position
                self.position = Point2D(new_position.x, new_position.y)


class Followers(Agent):

    def __init__(self, world, snake):
        self.world = world
        self.snake = snake
        position = Point2D(self.snake.old_position.x, self.snake.old_position.y)
        self.old_position = position
        self.color_choice = self.snake.color_choice
        Agent.__init__(self, position, world)


    def color(self):
        if self.color_choice == 'y':
            return "#FFCF00"
        elif self.color_choice == 'g':
            return '#B0FF00'
        elif self.color_choice == 'o':
            return '#FF4F00'
        elif self.color_choice == 'b':
            return "#FF0080"

    def update(self):
        self.old_position = self.position
        self.position = Point2D(self.snake.old_position.x, self.snake.old_position.y)


class Boundary1(Agent):
    START_X = 0
    START_Y = 0.92

    def __init__(self, world):
        xoffset = self.START_X
        yoffset = self.START_Y

        position = world.bounds.point_at((xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        Agent.__init__(self, position, world)

    def color(self):
        return "#FF0080"

    def shape(self):
        p1 = self.position + Vector2D(14.0, 0.3)
        p2 = self.position + Vector2D(14.0, -0.3)
        p3 = self.position + Vector2D(-28.0, -0.3)
        p4 = self.position + Vector2D(-28.0, 0.3)
        return [p1, p2, p3, p4]


class Boundary2(Agent):
    START_X = 0
    START_Y = -0.92

    def __init__(self, world):
        xoffset = -self.START_X
        yoffset = self.START_Y

        position = world.bounds.point_at((xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        Agent.__init__(self, position, world)

    def color(self):
        return "#FF0080"

    def shape(self):
        p1 = self.position + Vector2D(14.0, 0.3)
        p2 = self.position + Vector2D(14.0, -0.3)
        p3 = self.position + Vector2D(-28.0, -0.3)
        p4 = self.position + Vector2D(-28.0, 0.3)
        return [p1, p2, p3, p4]


class Boundary3(Agent):
    START_X = 0.47
    START_Y = 0

    def __init__(self, world):
        xoffset = self.START_X
        yoffset = self.START_Y

        position = world.bounds.point_at((xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        Agent.__init__(self, position, world)

    def color(self):
        return "#FF0080"

    def shape(self):
        p1 = self.position + Vector2D(0.3, 21)
        p2 = self.position + Vector2D(-0.3, 21)
        p3 = self.position + Vector2D(-0.3, -21)
        p4 = self.position + Vector2D(0.3, -21)
        return [p1, p2, p3, p4]


class Boundary4(Agent):
    START_X = -0.924
    START_Y = 0

    def __init__(self, world):
        xoffset = self.START_X
        yoffset = self.START_Y

        position = world.bounds.point_at((xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        Agent.__init__(self, position, world)

    def color(self):
        return "#FF0080"

    def shape(self):
        p1 = self.position + Vector2D(0.3, 21)
        p2 = self.position + Vector2D(-0.3, 21)
        p3 = self.position + Vector2D(-0.3, -21)
        p4 = self.position + Vector2D(0.3, -21)
        return [p1, p2, p3, p4]


class PlaySnake(Game):
    def __init__(self):
        Game.__init__(self, 'Snake', 60.0, 45.0, 600, 600, topology='bound', console_lines=7)
        self.survive = True
        self.report('Welcome to the game.')
        self.report('Double-press 1/2/3 to choose game mode.')
        self.report('1. Normal Mode')
        self.report('2. Invincible Mode')
        self.report('3. Advanced Mode')
        self.report('Press H to see Help')
        self.status = -2
        self.score = 0
        self.highest_score = 0
        self.game_mode = None
        Boundary1(self)
        Boundary2(self)
        Boundary3(self)
        Boundary4(self)
        self.snake = Snake(self)
        Bonus(self, self.snake)
        self.followers = []
        self.bad_followers = []

    def handle_keypress(self, event):
        if self.status == -2:
            Game.handle_keypress(self, event)
            if event.char == '1':
                self.game_mode = 1
                self.report('You have chosen the Normal Mode.')
                self.report('Press space to continue')
                self.report()
                self.report()
                self.report()
                self.report()
                self.status = 0

            elif event.char == '2':
                self.game_mode = 2
                self.report('You have chosen the Invincible Mode.')
                self.report('Press space to continue')
                self.report()
                self.report()
                self.report()
                self.report()
                self.status = 0

            elif event.char == '3':
                self.game_mode = 3
                self.report('You have chosen the Advanced Mode.')
                self.report('Press space to continue')
                self.report()
                self.report()
                self.report()
                self.report()
                self.status = 0

        elif self.status == 0:
            Game.handle_keypress(self, event)
            self.report('Please select snake\'s color')
            self.report("Double-press 'y' to select yellow snake(Default choice) ")
            self.report("Double-press 'o' to select orange snake.")
            self.report("Double-press 'g' to select green snake")
            self.report()

            if event.char == 'y':
                self.snake.color_choice = 'y'
                self.status = 1
            elif event.char == 'o':
                self.snake.color_choice = 'o'
                self.status = 1
            elif event.char == 'g':
                self.snake.color_choice = 'g'
                self.status = 1

        elif self.status == 1:
            Game.handle_keypress(self, event)
            self.report('Double-press W/D/A/S to move the snake')
            self.report()
            self.report()
            self.report()
            self.report()

            if event.char == 'w' or event.char == 's' or event.char == 'a' or event.char == 'd':
                self.status = 2

        elif self.status == 2:
            Game.handle_keypress(self, event)
            if self.survive:
                if event.char == 's':
                    if self.snake.towards != 'w':
                        self.snake.move_down()

                elif event.char == 'w':
                    if self.snake.towards != 's':
                        self.snake.move_up()

                elif event.char == 'a':
                    if self.snake.towards != 'd':
                        self.snake.move_left()

                elif event.char == 'd':
                    if self.snake.towards != 'a':
                        self.snake.move_right()

            else:
                if event.char == 'r':
                    self.score = 0
                    self.snake.position = self.bounds.point_at((-0.8 + 1.0) / 2.0, (0.8 + 1.0) / 2.0)
                    self.snake.speed = 0.3
                    self.snake.towards = None
                    self.snake.status = 0
                    self.survive = True

                elif event.char == 'm':
                    self.status = -2
                    self.survive = True
                    self.score = 0
                    self.snake.position = self.bounds.point_at((-0.8 + 1.0) / 2.0, (0.8 + 1.0) / 2.0)
                    self.snake.speed = 0.3
                    self.snake.towards = None
                    self.snake.status = 0
                    self.report('Double-press 1/2/3 to change game mode.')
                    self.report('1. Normal Mode')
                    self.report('2. Invincible Mode')
                    self.report('3. Advanced Mode')
                    self.report()

    def update(self):
        if self.status == 2:
            if self.snake.status == 1:
                self.snake.towards = None
                for follower in self.followers:
                    follower.leave()
                self.followers.clear()
                self.report()
                self.report(f"You lost. Totally score is: {self.score}.")
                self.report(f"Your highest score is {self.highest_score}.")
                self.report('Press r to reset the game')
                self.report('Press m to return back to the menu to choose color')
                self.survive = False
                for follower in self.bad_followers:
                    follower.leave()
                self.bad_followers.clear()
                Game.update(self)
            else:
                Game.update(self)
                self.report()
                self.report()
                self.report()
                self.report(f"Speed right now:{round(self.snake.speed,3) * 100}.")
                self.report(f"Your score is {self.score}.")
                if self.score > self.highest_score:
                    self.highest_score = self.score
                self.report(f"Your highest score is {self.highest_score}.")
                if self.game_mode == 3:
                    if self.score != 0 and self.score % 7 == 0:
                        if len(self.bad_followers) == 0:
                            i = 0
                            self.bad_followers.append(Followers(self, Bad_Snake(self)))
                            x = self.score // 2
                            if x > 40:
                                x = 40
                            while i <= x:
                                self.bad_followers.append(Followers(self, self.bad_followers[-1]))
                                i += 1
                            self.score += 1
        else:
            Game.update(self)


game = PlaySnake()
while not game.GAME_OVER:
    time.sleep(1.0 / 60.0)
    game.update()
