import random
import matplotlib.pyplot as plt


class Room:
    def __init__(self, width: int, length: int):
        """Constructor

        :param width: room width
        :param length: room length
        """
        self.width = width
        self.length = length
        self.room = list()
        for w in range(self.width):
            self.room.append(list())
            for _ in range(self.length):
                self.room[-1].append(0)

    def add_dust(self, count: int):
        """Add count number of dust to random positions in the room

        :param count: number of dust
        """
        for _ in range(count):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.length - 1)
            self.room[x][y] += 1

    def has_position(self, pos: tuple) -> True or False:
        """Checking pos(x, y) in room

        :param pos: (x, y) coordinates
        :return: True if the room has position with coordinates False otherwise
        """
        x, y = pos

        return (0 <= x < self.width) and (0 <= y < self.length)

    def has_dust(self, pos: tuple) -> True or False:
        """Checking dust in room

        :param pos: (x, y) coordinates
        :return: True if there is dust on position with coordinates False otherwise
        """
        x, y = pos

        if not self.has_position(pos):
            raise ValueError

        return self.room[x][y] >= 1

    def pickup_dust(self, pos: tuple):
        """Picking up dust in room

        :param pos: (x, y) coordinates
        """
        x, y = pos

        if self.has_dust(pos):
            self.room[x][y] -= 1

    def is_clean(self) -> True or False:
        """Checks if room is clean

        :return: True if there's no dust in the room False otherwise
        """
#         for line in self.room:
#             for dust_count in line:
#                 if dust_count != 0:
#                     return False
        return all(dust_count == 0 for line in self.room for dust_count in line)


class VacuumCleaner:
    def __init__(self, start_pos: tuple, room: Room):
        """Constructor

        :param start_pos: (x, y) coordinates where VacuumCleaner starts
        :param room: subclass for Room
        """
        self.current_position = start_pos
        self.possible_directions = ['N', 'E', 'S', 'W']
        self.room = room

    def move(self, direction: str):
        """Moves the vacuum cleaner:

        - If there's dust on the vacuum's current position, do not move it
        - Otherwise compute the new position's coordinate based on direction
        - If the room has position with the new coordinates, move the vacuum

        :param direction: should be a single letter (N, E, S, or W)
        """
        if direction not in self.possible_directions:
            raise ValueError

        if self.room.has_dust(self.current_position):
            self.room.pickup_dust(self.current_position)
            return

        new_x, new_y = self.current_position

        if direction == "N":
            new_x -= 1

        if direction == "S":
            new_x += 1

        if direction == "W":
            new_y -= 1

        if direction == "E":
            new_y += 1

        if self.room.has_position((new_x, new_y)):
            self.current_position = (new_x, new_y)


def simulate_cleaning(room_dimensions: tuple, dust_count: int, simulation_no: int) -> list[int]:
    """Method runs simulation_no number of simulations
    the vacuum cleaner moves randomly in the room

    :param room_dimensions: x, y coordinates(size of room)
    :param dust_count: count of dust on the floor
    :param simulation_no: number of simulations
    :return: list of integers -- the number of steps it takes to clean a room
    """

    all_steps = list()
    width, length = room_dimensions
    for _ in range(simulation_no):
        room = Room(width, length)
        room.add_dust(dust_count)

        vacuum_start = (random.randint(0, width - 1), random.randint(0, length - 1))
        vacuum = VacuumCleaner(vacuum_start, room)

        number_of_steps = 0

        while not room.is_clean():
            vacuum.move(random.choice(vacuum.possible_directions))
            number_of_steps += 1

        all_steps.append(number_of_steps)

    return all_steps


def main():
    """Tests the distribution of the number of steps it takes to clean the room

    Sample call of simulate_cleaning

    :return: Histogram that prints number of all steps in each simulation
    """

    simulations_step_counts = simulate_cleaning((5, 3), 50, 50)

    plt.hist(simulations_step_counts)
    plt.title("Vacuum steps count distribution")
    plt.xlabel("Steps count")
    plt.ylabel("Simulations count")
    plt.show()

    # Looks like an F-distribution


if __name__ == '__main__':
    main()
