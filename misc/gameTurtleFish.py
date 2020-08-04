from random import randint, choice


class Movable(object):
    def __init__(self, x_range, y_range, step):
        (self.x_min, self.x_max) = x_range
        (self.y_min, self.y_max) = y_range
        self.step = step
        self.x_pos = randint(self.x_min, self.x_max)
        self.y_pos = randint(self.y_min, self.y_max)

    def pos(self):
        return (self.x_pos, self.y_pos)

    def move(self):
        direction = choice(((1, 0), (0, 1), (-1, 0), (0, -1)))
        step = randint(1, self.step)

        x_new = self.x_pos + direction[0] * step
        y_new = self.y_pos + direction[1] * step

        if x_new > self.x_max:
            x_new = 2 * self.x_max - x_new
        elif x_new < self.x_min:
            x_new = 2 * self.x_min - x_new

        if y_new > self.y_max:
            y_new = 2 * self.y_max - y_new
        elif y_new < self.y_min:
            y_new = 2 * self.y_min - y_new

        self.x_pos = x_new
        self.y_pos = y_new

        return (self.x_pos, self.y_pos)


class Turtle(Movable):
    def __init__(self, name, **args):
        self.stamina_max = 100
        self.stamina_inc = 20
        self.stamina_dec = 1
        self.stamina = self.stamina_max
        self.name = name
        super().__init__(**args)

    def dead(self):
        return self.stamina - self.stamina_dec < 0

    def eat(self):
        self.stamina += self.stamina_inc
        self.stamina = (
            self.stamina_max if self.stamina > self.stamina_max else self.stamina
        )

    def move(self):
        if self.dead():
            return self.pos()
        else:
            self.stamina -= self.stamina_dec
            return super().move()


class Fish(Movable):
    def __init__(self, name, **args):
        self.name = name
        super().__init__(**args)


class Game(object):
    def __init__(self):
        self.x_range = (0, 10)
        self.y_range = (0, 10)
        self.turtle_nb = 1
        self.fish_nb = 10
        self.turtle_step = 2
        self.fish_step = 1
        self.round = 0
        self.turtle_list = [
            Turtle(
                name=i,
                x_range=self.x_range,
                y_range=self.y_range,
                step=self.turtle_step,
            )
            for i in range(self.turtle_nb)
        ]
        self.fish_list = [
            Fish(
                name=i, x_range=self.x_range, y_range=self.y_range, step=self.fish_step
            )
            for i in range(self.fish_nb)
        ]

    def not_end(self):
        return self.turtle_list and self.fish_list

    def handle_collision(self):
        for turtle in self.turtle_list:
            # it is dangerous to remove items while iterating, take a slice to make is safe
            for fish in self.fish_list[:]:
                if turtle.pos() == fish.pos():
                    turtle.eat()
                    self.fish_list.remove(fish)

        for turtle in self.turtle_list[:]:
            if turtle.dead():
                self.turtle_list.remove(turtle)

    def next_turn(self):
        if not self.not_end():
            return

        for turtle in self.turtle_list:
            turtle.move()

        for fish in self.fish_list:
            fish.move()

        self.round += 1
        self.handle_collision()
        self.print_stats()

    def print_stats(self):
        board = []
        for x in range(self.x_range[0], self.x_range[1]):
            line = []
            for y in range(self.y_range[0], self.y_range[1]):
                tag = (
                    "T"
                    if (x, y) in [turtle.pos() for turtle in self.turtle_list]
                    else "F"
                    if (x, y) in [fish.pos() for fish in self.fish_list]
                    else "O"
                )
                line.append(tag)
            board.append(" ".join(line))

        print(
            "ROUND {0}: {1} turtle(s) and {2} fish left:".format(
                self.round, len(self.turtle_list), len(self.fish_list)
            )
        )
        for i in range(len(board)):
            print(board[i])
        print("")

    def winner(self):
        return "TURTLE" if self.turtle_list else "FISH"


print("GAME BEGIN!\n")
game = Game()
while game.not_end():
    game.next_turn()
print("GAME END. WINNER: {0}!".format(game.winner()))
