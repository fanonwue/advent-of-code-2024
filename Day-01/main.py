def total_distance(list_a: list[int], list_b: list[int]) -> int:
    # Make sure the lists are sorted so that we can match the correct elements
    list_a.sort()
    list_b.sort()

    # Create pairs to be able to calculate their relative distance
    pairs = []
    for i in range(len(list_a)):
        pairs.append((list_a[i], list_b[i]))

    print(pairs)

    # Calculate total distance based off the pairs
    distance = 0
    for (a, b) in pairs:
        distance += abs(a - b)

    return distance

def similarity_score(list_a: list[int], list_b: list[int]) -> int:
    # Create a dict to hold the number of occurrences of each number
    # Since a dict is basically a hashmap, reading from it should be fast
    # There is also the list_b.count(e) function, but using it would
    # increase runtime to O(n^2) from the current O(n)
    count_in_b = {}
    for e in list_b:
        # Get the current count or 0 if the element hasn't been added yet
        current_count = count_in_b.get(e, 0)
        count_in_b[e] = current_count + 1

    # The similarity gets calculated by adding up the result of multiplying each element with its occurrence count
    similarity = 0
    for e in list_a:
        similarity += e * count_in_b.get(e, 0)

    print(count_in_b)

    return similarity


def parse_input(path: str = "input.txt") -> tuple[list[int], list[int]]:
    list_a = []
    list_b = []

    # Read the input file. It's two columns of ints seperated by whitespace
    with open(path) as f:
        for line in f:
            a, b = line.split()
            list_a.append(int(a))
            list_b.append(int(b))

    return list_a, list_b

if __name__ == '__main__':
    list_a, list_b = parse_input()
    assert len(list_a) == len(list_b), "lists have different length"

    distance = total_distance(list_a, list_b)
    print(f"Total distance: {distance}\n")

    similarity = similarity_score(list_a, list_b)
    print(f"Similarity score: {similarity}\n")
