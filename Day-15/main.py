from Robot import Robot
from util import ParsedMap, Direction, Point, Mode
from copy import deepcopy
from functools import cmp_to_key

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
            cell = row[x]

            if cell == 'O' or cell == '[':
                # formular taken from task description
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
            move_boxes_p1(robot, parsed_map, direction, new_position)
        case '['|']':
            assert mode is Mode.PART_TWO, "only part 2 should have this value"
            moveable = get_moveable_boxes(parsed_map, direction, robot.pos(), [])
            if moveable:
                move_boxes_p2(robot, parsed_map, direction, moveable)
        case _:
            print(f"ERROR: unknown cell type: {target_cell_value}")

def get_moveable_boxes(parsed_map: ParsedMap, direction: Direction, current_pos: Point, box_stack: list[Point]) -> list[Point]|None:
    # The box_stack contains the start of a box, so the left side only


    new_position = get_new_position(current_pos, direction)
    new_x, new_y = new_position
    next_cell_value = parsed_map[new_y][new_x]

    if new_position == (8, 6):
        pass

    match next_cell_value:
        # can't move
        case '#': return None
        # Next cell is empty so we can move the boxes
        case '.': return box_stack


    if direction.is_vertical():
        match next_cell_value:
            case '[':
                # left side of a box
                # since we are on the left side of the box, we need to check the right side of the box
                # the target_pos now points to the right side of the box, as we need to check that one
                target_pos = new_x + 1, new_y

                # When encountering the left side of a box, we are already at the correct side of the box so we
                # need to save the boxes position directly to our stack.
                # Remember: Our stack only contains the left side of a box
                stack_entry = new_x, new_y
                new_stack = deepcopy(box_stack)
                new_stack.append(stack_entry)
                right_side_stack = get_moveable_boxes(parsed_map, direction, target_pos, new_stack)
                # If the right side did not hit a wall (did not return None), we need to check the left side as well
                if right_side_stack is not None:
                    # if we have the start (left side) of moveable boxes on the right side of the box, we continue with those in mind
                    return get_moveable_boxes(parsed_map, direction, new_position, right_side_stack)
                # right side hit a wall, so we can't move anything
                return None
            case ']':
                # right side of a box
                # target_pos points to the left side, as we need to check that as well
                target_pos = new_x - 1, new_y
                new_stack = deepcopy(box_stack)
                new_stack.append(target_pos)

                left_side_stack = get_moveable_boxes(parsed_map, direction, target_pos, new_stack)

                # If the left side did not hit a wall (did not return None), we need to check the right side as well
                if left_side_stack is not None:
                    return get_moveable_boxes(parsed_map, direction, new_position, left_side_stack)
                return None

    elif direction.is_horizontal():
        match next_cell_value:
            case '[':
                # we hit the left side of the box, meaning new_position points to the start of a box
                # we can only continue if we are moving into the correct direction
                # when hitting the left side of a box we need to move right to move it
                if direction is Direction.RIGHT:
                    target_pos = new_x + 1, new_y
                    # as our stack saves the start of boxes, we need to add new_position directly
                    stack_entry = new_x, new_y
                    new_stack = deepcopy(box_stack)
                    new_stack.append(stack_entry)
                    return get_moveable_boxes(parsed_map, direction, target_pos, new_stack)
            case ']':
                # we hit the right side of the box, meaning new_position points to the end of a box
                # we can only continue if we are moving into the correct direction
                # when hitting the right side of a box we need to move left to move it
                if direction is Direction.LEFT:
                    target_pos = new_x - 1, new_y
                    new_stack = deepcopy(box_stack)
                    # we need to move one step to the left to find the start of the box, so instead of new_position
                    # we save target_pos, which got moved already
                    new_stack.append(target_pos)
                    return get_moveable_boxes(parsed_map, direction, target_pos, new_stack)

    return box_stack


def move_boxes_p1(robot: Robot, parsed_map: ParsedMap, direction: Direction, box_pos: Point):
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
                # we found a free spot behind the box, meaning it can move
                can_move = True
                box_stack.append((new_x, new_y))
            case 'O':
                box_stack.append((new_x, new_y))

        current_pos = (new_x, new_y)

        if can_move:
            break

    if can_move:
        # We can move, so we can start moving all boxes into the direction we are going
        # We need to move the last box we found first to make room, so we use our list of boxes like a stack
        while len(box_stack) > 0:
            x, y = box_stack.pop()
            new_value = '.'
            if len(box_stack) > 0:
                new_value = 'O'
            parsed_map[y][x] = new_value

        robot.move_to(box_pos)

def move_boxes_p2(robot: Robot, parsed_map: ParsedMap, direction: Direction, moveable: list[Point]):
    # create a unique set of points as we can move a box only once
    box_stack = list(set(moveable))

    if len(box_stack) > 0:
        robot_new_pos = get_new_position(robot.pos(), direction)
        robot.move_to(robot_new_pos)

        def compare_box_stack(a: Point, b: Point) -> int:
            a_x, a_y = a
            b_x, b_y = b
            # We need to move the boxes in order. If there is a box at (1, 1) and another at (1, 2) and we are moving UP,
            # we have to first check whether we can move the box at the back (1, 1) before moving (1, 2)
            # as we can't move anything if the last box in that direction is blocked
            # The box at the front of the list is also the box directly in front of us
            match direction:
                case Direction.UP: return b_y - a_y
                case Direction.DOWN: return a_y - b_y
                case Direction.LEFT: return b_x - a_x
                case Direction.RIGHT: return a_x - b_x

        # Sort the stack based on the direction
        box_stack.sort(key=cmp_to_key(compare_box_stack))

    while len(box_stack) > 0:
        # Move the boxes in order, starting with the one at the back of the line we have to move
        x, y = box_stack.pop()
        match direction:
            # When moving up or down, we always assume that we hit the left side of the box
            case Direction.UP:
                parsed_map[y - 1][x] = '['
                parsed_map[y - 1][x + 1] = ']'
                parsed_map[y][x] = '.'
                parsed_map[y][x + 1] = '.'
            case Direction.DOWN:
                parsed_map[y + 1][x] = '['
                parsed_map[y + 1][x + 1] = ']'
                parsed_map[y][x] = '.'
                parsed_map[y][x + 1] = '.'
            case Direction.LEFT:
                parsed_map[y][x + 1] = '.'
                parsed_map[y][x] = ']'
                parsed_map[y][x - 1] = '['
            case Direction.RIGHT:
                parsed_map[y][x] = '.'
                parsed_map[y][x + 1] = '['
                parsed_map[y][x + 2] = ']'

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
    # for part 2, the grid has doubled width
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
            # a box is no longer a singular position, but instead has a start and an end
            row.append('[')
            row.append(']')
        case '@':
            row.append('.')
            row.append('.')
            # Adjust the robot position for the double width grid
            pos = pos[0] * 2, pos[1]
            print(f"Robot is at initial position {pos}")
            robot.move_to(pos)
    return row

if __name__ == '__main__':
    # Specify the input file to use
    # sample_input.txt contains the large example of this AoC task as found on the Day-15 website

    #input_file = "sample_input.txt"
    input_file = "input.txt"

    run_1 = True
    run_2 = True

    # Part 1
    if run_1:
        print("---- PART ONE ----")
        # set global mode to PART_ONE
        # this affects several functions
        mode = Mode.PART_ONE
        parsed_input = parse_input(input_file)
        robot = parsed_input.robot
        directions = parsed_input.directions
        parsed_map = parsed_input.parsed_map

        for direction in parsed_input.directions:
            move(robot, parsed_map, direction)

        result = calc_gps(parsed_map)
        print(f"GPS sum for part 1: {result}")

    # Part 2
    if run_2:
        print("\n---- PART TWO ----")
        mode = Mode.PART_TWO
        parsed_input = parse_input(input_file)
        robot = parsed_input.robot
        directions = parsed_input.directions
        parsed_map = parsed_input.parsed_map

        for direction in parsed_input.directions:
            move(robot, parsed_map, direction)

        result = calc_gps(parsed_map)
        print(f"GPS sum for part 2: {result}")