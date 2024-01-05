class InvalidArgumentError(Exception):
    def __init__(self):
        self.message = 'Argument passed is not a tuple or range.'
        super().__init__(self.message)


class InvalidTupleError(Exception):
    def __init__(self):
        self.message = 'The tupple passed contains more then 2 values, contains a non-numeric value or the first number is higher then the second.' # noqa
        super().__init__(self.message)


class InvalidRangeError(Exception):
    def __init__(self):
        self.message = 'The passed range is invalid.'
        super().__init__(self.message)


class InvalidIntersectionError(Exception):
    def __init__(self):
        self.message = 'The provided intersection contains a non-numeric item, contains more then 2 items or the beginning value is higher then the end value.' # noqa


class NoneRangeError(Exception):
    def __init__(self):
        self.message = 'The arguments passed do not form a range'
        super().__init__(self.message)


def check_valid(source: tuple | range, destination: tuple | range):

    # check if passed argument is a tuple or range
    if isinstance(source, tuple) is True:
        # check if tuple is valid
        if all(isinstance(item, int) for item in source) is False or len(source) > 2 or source[0] > source[1]:
            raise InvalidTupleError

    elif isinstance(source, range) is True:
        source_tuple = tuple(source)
        if source_tuple == ():
            raise InvalidRangeError
        source = (source_tuple[0], source_tuple[-1] + 1)
    else:
        raise InvalidArgumentError

    if isinstance(destination, tuple) is True:
        if all(isinstance(item, int) for item in destination) is False or len(destination) > 2 or destination[0] > destination[1]: # noqa
            raise InvalidTupleError

    elif isinstance(destination, range) is True:
        destination_tuple = tuple(destination)
        if destination_tuple == ():
            raise InvalidRangeError
        destination = (destination_tuple[0], destination_tuple[-1] + 1)

    else:
        raise InvalidArgumentError

    return source, destination


def check_valid_intersection(intersection: tuple | range):
    if isinstance(intersection, tuple) is True:
        if all(isinstance(item, int) for item in intersection) is False or len(intersection) > 2 or intersection[0] > intersection[1]:  # noqa
            raise InvalidIntersectionError
    elif isinstance(intersection, range) is True:
        intersection_tuple = tuple(intersection)
        if intersection_tuple == ():
            raise InvalidIntersectionError
        else:
            intersection = (intersection_tuple[0], intersection_tuple[-1] + 1)
    else:
        raise InvalidArgumentError
    return intersection


def find_values(source: tuple | range, destination: tuple | range, return_value: str):
    source_lowest, source_highest = source
    destination_lowest, destination_highest = destination
    remainders = []

    # for more info on cases see cases.txt

    # case 1.1
    if source_lowest == destination_lowest and source_highest > destination_highest:
        intersection = (destination_lowest, destination_highest)
        remainders.append((destination_highest, source_highest))

    # case 1.2
    elif source_lowest < destination_lowest and source_highest > destination_highest:
        intersection = (destination_lowest, destination_highest)
        remainders.append((source_lowest, destination_lowest))
        remainders.append((destination_highest, source_highest))

    # case 1.3
    elif source_lowest < destination_lowest and source_highest == destination_highest:
        intersection = (destination_lowest, destination_highest)
        remainders.append((source_lowest, destination_lowest))

    # case 2
    elif destination_lowest < source_lowest and destination_highest > source_highest:
        intersection = (source_lowest, source_highest)

    # case 3
    elif source_lowest == destination_lowest and source_highest < destination_highest:
        intersection = (source_lowest, source_highest)

    # case 4
    elif destination_lowest < source_lowest and destination_highest == source_highest:
        intersection = (source_lowest, source_highest)

    # case 5
    elif source_lowest < destination_lowest < source_highest and source_highest > destination_lowest:
        intersection = (destination_lowest, source_highest)
        remainders.append((source_lowest, destination_lowest))

    # case 6
    elif destination_lowest < source_lowest < destination_highest < source_highest:
        intersection = (source_lowest, destination_highest)
        remainders.append((destination_highest, source_highest))

    # case 7
    elif destination_lowest == source_lowest and destination_highest == source_highest:
        intersection = (source_lowest, source_highest)

    # case 8
    else:
        intersection = None
        remainders.append((source_lowest, source_highest))

    if return_value == 'intersection':
        return intersection
    elif return_value == 'remainders':
        return remainders
    elif return_value == 'both':
        return intersection, remainders


def transform_existing_intersection(intersection: tuple | range, value_to_add: int):
    """Transform an existing intersection with a value"""
    if not intersection:
        return None
    else:
        intersection = check_valid_intersection(intersection)
        new_intersection = (intersection[0] + value_to_add, intersection[1] + value_to_add)
        return new_intersection


def transform_new_intersection(source: tuple | range, destination: tuple | range, value_to_add: int):
    """Find a new itersection using two ranges and transform it with a value"""
    source, destination = check_valid(source, destination)
    intersection = find_values(source, destination, 'intersection')
    if not intersection:
        return None
    else:
        new_intersection = (intersection[0] + value_to_add, intersection[1] + value_to_add)
        return new_intersection


def find_intersection(source: tuple | range, destination: tuple | range):
    """Get the intersection of two ranges"""
    source, destination = check_valid(source, destination)
    intersection = find_values(source, destination, 'intersection')
    return intersection


def find_remainders(source: tuple | range, destination: tuple | range):
    """Get the remainder of the source when you remove the intersection"""
    source, destination = check_valid(source, destination)
    remainders = find_values(source, destination, 'remainders')
    return remainders


def find_intersection_and_remainders(source: tuple | range, destination: tuple | range):
    """Get both the intersection and remainders of two ranges"""
    source, destination = check_valid(source, destination)
    intersection, remainders = find_values(source, destination, 'both')
    return intersection, remainders
