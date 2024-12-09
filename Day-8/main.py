from typing import Dict

Positions = Dict[str, list[tuple[int, int]]]
Distances = Dict[tuple[int, int], list[tuple[int, int]]]

def get_positions(rows: list[str]) -> Positions:
    positions: Positions = {}

    # Find all antennas and map them to their frequency
    # The resulting dict has a str key that represents the frequency, and the value is a list tuples that represent
    # the X and Y coordinates of each antenna with that frequency
    for x, row in enumerate(rows):
        for y, c in enumerate(row):
            # valid frequencies are always alphanumerical characters
            if c.isalnum():
                positions.setdefault(c, [])
                positions[c].append((x, y))
    return positions

def get_distances(positions: Dict[str, list[tuple[int, int]]]) -> Distances:
    distances: Distances = {}

    # Calculate the distance between all antennas of a given frequency
    # The resulting dict will have a map of all antennas mapped to a list of distances (X and Y)
    # These distances are the distance between the antenna in the key and all other antennas that have the same frequency
    for pos_list in positions.values():
        for pos in pos_list:
            for j in range(len(pos_list)):
                dis = ((pos[0] - pos_list[j][0]), (pos[1] - pos_list[j][1]))
                distances.setdefault(pos, [])
                if dis != (0, 0):
                    distances[pos].append(dis)
    return distances

def get_antinode_positions(distances: Distances, inline: bool = False) -> set[tuple[int, int]]:
    is_in_field = lambda x, y: 0 <= x < len(rows) and 0 <= y < len(rows[x])

    # Create a set to save our antinode positions to
    # There can be multiple antinodes at a position, but we only need it once
    antinodes: set[tuple[int, int]] = set()
    for pos, dis_list in distances.items():
        for dis in dis_list:
            x, y = pos[0] + dis[0], pos[1] + dis[1]

            # For Part 1, we only want the one antinode per direction, so we continue the loop after checking the first one
            # without executing the rest
            if not inline:
                if is_in_field(x, y):
                    antinodes.add((x, y))
                continue

            # For Part 2, we want all antinodes within the line
            x, y = pos[0], pos[1]
            while is_in_field(x, y):
                antinodes.add((x, y))
                # Move to the next positions in the line
                x += dis[0]
                y += dis[1]

    # Only return a unique set of antinodes
    return antinodes


def parse_input(path: str = "input.txt") -> list[str]:
    rows = []

    # Read the input file. It's a matrix of antennas with different frequencies
    with open(path) as f:
        for line in f:
            rows.append(line.strip())

    return rows

if __name__ == '__main__':
    rows = parse_input()
    positions = get_positions(rows)
    distances = get_distances(positions)

    # Part 1
    antinode_positions = get_antinode_positions(distances)
    print(f"Antinodes found: {len(antinode_positions)}")

    # Part 2
    inline_antinode_positions = get_antinode_positions(distances, inline=True)
    print(f"Inline Antinodes found: {len(inline_antinode_positions)}")