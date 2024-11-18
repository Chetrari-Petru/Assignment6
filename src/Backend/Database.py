
__the_list = []
__ids = 0
__unused_ids = []


__history = []


def __gen_id() -> int:
    global __ids
    if len(__unused_ids) == 0:
        __ids += 1
        return __ids
    return __unused_ids.pop()


def __write_history() -> None:
    """
    Keeps track of the operations done on the list
    """
    global __the_list
    global __history

    __history.append(__the_list.copy())


def undo() -> None:
    """
    Undoes the last operation done on the list
    """
    global __the_list
    global __history


    __history.pop()
    __the_list = [] if len(__history) == 0 else __history[-1].copy()

def add_participant(p1: float, p2: float, p3: float, index:int = -1) -> None:
    """
    Adds a participant to the list
    :param p1: Score of first problem
    :param p2: Score of second problem
    :param p3: Score of third problem
    :param index: Index to insert at
    :return: Nothing

    Use -1 as index to append at the end of the list
    """
    global __the_list
    if index >= len(__the_list):
        raise IndexError("Index out of range")
    if index == -1:
        index = len(__the_list)+1
    __the_list.insert(
        index,
        {"id": __gen_id(),
         "p1": p1,
         "p2": p2,
         "p3": p3}
    )
    __write_history()

def get_list() -> list:
    """
    Returns the list of all participants
    :return: The list of all participants
    """
    global __the_list
    return __the_list.copy()


def remove_index(index: int) -> None:
    """
    Removes the value of the index from the list
    :param index: The position of the participant in the list
    :return: Nothing
    """
    global __the_list
    del __the_list[index]
    __write_history()

def __find_index_by_id(id: int) -> int:
    """
    Returns the index of the participant with the given id
    :param id: the id of the participant
    :return: The index of the participant with the given id or -1 if it doesn't exist
    """
    global __the_list
    for i in __the_list:
        if i["id"] == id:
            return i["id"]
    return -1

def replace_score(id:int, problem:int, score: float) -> None:
    """
    Replaces the score of the participant with the given id at the given problem
    :param id: The id of the participant
    :param problem: The problem of which score to replace
    :param score: The score of said problem
    :return: Nothing
    """

    map = [None, "P1", "P2", "P3"]
    if problem < 1 or problem > 3 :
        raise IndexError("param problem must be between 1 and 3")

    index = __find_index_by_id(id)
    __the_list[index][map[problem]] = score
    __write_history()

def remove_entries(start: int, end: int = -1) -> None:
    """
    Removes entries between indices start and end
    :param start: the start position of removed entries
    :param end: the end position of removed entries
    :return: Nothing

    if only start is given, then it deletes the element with the given index
    """
    global __the_list
    global __unused_ids
    if end == -1:
        end = start

    beg = __the_list[:start]
    fin = __the_list[end+1:]
    for p in __the_list[start: end+1]:
        __unused_ids.append(p["id"])
    __the_list =  beg+fin
    __write_history()

def remove_entries_by_ids(ids: list) -> None:
    """
    Removes all entries with the given ids
    :param ids: a list of ids
    :return: Nothing

    it ignores non-valid ids
    """

    global __the_list
    offset = 0
    for i in ids:
        index = __find_index_by_id(i)
        index -= offset
        if index != -1:
            __the_list.pop(index)
            offset += 1
    __write_history()



def remove_entries_by_indices(indices: list) -> None:
    """
    Removes all entries with the given indices
    :param ids: a list of indices
    :return: Nothing
    """

    global __the_list
    offset = 0
    for index in indices:
        index -= offset
        if index != -1:
            __the_list.pop(index)
            offset += 1
    __write_history()