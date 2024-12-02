from enum import Enum
from typing import Generator

class Direction(Enum):
    SAME = 0
    DECREASING = -1
    INCREASING = 1

class FilterMode(Enum):
    SAFE = 1,
    UNSAFE = 2

class UnsafeException(Exception):
    pass

def filter_reports(reports: list[list[int]], safe_threshold: int = 0, filter_mode: FilterMode = FilterMode.SAFE) -> Generator[list[int], None, None]:
    max_diff = 3

    for levels in reports:
        previous = None
        direction = None
        unsafe_counter = 0
        for level in levels:
            try:
                # no change, so it's definitely unsafe
                if previous == level:
                    raise UnsafeException

                diff = 0
                # Calculate diff only if we got a previous value
                if previous is not None:
                    diff = level - previous

                # diff exceeds max_diff, so it's unsafe
                if abs(diff) > max_diff:
                    raise UnsafeException

                # determine direction if we got a previous value already
                if previous is not None and direction is None:
                    # Diff > 0 means the current level is higher than the previous, therefore it must be increasing
                    if diff > 0:
                        direction = Direction.INCREASING
                    else:
                        direction = Direction.DECREASING

                # Increasing levels but the diff was less than 0 (meaning previous was higher than current) -> Unsafe
                if direction == Direction.INCREASING and diff < 0:
                    raise UnsafeException

                # Decreasing levels but the diff was greater than 0 (meaning previous was lower than current) -> Unsafe
                if direction == Direction.DECREASING and diff > 0:
                    raise UnsafeException

            except UnsafeException:
                unsafe_counter += 1
            finally:
                # Using a finally block ensures that the previous level gets updated
                previous = level

        # If we want only safe reports, the unsafe_counter must not exceed the safe_threshold
        if filter_mode is FilterMode.SAFE and unsafe_counter <= safe_threshold:
            yield levels
        # It's the opposite if we want unsafe reports
        elif filter_mode is FilterMode.UNSAFE and unsafe_counter > safe_threshold:
            yield levels

def filter_safe(reports: list[list[int]], safe_threshold: int = 0):
    return filter_reports(reports, safe_threshold, FilterMode.SAFE)

def filter_unsafe(reports: list[list[int]], safe_threshold: int = 0):
    return filter_reports(reports, safe_threshold, FilterMode.UNSAFE)

def parse_input() -> list[list[int]]:
    reports = []

    # Read the input file. It's rows of whitespace seperated ints
    with open("input.txt") as f:
        for line in f:
            levels = list(map(int, line.split()))
            reports.append(levels)

    return reports

if __name__ == '__main__':
    reports = parse_input()

    # Part 1
    safe_reports = list(filter_safe(reports))
    print(f"Count of safe reports: {len(safe_reports)}")

    # Part 2
    safe_threshold = 1
    safe_reports = list(filter_safe(reports, safe_threshold))
    print(f"Count of safe reports with safe_threshold = {safe_threshold}: {len(safe_reports)}")
