#
# This is the program's UI module. The user interface and all interaction with the user (print and input statements) are found here
#
import sys
from Backend import Database
import Frontend.functions as ui_func
import texttable as tt
from re import *

def add_command():
    pass



def __pretty_print(list):
    table = tt.Texttable()
    table.set_cols_align(["l", "c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m", "m"])
    ls = [["Participant", "Problem 1", "Problem 2", "Problem 3", "Average"]]
    for entry in list:
        ls.append([entry["id"], entry["p1"], entry["p2"], entry["p3"], (entry["p1"]+entry["p2"]+entry["p3"])/3])
    table.add_rows(ls)
    print(table.draw())



def Menu():
    importing_commands = False
    if len(sys.argv) == 2:
        importing_commands = True
    options = {
        "add": {"syntax": "add <P1 score> <P2 score> <P3 score>", "description": "Adds a participant to the list"},
        "list": {"syntax": "list", "description": "Lists all participants"},
        "list_comp": {"syntax": "list [ < | = | > ] <score>",
                      "description": "Lists all participants compared by a threshold"},
        "list_sort": {"syntax": "list sorted", "description": "Lists all participants sorted descending by average"},
        "insert": {"syntax": "insert <P1 score> <P2 score> <P3 score> at <position>",
                   "description": "Inserts a participant into the list at the given position"},
        "remove": {"syntax": "remove <position>",
                   "description": "Removes a participant from the list"},
        "remove_to": {"syntax": "remove <start position> to <end position>",
                      "description": "Removes a participants from between <start position> and <end position>"},
        "remove_comp": {"syntax": "remove [ < | = | > ] <score>",
                        "description": "Removes all participants compared by a threshold"},
        "top": {"syntax": "top <number>", "description": "Prints the top n participants"},
        "top_spec": {"syntax": "top <number> <p1 | p2 | p3>",
                     "description": "Prints the top n participants of the specified problem"},
        "undo": {"syntax": "undo", "description": "Undoes the last command"},
    }
    if importing_commands:
        file = open(sys.argv[1], "r")

    while True:
        print("")
        _command = ""
        if importing_commands:
            try:
                _command = file.readline()
                if _command == "EOF":
                    raise EOFError
            except EOFError:
                file.close()
                print("Imported commands successfully")
                importing_commands = False
        else:
            _command = input()


        words = split(r"[,.]?\s+", _command)
        if words[0] == "add":
            try:
                p1,p2,p3 = float(words[1]),float(words[2]),float(words[3])
            except IndexError:
                print("fatal: argument missing")
                print("usage: "+options["add"]["syntax"])
                continue
            except ValueError:
                print("fatal: scores must be numbers" )
                print("usage: "+options["add"]["syntax"])
                continue

            Database.add_participant(p1,p2,p3)
            print("Added participant with scores {0}, {1}, {2}".format(p1,p2,p3))

        elif words[0] == "list" or words[0] == "ls":
            keys = ["list", "list_sort", "list_comp"]

            if len(words) == 1:
                __pretty_print(Database.get_list())
                continue


            if words[1] == "sorted":
                sorted_list = ui_func.sort_list(Database.get_list())
                __pretty_print(sorted_list)
                continue

            # else
            charmap = ['<','=','>']
            if not words[1] in charmap:
                print("syntax error")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            try:
                score = float(words[2])
            except ValueError:
                print("fatal: scores must be numbers")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue
            except IndexError:
                print("fatal: argument missing")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            __pretty_print(
                ui_func.comp_list(
                    Database.get_list(), words[1], score
            ))





        elif words[0] == "insert":
            try:
                p1,p2,p3 = float(words[1]),float(words[2]),float(words[3])
            except IndexError:
                print("fatal: argument missing")
                print("usage: "+options["insert"]["syntax"])
                continue
            except ValueError:
                print("fatal: scores must be numbers" )
                print("usage: "+options["insert"]["syntax"])
                continue



            try:
                if words[4] != "at":
                    print("syntax error")
                    print("usage: "+options["insert"]["syntax"])
                    continue
            except IndexError:
                print("fatal: argument missing")
                print("usage: "+options["insert"]["syntax"])
                continue

            try:
                index = int(words[5])
            except ValueError:
                print("fatal: index must be an integer")
                print("usage: "+options["insert"]["syntax"])
                continue
            except IndexError:
                print("fatal: no index was given")
                print("usage: "+options["insert"]["syntax"])
                continue

            try:
                Database.add_participant(p1,p2,p3,index)
                print("Added participant with index {0} and scores {1}, {2}, {3}".format(index, p1,p2,p3))
                continue
            except IndexError:
                print("fatal: index out of range")
                print("usage: "+options["insert"]["syntax"])
                continue

        elif words[0] == "remove" or words[0] == "rm":
            keys = ["remove", "remove_to", "remove_comp"]
            charmap = ['<','=','>']

            cond = False
            if len(words) == 1:
                print("fatal: argument missing")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            if not words[1] in charmap:
                cond = True

            if not cond:
                try:
                    score = float(words[2])
                except ValueError:
                    print("fatal: scores must be numbers")
                    usage_txt = "usage: "
                    for key in keys:
                        print(usage_txt, options[key]["syntax"])
                        usage_txt = "       "
                    continue
                except IndexError:
                    print("fatal: argument missing")
                    usage_txt = "usage: "
                    for key in keys:
                        print(usage_txt, options[key]["syntax"])
                        usage_txt = "       "
                    continue

                indices_to_rm = ui_func.get_indices_of_comp(Database.get_list(), words[1], score)
                print(indices_to_rm)
                Database.remove_entries_by_indices(indices_to_rm)
                print("Removed participants with averages {0} than {1}".format(words[1], score))
                continue

            try:
                begin = int(words[1])
            except IndexError:
                print("fatal: argument missing")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            except ValueError:
                print("fatal: index must be an integer")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            if len(words) == 2:
                Database.remove_entries(begin)
                print("Removed participant with index {0}".format(begin))
                continue

            # else

            if words[2] != "to":
                print("syntax error")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            try:
                end = int(words[3])
            except IndexError:
                print("fatal: argument missing")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            except ValueError:
                print("fatal: index must be an integer")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            Database.remove_entries(begin,end)
            print("Removed participants between {0} and {1} ".format(begin,end))
            continue

        elif words[0] == "undo" or words[0] == "u":
            Database.undo()

        elif words[0] == "top":
            keys = ["top", "top_spec"]

            try:
                number = int(words[1])
            except ValueError:
                print("fatal: argument must be an integer")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue
            except IndexError:
                print("fatal: argument missing")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            if len(words) < 3:
                sorted_list = ui_func.sort_list(Database.get_list())
                sorted_list = sorted_list[:number]
                __pretty_print(sorted_list)
                continue

            charmap = ['p1','p2','p3']
            if not words[2] in charmap:
                print("fatal: argument missing")
                usage_txt = "usage: "
                for key in keys:
                    print(usage_txt, options[key]["syntax"])
                    usage_txt = "       "
                continue

            sorted_list = ui_func.sort_list_by_problem(Database.get_list(), words[2])
            sorted_list = sorted_list[:number]
            __pretty_print(sorted_list)

        elif words[0] == "help":
            help_list = {"add": ["add"],
                         "insert": ["insert"],
                         "list":["list", "list_comp", "list_sort"],
                         "remove": ["remove", "remove_to", "remove_comp"],
                         "top": ["top", "top_spec"],
                         "undo": ["undo"]
                         }

            tab = "    "
            for title in help_list:
                print("command: "+title)
                parent = help_list[title]
                for option in parent:
                    print(tab+options[option]["description"])
                    print(tab+"syntax:"+tab+options[option]["syntax"])
                    print()
                print("---------------------------------------")
        elif words[0] == "exit":
            return 0






