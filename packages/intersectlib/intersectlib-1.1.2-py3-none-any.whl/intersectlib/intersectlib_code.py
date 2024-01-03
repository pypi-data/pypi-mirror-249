class InvalidArgumentError(Exception):
    def __init__(self):
        self.message = 'Argument passed is not a tuple or range.'
        super().__init__(self.message)


class InvalidTupleError(Exception):
    def __init__(self):
        self.message = 'The tupple passed contains more then 2 values, contains a non numeric value or the first number is higher then the second.' # noqa
        super().__init__(self.message)


class InvalidRangeError(Exception):
    def __init__(self):
        self.message = 'The passed range is invalid.'
        super().__init__(self.message)


class NoneRangeError(Exception):
    def __init__(self):
        self.message = 'The arguments passed do not form a range'
        super().__init__(self.message)


def check_valid(source, destination):
    # if source == destination:
    #     ra

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


def find_values(source, destination, return_value):
    source_lowest, source_highest = source
    destination_lowest, destination_highest = destination
    remainders = []

    # for more info on cases see cases.txt

    # case 1.1
    if source_lowest == destination_lowest and source_highest > destination_highest:
        print('1.1')
        intersection = (destination_lowest, destination_highest)
        remainders.append((destination_highest, source_highest))

    # case 1.2
    elif source_lowest < destination_lowest and source_highest > destination_highest:
        print('1.2')
        intersection = (destination_lowest, destination_highest)
        remainders.append((source_lowest, destination_lowest))
        remainders.append((destination_highest, source_highest))

    # case 1.3
    elif source_lowest < destination_lowest and source_highest == destination_highest:
        print('1.3')
        intersection = (destination_lowest, destination_highest)
        remainders.append((source_lowest, destination_lowest))

    # case 2
    elif destination_lowest < source_lowest and destination_highest > source_highest:
        print('2')
        intersection = (source_lowest, source_highest)

    # case 3
    elif source_lowest == destination_lowest and source_highest < destination_highest:
        print('3')
        intersection = (source_lowest, source_highest)

    # case 4
    elif destination_lowest < source_lowest and destination_highest == source_highest:
        print('4')
        intersection = (source_lowest, source_highest)

    # case 5
    elif source_lowest < destination_lowest and source_highest > destination_lowest:  # noqa
        print('5')
        intersection = (destination_lowest, source_highest)
        remainders.append((source_lowest, destination_lowest))

    # case 6
    elif destination_lowest < source_lowest and source_highest > destination_highest:
        print('6')
        intersection = (source_lowest, destination_highest)
        remainders.append((destination_highest, source_highest))

    # case 7
    elif destination_lowest == source_lowest and destination_highest == source_highest:
        print('7')
        intersection = (source_lowest, source_highest)

    # case 8
    else:
        print('8')
        intersection = None
        remainders.append((source_lowest, source_highest))

    if return_value == 'intersection':
        return intersection
    elif return_value == 'remainders':
        return remainders
    elif return_value == 'both':
        return intersection, remainders


def transform_intersection(source, destination, value_to_add):
    source, destination = check_valid(source, destination)
    intersection = find_values(source, destination, 'intersection')
    if not intersection:
        return None
    else:
        new_intersection = (intersection[0] + value_to_add, intersection[1] + value_to_add)
        return new_intersection


def find_intersection(source, destination):
    source, destination = check_valid(source, destination)
    intersection = find_values(source, destination, 'intersection')
    return intersection


def find_remainders(source, destination):
    source, destination = check_valid(source, destination)
    remainders = find_values(source, destination, 'remainders')
    return remainders


def find_intersection_and_remainders(source, destination):
    source, destination = check_valid(source, destination)
    intersection, remainders = find_values(source, destination, 'both')
    return intersection, remainders
