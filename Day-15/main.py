from Robot import Robot
from util import ParsedMap, Direction, Point, Mode

mode = Mode.PART_ONE

class Input:
    def __init__(self, parsed_map: ParsedMap, directions: list[Direction], robot: Robot):
        self.parsed_map = parsed_map
        self.directions = directions
        self.robot = robot

def get_new_position(start: Point, direction: Direction) -> Point:
    new_x, new_y = start[0], start[1]
    match direction:
        case Direction.UP: new_y -= 1
        case Direction.DOWN: new_y += 1
        case Direction.LEFT: new_x -= 1
        case Direction.RIGHT: new_x += 1
    return new_x, new_y

def calc_gps(parsed_map: ParsedMap) -> int:
    sum = 0
    for y in range(0, len(parsed_map)):
        row = parsed_map[y]
        for x in range(0, len(row)):
            cell = parsed_map[y][x]

            if cell == 'O':
                sum += (100 * y) + x
    return sum



def move(robot: Robot, parsed_map: ParsedMap, direction: Direction):
    global mode
    new_position = get_new_position(robot.pos(), direction)
    x, y = new_position
    target_cell_value = parsed_map[y][x]


    match target_cell_value:
        case '.': robot.move_to(new_position)
        # It's a wall, we can't move
        case '#': return
        # A box
        case 'O':
            assert mode is Mode.PART_ONE, "only part 1 should have this value"
            move_boxes(robot, new_position, parsed_map, direction)
        case '['|']':
            assert mode is Mode.PART_TWO, "only part 2 should have this value"
        case _:
            print(f"ERROR: unknown cell type: {target_cell_value}")

def get_moveable_boxes(current_pos: Point, box_stack: list[Point], parsed_map: ParsedMap, direction: Direction):
    pass


def move_boxes(robot: Robot, box_pos: Point, parsed_map: ParsedMap, direction: Direction):
    box_stack = [box_pos]

    can_move = False
    current_pos: Point = box_pos[0], box_pos[1]

    while True:
        new_x, new_y = get_new_position(current_pos, direction)
        next_cell_value = parsed_map[new_y][new_x]

        match next_cell_value:
            # a wall, can't move
            case '#': return
            case '.':
                can_move = True
                box_stack.append((new_x, new_y))
            case 'O':
                box_stack.append((new_x, new_y))

        current_pos = (new_x, new_y)

        if can_move:
            break

    if can_move:
        while len(box_stack) > 0:
            x, y = box_stack.pop()
            new_value = '.'
            if len(box_stack) > 0:
                new_value = 'O'
            parsed_map[y][x] = new_value

        robot.move_to(box_pos)

def parse_input(path: str = "input.txt") -> Input:
    global mode
    parsed_map: ParsedMap = []
    directions: list[Direction] = []
    robot = Robot(0, 0)

    # Read the input file. The first half (separated by an empty line) is the map, the 2nd part the list of directions
    # the robot will follow
    with open(path) as f:
        file_iter = iter(f)
        # Read the map
        for y, line in enumerate(file_iter):
            # This is the empty line separating the map from the movement
            if line == "\n":
                break

            new_row = []
            for x, cell in enumerate(line):
                if mode is Mode.PART_ONE:
                    parsed = parse_cell_part_one((x, y), cell, robot)
                    if parsed is not None:
                        new_row.append(parsed)
                else:
                    parsed = parse_cell_part_two((x, y), cell, robot)
                    if parsed is not None:
                        new_row.extend(parsed)
            parsed_map.append(new_row)

        for line in file_iter:
            new_directions = [Direction(direction) for direction in line.strip("\n")]
            directions.extend(new_directions)

    return Input(parsed_map, directions, robot)

def parse_cell_part_one(pos: Point, cell: str, robot: Robot) -> str|None:
    match cell:
        case "\n": return None
        case '@':
            print(f"Robot is at initial position {pos}")
            robot.move_to(pos)
            cell = '.'
    return cell

def parse_cell_part_two(pos: Point, cell: str, robot: Robot) -> list[str]|None:
    row = []
    match cell:
        case "\n": return None
        case '#':
            row.append('#')
            row.append('#')
        case '.':
            row.append('.')
            row.append('.')
        case 'O':
            row.append('[')
            row.append(']')
        case '@':
            row.append('.')
            row.append('.')
            pos = pos[0] * 2, pos[1]
            print(f"Robot is at initial position {pos}")
            robot.move_to(pos)
            cell = '.'
    return row

if __name__ == '__main__':
    # Part 1
    print("---- PART ONE ----")
    mode = Mode.PART_ONE
    parsed_input = parse_input("input.txt")
    robot = parsed_input.robot
    directions = parsed_input.directions
    parsed_map = parsed_input.parsed_map

    for direction in parsed_input.directions:
        move(robot, parsed_map, direction)

    result = calc_gps(parsed_map)
    print(f"GPS sum for part 1: {result}")

    # Part 2
    print("\n---- PART TWO ----")
    mode = Mode.PART_TWO
    parsed_input = parse_input("sample_input.txt")
    robot = parsed_input.robot
    directions = parsed_input.directions
    parsed_map = parsed_input.parsed_map

    print(parsed_map)