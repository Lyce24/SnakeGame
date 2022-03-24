from Game import Game, Agent
from geometry import Point2D, Vector2D
import random
import time


# setting up bonus point for the snake.
class Bonus(Agent):
    # shape of the bonus
    WIDTH = 1.0
    LENGTH = 1.0

    def __init__(self, world, snake):
        self.length = self.LENGTH
        self.width = self.WIDTH
        # make the bonus show randomly inside the boundary.
        xoffset = random.uniform(-0.8, 0.4)
        yoffset = random.uniform(-0.8, 0.8)
        position = world.bounds.point_at(
            (xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)

        # passing the bonus into the world with the snake in it.
        self.snake = snake
        self.world = world

        # speed of the bonus for the floating bonus mode.
        self.heading = None
        self.speed = 0.18
        self.color_index = 0
        self.dx = random.choice([1.2, -1.2])
        self.dy = random.choice([1.2, -1.2])
        self.old_position = position

        # show the bonus in the world with the Agent class
        Agent.__init__(self, position, world)

    # different colors for different bonus (normal, special, damage mode)
    def color(self):
        if self.color_index == 0:
            return "#B0ABA8"
        elif self.color_index == 1:
            return "#00FFCF"
        elif self.color_index == 2:
            return "#FF4F00"

    # make the bonus a square point in the class
    def shape(self):
        p1 = self.position + Vector2D(self.width / 2.0, self.length / 2.0)
        p2 = self.position + Vector2D(-self.width / 2.0, self.length / 2.0)
        p3 = self.position + Vector2D(-self.width / 2.0, -self.length / 2.0)
        p4 = self.position + Vector2D(self.width / 2.0, -self.length / 2.0)
        return [p1, p2, p3, p4]

    # when player chose the floating bonus mode, let the bonus stays in the boundary
    def check(self):
        # when hitting the boundaries, the direction reverses
        if self.position.x >= 13.3:
            self.dx = -self.dx

        elif self.position.x <= -27.0:
            self.dx = -self.dx

        elif self.position.y >= 19.5:
            self.dy = -self.dy

        elif self.position.y <= -19.5:
            self.dy = -self.dy

    # make the bonus update depending on the mode the player has chosen...
    def update(self):
        # if the floating bonus mode...
        if self.world.game_mode == 4:
            # if the snake eats the bonus...(calculate the distance between the center of the bonus and the center of
            # the snake)
            if ((self.position.x - self.snake.position.x) ** 2 + (
                    self.position.y - self.snake.position.y) ** 2) ** 0.5 < 0.7:

                # make the new bonus appears randomly in the world
                new_position = self.world.bounds.point_at((random.uniform(-0.7, 0.4) + 1.0) / 2.0,
                                                          (random.uniform(-0.6, 0.6) + 1.0) / 2.0)
                self.position = new_position
                self.position = Point2D(new_position.x, new_position.y)

                # score += 1 and speed of the snake += 0.005
                self.world.score += 1
                self.world.snake.speed += 0.005
                # add three followers for the snake
                if not self.world.followers:
                    self.world.followers.append(
                        Followers(self.world, self.world.snake))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                else:
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))

            # if the snake missed the bonus...
            else:
                # make sure the bonus is in the boundaries...
                self.check()
                # make the bonus move by using Vector2D wth dx and dy
                self.old_position = self.position
                self.heading = Vector2D(self.dx, self.dy)
                new_position = self.position + self.heading * self.speed
                self.position = new_position
                self.position = Point2D(new_position.x, new_position.y)

        # if the player chose the head-to-tail mode...
        elif self.world.game_mode == 5:
            # similar process as stated before if the snake eats the bonus...
            if ((self.position.x - self.snake.position.x) ** 2 + (
                    self.position.y - self.snake.position.y) ** 2) ** 0.5 < 0.7:
                new_position = self.world.bounds.point_at((random.uniform(-0.7, 0.4) + 1.0) / 2.0,
                                                          (random.uniform(-0.6, 0.6) + 1.0) / 2.0)
                self.position = new_position
                self.position = Point2D(new_position.x, new_position.y)
                self.world.score += 1
                self.world.snake.speed += 0.005
                if not self.world.followers:
                    self.world.followers.append(
                        Followers(self.world, self.world.snake))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                else:
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))

                # make the head of the snake to be the position of the last follower
                self.world.snake.position = self.world.followers[-1].position
                # change the heading of the snake to its opposite direction as before...
                if self.world.snake.towards == 'w':
                    self.world.snake.towards = 's'
                elif self.world.snake.towards == 's':
                    self.world.snake.towards = 'w'
                elif self.world.snake.towards == 'a':
                    self.world.snake.towards = 'd'
                elif self.world.snake.towards == 'd':
                    self.world.snake.towards = 'a'

        # if the player chose the damagemode...
        elif self.world.game_mode == 6:
            # if the snake eats the bonus...
            if ((self.position.x - self.snake.position.x) ** 2 + (
                    self.position.y - self.snake.position.y) ** 2) ** 0.5 < 0.7:

                # if the bonus is a special bonus...(score % 11 == 0 as shield point)
                if self.world.score != 0 and self.world.score % 11 == 0:
                    new_position = self.world.bounds.point_at((random.uniform(-0.7, 0.4) + 1.0) / 2.0,
                                                              (random.uniform(-0.6, 0.6) + 1.0) / 2.0)
                    self.position = new_position
                    self.position = Point2D(new_position.x, new_position.y)
                    # shield of the snake += 4 and make the damage mode disappear
                    self.world.snake.shield += 4
                    self.world.snake.damagemode = 0

                # if the bonus is a damage bonus...(score % 13 == 0)
                elif self.world.score != 0 and self.world.score % 13 == 0:
                    new_position = self.world.bounds.point_at((random.uniform(-0.7, 0.4) + 1.0) / 2.0,
                                                              (random.uniform(-0.6, 0.6) + 1.0) / 2.0)
                    self.position = new_position
                    self.position = Point2D(new_position.x, new_position.y)
                    # activate snake's damage mode
                    self.world.snake.damagemode = 1

                # if the regular bonus, then similar process as before (set damage mode as 0)
                else:
                    new_position = self.world.bounds.point_at((random.uniform(-0.7, 0.4) + 1.0) / 2.0,
                                                              (random.uniform(-0.6, 0.6) + 1.0) / 2.0)
                    self.position = new_position
                    self.position = Point2D(new_position.x, new_position.y)
                    self.world.snake.damagemode = 0

                # add followers and barriers to the world
                if not self.world.followers:
                    self.world.followers.append(
                        Followers(self.world, self.world.snake))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.score += 1
                    self.world.snake.speed += 0.005
                else:
                    # add barriers every time when the snake eat the 2 bonuses
                    if self.world.score % 2 == 1:
                        self.world.followers.append(
                            Followers(self.world, self.world.followers[-1]))
                        self.world.followers.append(
                            Followers(self.world, self.world.followers[-1]))
                        self.world.followers.append(
                            Followers(self.world, self.world.followers[-1]))
                        b = Barriers(self.world)
                        self.world.barriers.append(b)
                        self.position = new_position
                        self.position = Point2D(new_position.x, new_position.y)
                        self.world.score += 1
                        self.world.snake.speed += 0.005

                    # regular update for regular bonus
                    else:
                        self.world.followers.append(
                            Followers(self.world, self.world.followers[-1]))
                        self.world.followers.append(
                            Followers(self.world, self.world.followers[-1]))
                        self.world.followers.append(
                            Followers(self.world, self.world.followers[-1]))
                        self.world.score += 1
                        self.world.snake.speed += 0.005

        # every other mode...
        else:
            # if the snake eats the bonus, add three followers to the snake
            if ((self.position.x - self.snake.position.x) ** 2 + (
                    self.position.y - self.snake.position.y) ** 2) ** 0.5 < 0.7:
                new_position = self.world.bounds.point_at((random.uniform(-0.7, 0.4) + 1.0) / 2.0,
                                                          (random.uniform(-0.6, 0.6) + 1.0) / 2.0)
                self.position = new_position
                self.position = Point2D(new_position.x, new_position.y)
                self.world.score += 1
                self.world.snake.speed += 0.005
                if not self.world.followers:
                    self.world.followers.append(
                        Followers(self.world, self.world.snake))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                else:
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))
                    self.world.followers.append(
                        Followers(self.world, self.world.followers[-1]))


# setting up the snake class
class Snake(Agent):
    # set the birthplace for the snake...
    START_X = -0.8
    START_Y = 0.8

    # main attributes for the snake
    def __init__(self, world):
        self.world = world
        self.speed = 0.3
        xoffset = self.START_X
        yoffset = self.START_Y
        self.towards = None
        self.dx = 0
        self.dy = 0
        self.shield = 4
        self.status = 0
        self.color_choice = 'y'
        self.damagemode = 0
        self.heading = Vector2D(self.dx, self.dy)
        position = world.bounds.point_at(
            (xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        self.old_position = position
        Agent.__init__(self, position, world)

    # different colors for the snake for player to choose
    def color(self):
        if self.color_choice == 'y':
            return "#FFCF00"
        elif self.color_choice == 'g':
            return '#B0FF00'
        elif self.color_choice == 'o':
            return '#FF4F00'

    # make the shape for the snake as bigger than its followers...
    def shape(self):
        p1 = self.position + Vector2D(0.5, -0.5)
        p2 = self.position + Vector2D(0.5, 0.5)
        p3 = self.position + Vector2D(-0.5, 0.5)
        p4 = self.position + Vector2D(-0.5, -0.5)
        return [p1, p2, p3, p4]

    # change direction of the snake
    def move_down(self):
        self.towards = 's'

    def move_up(self):
        self.towards = 'w'

    def move_right(self):
        self.towards = 'd'

    def move_left(self):
        self.towards = 'a'

    # update method of the snake
    def update(self):
        # if there is barriers in the world...(meaning the player is playing damagemode)
        if self.world.barriers:
            # if the damage mode is off...
            if self.damagemode == 0:
                # if the snake has shield...
                if self.shield > 0:
                    # check for every barrier...
                    for barrier in self.world.barriers:
                        x = ((self.position.x - barrier.position.x) ** 2 + (
                            self.position.y - barrier.position.y) ** 2) ** 0.5
                        # if the head of snake crashes into one of the barriers, shield -= 1
                        if 0.0 < x < 0.85:
                            self.shield -= 1
                        if self.shield < 0:
                            self.shield = 0

                # if the snake has no shield, hit the barrier and die
                elif self.shield == 0:
                    for barrier in self.world.barriers:
                        x = ((self.position.x - barrier.position.x) ** 2 + (
                            self.position.y - barrier.position.y) ** 2) ** 0.5
                        if 0.0 < x < 0.85:
                            self.status = 1

            # if the damage mode is activated...
            else:
                # check every barrier...
                for barrier in self.world.barriers:
                    x = ((self.position.x - barrier.position.x) ** 2 + (
                        self.position.y - barrier.position.y) ** 2) ** 0.5
                    # if the snake hits one of the barriers, the barriers breaks and score of the snake+= 5
                    if 0.0 < x < 0.85:
                        # reset the damage mode
                        self.damagemode = 0
                        # remove the barriers from the world
                        self.world.barriers.remove(barrier)
                        barrier.leave()
                        self.world.score += 5
                        # out of the loop
                        continue

        # if playing Sudden Attack mode...
        if self.world.bad_followers:
            # check every follower of the bad snake...
            for followers in self.world.bad_followers:
                # if the head of the snake hits the followers, then index = 1(means dead)
                x = ((self.position.x - followers.position.x) ** 2 + (
                    self.position.y - followers.position.y) ** 2) ** 0.5
                if 0.0 < x < 0.85:
                    self.status = 1

        # if playing game mode besides 2 and 5...(they are too hard if they have this rule)
        if self.world.game_mode != 2 and self.world.game_mode != 5:
            # if the snake hit the followers of itself, the snake will die
            if len(self.world.followers) >= 5:
                for followers in self.world.followers[4:]:
                    x = ((self.position.x - followers.position.x) ** 2 + (
                        self.position.y - followers.position.y) ** 2) ** 0.5
                    if 0.0 < x < 0.85:
                        self.status = 1

        # if the snake is alive...
        if self.status != 1:
            # hit the boundaries and dead (Except the invincible mode)
            if self.position.x >= 13.3:
                # if invincible mode...
                if self.world.game_mode == 2:
                    # hit the boundary and passes through its opposite one
                    self.position.x = -26.7
                else:
                    self.status = 1
            elif self.position.x <= -27.0:
                if self.world.game_mode == 2:
                    self.position.x = 13.0
                else:
                    self.status = 1
            elif self.position.y >= 19.5:
                if self.world.game_mode == 2:
                    self.position.y = -19.3
                else:
                    self.status = 1
            elif self.position.y <= -19.5:
                if self.world.game_mode == 2:
                    self.position.y = 19.3
                else:
                    self.status = 1
            # if the snake is still alive...
            else:
                # change direction with the change of heading
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

                # update its position
                self.old_position = self.position
                self.heading = Vector2D(self.dx, self.dy)
                new_position = self.position + self.heading * self.speed
                self.position = new_position
                self.position = Point2D(new_position.x, new_position.y)


# bad snake created for the Sudden attack mode...(Basically create a snake randomly that
# add difficulty to this game. If the snake bumps into one of the followers of the bad
# snake, the snake dies.)
class Bad_Snake(Agent):
    START_X = random.uniform(-0.7, 0.4)
    START_Y = random.uniform(-0.7, 0.7)

    # similar behaviors as snake but with dx and dy and different color
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
        position = world.bounds.point_at(
            (xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
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

    # make the bad snake in boundaries
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
        # check if hit the followers of the snake, if it does, then the bad snake dies...
        for followers in self.world.followers:
            x = ((self.position.x - followers.position.x) ** 2 + (
                self.position.y - followers.position.y) ** 2) ** 0.5
            if 0.0 < x < 0.85:
                self.status = 1
                self.world.score += 3

        # if died...
        if self.status == 1:
            # clear everything
            self.leave()
            for followers in self.world.bad_followers:
                followers.leave()
            self.world.bad_followers.clear()

        # if alive...
        else:
            # if the snake dies, then leave...
            if self.world.snake.status == 1:
                self.leave()
            # else, update like normal snake (in boundaries)
            else:
                self.check()
                self.old_position = self.position
                self.heading = Vector2D(self.dx, self.dy)
                new_position = self.position + self.heading * self.speed
                self.position = new_position
                self.position = Point2D(new_position.x, new_position.y)


# followers for the snake (basically follows the old position of the last followers alive,
# E.g. if there is no followers at beginning, then the first follower will follow the old
# position of the snake head. Then it follows the rule of tracing the old position for the
# last followers exists.)
class Followers(Agent):

    # passing the world and the snake that meant to be followed
    def __init__(self, world, snake):
        self.world = world
        self.snake = snake
        # records the old position for next followers; follows the color of the original snake
        position = Point2D(self.snake.old_position.x,
                           self.snake.old_position.y)
        self.old_position = position
        self.color_choice = self.snake.color_choice
        Agent.__init__(self, position, world)

    def shape(self):
        p1 = self.position + Vector2D(0.125, 0.125)
        p2 = self.position + Vector2D(-0.125, 0.125)
        p3 = self.position + Vector2D(-0.125, -0.125)
        p4 = self.position + Vector2D(0.125, -0.125)
        return [p1, p2, p3, p4]

    def color(self):
        if self.color_choice == 'y':
            return "#FFCF00"
        elif self.color_choice == 'g':
            return '#B0FF00'
        elif self.color_choice == 'o':
            return '#FF4F00'
        elif self.color_choice == 'b':
            return "#FF0080"

    # trace the old position of the last followers (self.snake here)
    def update(self):
        self.old_position = self.position
        self.position = Point2D(self.snake.old_position.x,
                                self.snake.old_position.y)


# Barriers for the damage mode (randomly generates a bonus-like point in the world.
# If the snake hits one of them, then the snake dies or lose shields depends on the
# shielding power of the snake.)
class Barriers(Agent):
    WIDTH = 1.0
    LENGTH = 1.0

    def __init__(self, world):
        # setting attributes for the barriers (standard size as bonus)
        self.length = self.LENGTH
        self.width = self.WIDTH
        xoffset = random.uniform(-0.8, 0.4)
        yoffset = random.uniform(-0.8, 0.8)
        self.world = world
        position = world.bounds.point_at(
            (xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        self.old_position = position
        Agent.__init__(self, position, world)

    def color(self):
        return "#FF0080"

    def shape(self):
        p1 = self.position + Vector2D(self.width / 2.0, self.length / 2.0)
        p2 = self.position + Vector2D(-self.width / 2.0, self.length / 2.0)
        p3 = self.position + Vector2D(-self.width / 2.0, -self.length / 2.0)
        p4 = self.position + Vector2D(self.width / 2.0, -self.length / 2.0)
        return [p1, p2, p3, p4]


# setting up boundaries by passing x,y-coordinate and the shape of the barriers
class Boundary(Agent):

    def __init__(self, world, x, y, side):
        xoffset = x
        yoffset = y
        self.side = side
        position = world.bounds.point_at(
            (xoffset + 1.0) / 2.0, (yoffset + 1.0) / 2.0)
        Agent.__init__(self, position, world)

    def color(self):
        return "#FF0080"

    def shape(self):
        # if this barrier is for 'up' or 'down'...
        if self.side == 'ud':
            p1 = self.position + Vector2D(14.0, 0.3)
            p2 = self.position + Vector2D(14.0, -0.3)
            p3 = self.position + Vector2D(-28.0, -0.3)
            p4 = self.position + Vector2D(-28.0, 0.3)
            return [p1, p2, p3, p4]

        # if this barrier is for 'left' ot 'right'...
        elif self.side == 'lr':
            p1 = self.position + Vector2D(0.3, 21)
            p2 = self.position + Vector2D(-0.3, 21)
            p3 = self.position + Vector2D(-0.3, -21)
            p4 = self.position + Vector2D(0.3, -21)
            return [p1, p2, p3, p4]


# main process of SNAKE GAME
class PlaySnake(Game):
    def __init__(self):
        # set window to play the game
        Game.__init__(self, 'Snake', 60.0, 45.0, 600, 600,
                      topology='bound', console_lines=10)
        self.survive = True
        # initiate the game with some message of how to play at the start the game.
        self.report("Welcome to the game.")
        self.report('Press 1/2/3/4/5/6 to choose game mode.')
        self.report('1. Normal Mode')
        self.report('2. Invincible Mode')
        self.report('3. Sudden Attack Mode')
        self.report('4. Floating Bonus Mode')
        self.report('5. Head-To-Tail Mode')
        self.report('6. Damage Mode')
        self.report('Press h to see Help')

        # set some index for future useage.
        self.status = -2
        self.score = 0
        self.highest_score = 0
        self.game_mode = None

        # set barriers and Main object - Snakes into the game.
        Boundary(self, 0, 0.92, 'ud')
        Boundary(self, 0, -0.92, 'ud')
        Boundary(self, 0.47, 0, 'lr')
        Boundary(self, -0.924, 0, 'lr')
        self.snake = Snake(self)
        self.bonus = Bonus(self, self.snake)

        # setting empty list for future useage.
        self.followers = []
        self.bad_followers = []
        self.barriers = []

    def handle_keypress(self, event):
        # phase of choosing mode
        if self.status == -2:
            Game.handle_keypress(self, event)
            if event.char == '1':
                self.game_mode = 1
                self.report('You have chosen the Normal Mode.')
                self.report()
                self.report(
                    'This’s the most classic rules of playing Snake. Hitting the boundaries and yourself will cause death.')
                self.report()
                self.report()
                self.report()
                self.report()
                self.report('Press space to continue')
                self.report()

                self.status = 0

            elif event.char == '2':
                self.game_mode = 2
                self.report('You have chosen the Invincible Mode.')
                self.report()
                self.report(
                    'Invincible mode as you will never die, not from hitting the boundaries or yourself.')
                self.report(
                    'However, the highest score will not change since you are invincible.')
                self.report()
                self.report()
                self.report()
                self.report('Press space to continue')
                self.report()

                self.status = 0

            elif event.char == '3':
                self.game_mode = 3
                self.report('You have chosen the Sudden Attack Mode.')
                self.report()
                self.report(
                    'While eating the bonus, another Snake will generate in the world randomly and move.')
                self.report(
                    'You will die if you hit it. However, you can kill it by using a small trick if it hits your body.')
                self.report()
                self.report()
                self.report()
                self.report('Press space to continue')
                self.report()

                self.status = 0

            elif event.char == '4':
                self.game_mode = 4
                self.report('You have chosen the Floating Bonus Mode.')
                self.report()
                self.report(
                    'The bonus for this mode will move in this world, you have to predict the movement')
                self.report('of the bonus in order to eat it.')
                self.report()
                self.report()
                self.report()
                self.report('Press space to continue')
                self.report()

                self.status = 0

            elif event.char == '5':
                self.game_mode = 5
                self.report('You have chosen the Head-To-Tail Mode.')
                self.report()
                self.report(
                    'When the snake eats the bonus, the head becomes the tail and the tail become the head.')
                self.report(
                    'The direction of movement of the snake all changes too, so you have to be careful about not hitting the boundaries.')
                self.report()
                self.report()
                self.report()
                self.report('Press space to continue')
                self.report()

                self.status = 0

            elif event.char == '6':
                self.game_mode = 6
                # in order to show the shields of the snake, the default color for the snake is green
                self.snake.color_choice = 'g'
                self.report('You have chosen the Damage Mode.')
                self.report()
                self.report(
                    'Barriers will generate frequently in this mode. You need to collect the special bonuses as many as possible in ')
                self.report(
                    'order to survive. You can destroy the barriers when you are in damage mode by eating orange bonus.')
                self.report()
                self.report()
                self.report()
                self.report('Press space to continue')
                self.report()

                self.status = 1

            # show help information
            elif event.char == 'h':
                self.report(
                    'Player can use ‘W/A/S/D’ to change the direction of the snake. The game ends when the snake hits the boundaries')
                self.report(
                    'or itself. The snake can gain points by eating the grey bonus in the game. However, eating the bonus will ')
                self.report(
                    'cause the speed and the length of the snake to increase, which increases the difficulty of the game.')
                self.report()
                self.report(
                    'The game has different modes, by pressing 1/2/3/4/5/6, you can experience each mode by yourself. ')
                self.report()
                self.report('GLHF!')
                self.report()
                self.report("Press 'b' to return to the main menu.")

            # b to return to the menu
            elif event.char == 'b':
                self.report("Welcome to the game.")
                self.report('Press 1/2/3/4/5/6 to choose game mode.')
                self.report('1. Normal Mode')
                self.report('2. Invincible Mode')
                self.report('3. Sudden Attack Mode')
                self.report('4. Floating Bonus Mode')
                self.report('5. Head-To-Tail Mode')
                self.report('6. Damage Mode')
                self.report('Press h to see Help')

        # choosing color of the snake
        elif self.status == 0:
            Game.handle_keypress(self, event)
            self.report('Please select snake\'s color')
            self.report(
                "Double-press 'y' to select yellow snake(Default choice) ")
            self.report("Double-press 'o' to select orange snake.")
            self.report("Double-press 'g' to select green snake")
            self.report()
            self.report()
            self.report()
            self.report()
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

        # initiate the game, let players be familiar with the game.
        elif self.status == 1:
            Game.handle_keypress(self, event)
            self.report('Press W/D/A/S to move the snake')
            self.report()
            self.report()
            self.report()
            self.report()
            self.report()
            self.report()
            self.report()
            self.report()

            if event.char == 'w' or event.char == 's' or event.char == 'a' or event.char == 'd':
                self.status = 2

        # start the game...
        elif self.status == 2:
            Game.handle_keypress(self, event)
            # if the snake is alive...
            if self.survive:
                if self.game_mode == 2:
                    if event.char == ' ':
                        self.snake.status = 1

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

            # if the snake is dead...
            else:
                # r - restart the game with same mode.
                if event.char == 'r':
                    self.score = 0
                    self.snake.position = self.bounds.point_at(
                        (-0.8 + 1.0) / 2.0, (0.8 + 1.0) / 2.0)
                    self.snake.speed = 0.3
                    self.snake.towards = None
                    self.snake.status = 0
                    self.survive = True

                # m - return to the menu to change mode and color
                elif event.char == 'm':
                    self.status = -2
                    self.survive = True
                    self.score = 0
                    self.snake.position = self.bounds.point_at(
                        (-0.8 + 1.0) / 2.0, (0.8 + 1.0) / 2.0)
                    self.snake.speed = 0.3
                    self.snake.towards = None
                    self.snake.status = 0
                    self.report('Press 1/2/3/4/5/6 to change game mode.')
                    self.report('1. Normal Mode')
                    self.report('2. Invincible Mode')
                    self.report('3. Sudden Attack Mode')
                    self.report('4. Floating Bonus Mode')
                    self.report('5. Head-To-Tail Mode')
                    self.report('6. Damage Mode')
                    self.report()
                    self.report('Press q to quit the game.')

    def update(self):
        # if the game is still going...
        if self.status == 2:
            # if the snake is dead, set the snake to the initial mode.
            if self.snake.status == 1:
                self.snake.towards = None
                # delete all followers
                for follower in self.followers:
                    follower.leave()
                self.followers.clear()
                self.report()
                self.report(f"You lost. Totally score is: {self.score}.")
                self.report(f"Your highest score is {self.highest_score}.")
                self.report()
                self.report()
                self.report()
                self.report('Press r to reset the game')
                self.report(
                    'Press m to return back to the menu to choose color')
                self.report('Press q to quit the game.')
                self.survive = False
                # delete all bad snakes and their followers, and all barriers.
                for follower in self.bad_followers:
                    follower.leave()
                self.bad_followers.clear()
                for barrier in self.barriers:
                    barrier.leave()
                self.barriers.clear()
                Game.update(self)
            else:
                # if the snake is alive and the game mode is 'Damage mode'...
                if self.game_mode == 6:
                    # make changes of the console to show different things...
                    Game.update(self)
                    self.report()
                    self.report(f'Shields:{self.snake.shield}')
                    self.report()
                    self.report(
                        '* Each encounter with the purple block will consume certain amount of shields.')
                    self.report('* Eat bonus of cyan color to gain 4 shields.')
                    self.report(
                        '* Eat bonus of orange color to activate damage mode to destroy barriers and get 5 points.')
                    self.report()
                    self.report(
                        f"Speed right now:{round(self.snake.speed, 3) * 100}.")
                    self.report(f"Your score is {self.score}.")
                    if self.score > self.highest_score:
                        self.highest_score = self.score
                    self.report(f"Your highest score is {self.highest_score}.")

                    # change the colors of the snake and bonuses based on their status.
                    if self.snake.damagemode != 0:
                        self.snake.color_choice = 'o'
                        self.snake.color()
                    elif self.snake.shield <= 2:
                        self.snake.color_choice = 'y'
                        self.snake.color()
                    else:
                        self.snake.color_choice = 'g'
                        self.snake.color()

                    if self.score != 0 and self.score % 11 == 0:
                        self.bonus.color_index = 1
                        self.bonus.color()
                    elif self.score != 0 and self.score % 13 == 0:
                        self.bonus.color_index = 2
                        self.bonus.color()
                    else:
                        self.bonus.color_index = 0
                        self.bonus.color()

                # if game mode is sudden attack...
                elif self.game_mode == 3:
                    Game.update(self)
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report(
                        f"Speed right now:{round(self.snake.speed, 3) * 100}.")
                    self.report(f"Your score is {self.score}.")
                    if self.score > self.highest_score:
                        self.highest_score = self.score
                    self.report(f"Your highest score is {self.highest_score}.")

                    # if score % 7 == 0, make the bad snake show up randomly
                    if self.score != 0 and self.score % 3 == 0:
                        # make the bad snake grow when the game continues (leveling up)
                        if len(self.bad_followers) == 0:
                            i = 0
                            self.bad_followers.append(
                                Followers(self, Bad_Snake(self)))
                            self.bad_followers.append(
                                Followers(self, self.bad_followers[-1]))
                            self.bad_followers.append(
                                Followers(self, self.bad_followers[-1]))
                            x = self.score // 2
                            # at most 33 followers for the bad snake.
                            if x > 30:
                                x = 30
                            while i <= x:
                                self.bad_followers.append(
                                    Followers(self, self.bad_followers[-1]))
                                i += 1
                            self.score += 1
                # any other game mode
                else:
                    # standard update method + showing data in the console.
                    Game.update(self)
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report()
                    self.report(
                        f"Speed right now:{round(self.snake.speed, 3) * 100}.")
                    self.report(f"Your score is {self.score}.")
                    if self.game_mode == 2:
                        self.report('Press space to stop the game.')
                    else:
                        if self.score > self.highest_score:
                            self.highest_score = self.score
                        self.report(
                            f"Your highest score is {self.highest_score}.")

        # if not in the game, update too.
        else:
            Game.update(self)


game = PlaySnake()
while not game.GAME_OVER:
    time.sleep(1.0 / 60.0)
    game.update()
