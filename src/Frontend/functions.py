#
# The program's functions are implemented here. There is no user interaction in this file, therefore no input/print statements. Functions here
# communicate via function parameters, the return statement and raising of exceptions. 
#

def sort_list(the_list:list) -> list:
    """
    Sorts participants in decreasing order by average.
    :param the_list: the list of participants
    :return: the sorted list
    """
    for i in range(len(the_list)):
        the_list[i]["average"] = (the_list[i]["p1"] + the_list[i]["p2"] + the_list[i]["p3"]) / 3

    for i in range(len(the_list)-1):
        for j in range(i, len(the_list)):
            if the_list[i]["average"] < the_list[j]["average"]:
                swap = the_list[i]
                the_list[i] = the_list[j]
                the_list[j] = swap

    return the_list


def __lt(this, other):
    return this.__lt__(other)

def __gt(this, other):
    return this.__gt__(other)

def __eq(this, other):
    return this.__eq__(other)

def comp_list(the_list: list, mode: str, threshold: float) -> list:
    """
    Returns the elements above, below or equal to the threshold, depending on mode
    :param the_list: the list to be filtered
    :param mode: <, = or >
    :param threshold: the threshold
    :return: the filtered list
    """

    mode_map = {
        '<': __lt,
        '>': __gt,
        '=': __eq,
    }
    for i in range(len(the_list)):
        the_list[i]["average"] = round((the_list[i]["p1"] + the_list[i]["p2"] + the_list[i]["p3"]) / 3, 3)

    threshold = round(threshold, 3)
    i = 0
    while i < len(the_list):
        print(the_list[i]["average"])
        if not mode_map[mode](the_list[i]["average"], threshold):
            the_list.pop(i)
        else:
            i += 1

    return the_list

def get_indices_of_comp(the_list:list, mode: str, threshold: float) -> list:
    """
    gets all the indices of elements above, below or equal to the threshold, depending on mode
    :param the_list: the list to be filtered
    :param mode: <, = or >
    :param threshold: the threshold
    :return: the list of indices to be removed
    """

    mode_map = {
        '<': __lt,
        '>': __gt,
        '=': __eq,
    }

    indices = []

    for i in range(len(the_list)):
        the_list[i]["average"] = round((the_list[i]["p1"] + the_list[i]["p2"] + the_list[i]["p3"]) / 3, 3)

    threshold = round(threshold, 3)
    for index in range(len(the_list)):
        if mode_map[mode](the_list[index]["average"], threshold):
            indices.append(index)

    return indices


def sort_list_by_problem(the_list:list, problem:str) -> list:
    """
    sorts the list descending by with respect to scores of the given problem
    :param the_list: the list to be sorted
    :param problem: the problem to sort by
    :return: the sorted list
    """

    print(problem)
    for i in range(len(the_list)-1):
        for j in range(i, len(the_list)):
            if the_list[i][problem] < the_list[j][problem]:
                swap = the_list[i]
                the_list[i] = the_list[j]
                the_list[j] = swap

    print(the_list)

    return the_list