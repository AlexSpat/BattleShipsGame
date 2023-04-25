import random


class Ship:
    def __init__(self, coordinates, ship_size):
        self.coordinates = coordinates
        self.ship_size = ship_size
        self.hits = []

    def hit(self, coordinate):
        self.hits.append(coordinate)

    def is_sunk(self):
        return all(coordinate in self.hits for coordinate in self.coordinates)


class Board:
    def __init__(self, size):
        self.size = size
        self.ships = []
        self.grid = [['О' for _ in range(size)] for _ in range(size)]
        self.hits = []
        self.misses = []

    def add_ship(self, ship, ship_size):
        if ship_size == 1:
            for coordinate in ship.coordinates:
                if not self.is_valid_coordinate(coordinate):
                    raise ValueError("Invalid ship placement")
                x, y = coordinate
                if self.grid[x][y] == '■':
                        raise ValueError("В этом месте уже есть корабль")
                for x, y in self.get_adjacent_coordinates(coordinate):
                    if self.is_valid_coordinate((x, y)) and self.grid[x][y] == '■':
                        raise ValueError("Ships must be at least one cell apart")
                self.grid[coordinate[0]][coordinate[1]] = '■'
            self.ships.append(ship)
        elif ship_size == 2:
            x1, y1 = 0, 0
            for coordinate in ship.coordinates:
                if not self.is_valid_coordinate(coordinate):
                    raise ValueError("Invalid ship placement")
                for x, y in self.get_adjacent_coordinates(coordinate):
                    if not x == x1 and y == y1:
                        if self.is_valid_coordinate((x, y)) and self.grid[x][y] == '■':
                            raise ValueError("Ships must be at least one cell apart")
                self.grid[coordinate[0]][coordinate[1]] = '■'
                x1, y1 = coordinate
            self.ships.append(ship)

    def is_valid_coordinate(self, coordinate):
        x, y = coordinate
        return 0 <= x < self.size and 0 <= y < self.size

    def get_adjacent_coordinates(self, coordinate):
        x, y = coordinate
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def is_hit(self, coordinate):
        return coordinate in self.hits

    def is_miss(self, coordinate):
        return coordinate in self.misses

    def record_hit(self, coordinate):
        self.hits.append(coordinate)

    def record_miss(self, coordinate):
        self.misses.append(coordinate)

    def display(self):
        print(" | " + " | ".join(str(i + 1) for i in range(self.size)) + " |")
        for i in range(self.size):
            row = "| " + " | ".join(self.grid[i]) + " |"
            print(f"{i + 1} | {row}")


player_board = Board(6)
computer_board = Board(6)


def play_game():
    for ship_size in [2, 2, 1, 1, 1, 1]: # [3, 2, 2, 1, 1, 1, 1]:
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            direction = random.choice(['horizontal', 'vertical'])
            coordinates = [(x, y)]
            if direction == 'horizontal':
                for i in range(1, ship_size):
                    coordinates.append((x + i, y))
            else:
                for i in range(1, ship_size):
                    coordinates.append((x, y + i))
                    try:
                        ship = Ship(coordinates, ship_size)
                        computer_board.add_ship(ship, ship_size)
                        break
                    except ValueError:
                        continue
                    
    # Place ships on player board
    player_board.display()
    print("Place your ships:")
    numb_ship = 1
    for ship_size in [1, 1, 1, 1]: # [3, 2, 2, 1, 1, 1, 1]:
        while True:
            if ship_size == 2 or ship_size == 3:
                try:
                    vert_or_hor = int(input("Вы хотите расположить корабль вертикально (1) или горизонтально (2)?: "))
                    if vert_or_hor == 1:
                        coordinates = []
                        y = int(input(f"Enter Y coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                        for i in range(ship_size):
                            x = int(input(f"Enter X coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                            coordinates.append((x, y))
                        ship = Ship(coordinates, ship_size)
                        player_board.add_ship(ship, ship_size)
                        numb_ship += 1
                        player_board.display()
                        break
                    elif vert_or_hor == 2:
                        coordinates = []
                        x = int(input(f"Enter X coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                        for i in range(ship_size):
                            y = int(input(f"Enter Y coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                            coordinates.append((x, y))
                        ship = Ship(coordinates, ship_size)
                        player_board.add_ship(ship, ship_size)
                        numb_ship += 1
                        player_board.display()
                        break
                    else:
                        print("Хз")
                except ValueError as e:
                        print(e)
            else:
                try:
                    coordinates = []
                    x = int(input(f"Enter X coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                    y = int(input(f"Enter Y coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                    coordinates.append((x, y))
                    ship = Ship(coordinates, ship_size)
                    player_board.add_ship(ship, ship_size)
                    numb_ship += 1
                    player_board.display()
                    break
                except ValueError as e:
                    print(e)
                    

    # Place ships on computer board
    # print("Комп расставляет корабли")
    

    while True:
        print("Player's turn:")
        player_board.display()
        x = int(input("Enter X coordinate for your attack: ")) - 1
        y = int(input("Enter Y coordinate for your attack: ")) - 1
        if player_board.is_hit((x, y)) or player_board.is_miss((x, y)):
            print("You've already attacked that coordinate. Try again.")
            continue
        if computer_board.grid[x][y] == '■':
            print("Hit!")
            player_board.record_hit((x, y))
            for ship in computer_board.ships:
                if (x, y) in ship.coordinates:
                    ship.hit((x, y))
                    if ship.is_sunk():
                        print("You sank a ship!")
                        computer_board.ships.remove(ship)
                    break
        else:
            print("Miss.")
            player_board.record_miss((x, y))

        if not computer_board.ships:
            print("Congratulations! You won!")
            break

        print("Computer's turn:")
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            if (x, y) not in player_board.hits and (x, y) not in player_board.misses:
                break
        if player_board.grid[x][y] == '■':
            print("You were hit!")
            for ship in player_board.ships:
                if (x, y) in ship.coordinates:
                    ship.hit((x, y))
                    if ship.is_sunk():
                        print("Computer sank one of your ships!")
                        player_board.ships.remove(ship)
                    break
        else:
            print("Computer missed.")
            player_board.record_miss((x, y))

        if not player_board.ships:
            print("Game over. You lost.")
            break


if __name__ == "__main__":
    play_game()
