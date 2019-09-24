from __future__ import print_function
import sys
import re
# import traceback
# YOUR CODE GOES HERE
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2


def parse_line(line):

    line = line.strip()
    if len(line) == 0:
        raise Exception("empty input")
    command = line[0]

    # check the format of commmand a
    if command == 'a':
        r = re.match(r'a[\s]+[\"]{1}(([a-zA-Z]+[\s]*)+|([\s]+[a-zA-Z]*)+)[\"]{1}[\s]+([\(]{1}\s*[+-]?[0-9]+\s*\,\s*[+-]?[0-9]+\s*[\)]{1}\s*){2,}', line)
        if r is None:
            raise Exception("Wrong format")
        start, stop = r.span()
        if stop - start == len(line) :
            street_info = line[1:].strip()
            return command, street_info
        else:
            raise Exception("Wrong format")

    # check the format of command c
    elif command == 'c':
        r = re.match(r'c[\s]+[\"]{1}(([a-zA-Z]+[\s]*)+|([\s]+[a-zA-Z]*)+)[\"]{1}[\s]+([\(]{1}\s*[+-]?[0-9]+\s*\,\s*[+-]?[0-9]+\s*[\)]{1}\s*){2,}', line)
        if r is None:
            raise Exception("Wrong format")
        start, stop = r.span()
        if stop - start == len(line) :
            street_info = line[1:].strip()
            return command, street_info
        else:
            raise Exception("Wrong format")

    # check the format of command r
    elif command == 'r':
        r = re.match(r'r[\s]+[\"]{1}(([a-zA-Z]+[\s]*)+|([\s]+[a-zA-Z]*)+)[\"]{1}[\s]*', line)
        if r is None:
            raise Exception("Wrong format")
        start, stop = r.span()
        if stop - start == len(line) :
            street_info = line[1:].strip()
            return command, street_info
        else:
            raise Exception("Wrong format")

    # check the format of command g
    elif command == 'g':
        r = re.match(r'^g{1}$', line)
        if r is None:
            raise Exception("Wrong format")
        return command, None
    else:
        raise Exception("unknown commnad")

def format_coordinate(x, y):
    #check x
    if isinstance(x, (int, long)):
        pass
    elif x.is_integer():
        x = int(x)
    else:
        x = float("{0:.2f}".format(x))

    # check y
    if isinstance(y, (int, long)):
        pass
    elif y.is_integer():
        y = int(y)
    else:
        y = float("{0:.2f}".format(y))
    return x, y


def get_street_name(input_info):
    # get street name
    street_name_begin = input_info.find("\"")
    street_name_end = input_info.find("\"", street_name_begin + 1)
    street_name = input_info[street_name_begin + 1 : street_name_end]
    return street_name

def get_coordinates(input_info):
    coordinates_start = input_info.find('(')
    string_coordinates = input_info[coordinates_start:]

    r = re.compile(r'([\(]{1}\s*[+-]?[0-9]\s*\,\s*[+-]?[0-9]\s*[\)]{1}\s*)')
    list_coordinates = r.findall(string_coordinates)
    list_points = []
    for i in range(len(list_coordinates)):
        coordinate = eval(list_coordinates[i])
        newPoint = Point(coordinate[0], coordinate[1]);
        list_points.append(newPoint)

    return list_points

def street_is_existed(name, street_info_dict):
    return name in street_info_dict.keys()

def add_street(street_info, street_info_dict):
    street_name = get_street_name(street_info)
    list_points = get_coordinates(street_info)
    if (street_is_existed(street_name, street_info_dict)):
        raise Exception('"a" specified for a street that has already existed')

    else:
        street_info_dict[street_name] = list_points

def remove_street(street_info, street_info_dict):
    street_name = get_street_name(street_info)
    if (street_is_existed(street_name, street_info_dict)):
        del street_info_dict[street_name]
    else:
        raise Exception('"r" specified for a street that does not exist')

def change_street(street_info, street_info_dict):
    street_name = get_street_name(street_info)
    list_points = get_coordinates(street_info)
    if (street_is_existed(street_name, street_info_dict)):
        street_info_dict[street_name] = list_points
    else:
        raise Exception('"c" specified for a street that does not exist')


def add_to_edges(points_list, points_for_edges):
    # TODO if end-points == intersection points
    if (points_list[0].get_x() == points_list[1].get_x() and points_list[0].get_y() == points_list[1].get_y()):
        del points_list[0]

    if (points_list[-1].get_x() == points_list[1].get_x() and points_list[-1].get_y() == points_list[1].get_y()):
        del points_list[-1]

    if len(points_for_edges) == 0:
        points_for_edges.append(points_list)
    else:
        for i in range(len(points_for_edges)):
            if (points_for_edges[i][0].get_x() == points_list[0].get_x() and points_for_edges[i][0].get_y() == points_list[0].get_y() and points_for_edges[i][-1].get_x() == points_list[-1].get_x() and points_for_edges[i][-1].get_y() == points_list[-1].get_y()) or (points_for_edges[i][0].get_x() == points_list[-1].get_x() and points_for_edges[i][0].get_y() == points_list[-1].get_y() and points_for_edges[i][-1].get_x() == points_list[0].get_x() and points_for_edges[i][-1].get_y() == points_list[0].get_y()):
                intersection_x = points_list[1].get_x()
                intersection_y = points_list[1].get_y()
                for j in range(len(points_for_edges[i])):
                    if j >= 1 and j <= len(points_for_edges[i]) - 1:
                        if points_for_edges[i][j].get_x() == intersection_x:
                            if points_for_edges[i][j].get_y() == intersection_y:
                                return
                            elif intersection_y > points_for_edges[i][j].get_y():
                                if j != len(points_for_edges[i]) - 1:
                                    continue
                                else:
                                    points_for_edges[i].insert(j+1, points_list[1])
                                    return
                            else:

                                points_for_edges[i].insert(j, points_list[1])
                                return
                        elif intersection_x < points_for_edges[i][j].get_x():

                            points_for_edges[i].insert(j, points_list[1])
                            return
                        else:
                            if j != len(points_for_edges[i]) - 1:
                                continue
                            else:
                                points_for_edges[i].append(points_list[1])
                                return
            else:
                if i == len(points_for_edges) - 1:
                    points_for_edges.append(points_list)
                    break
                continue



def add_to_intersections_list(x, y, intersections_list):
    if len(intersections_list) == 0:
        intersections_list.append(Point(x, y))
    else:
        for i in range(len(intersections_list)):
            current_x = intersections_list[i].get_x()
            current_y = intersections_list[i].get_y()

            if (x == current_x):
                if (y == current_y):
                    break
                elif y > current_y:
                    if i != len(intersections_list) - 1:
                        continue
                    else:
                        intersections_list.insert(i+1, Point(x, y))
                        break
                else:
                    intersections_list.insert(i, Point(x, y))
                    break
            elif x < current_x:
                intersections_list.insert(i, Point(x, y))
                break
            else:
                if i == len(intersections_list) - 1:
                    intersections_list.append(Point(x, y))
                    break
                continue


def display_intersections_list(intersections_list, intersections_dict):
    reverse_intersections_dict = {}
    for id in range(len(intersections_list)):
        intersections_dict[id+1] = (intersections_list[id].get_x(), intersections_list[id].get_y())
        reverse_intersections_dict[intersections_list[id].get_x(), intersections_list[id].get_y()] = id + 1

    ss = 'V = {\n'
    for item in intersections_dict.items():
        ss += "  {:<4}({},{})\n".format(str(item[0]) + ':', item[1][0], item[1][1])
    ss += '}'

    return ss, reverse_intersections_dict

def find_edges(points_for_edges):
    finded_edges_list = []
    for ps in range(len(points_for_edges)):
        for p in range(len(points_for_edges[ps]) - 1):
            finded_edges_list.append(Line(points_for_edges[ps][p], points_for_edges[ps][p+1]))

    return finded_edges_list

def display_edges(reversed_intersections_dict, edges):
    display_only = []
    for items in edges:
        id1 = reversed_intersections_dict[(items.get_p1().get_x(), items.get_p1().get_y())]
        id2 = reversed_intersections_dict[(items.get_p2().get_x(), items.get_p2().get_y())]
        display_only.append([id1, id2])
    ee = 'E = {\n'
    for item in range(len(display_only)):
        if item != len(display_only) - 1:
            ee += "  <{},{}>,\n".format(display_only[item][0], display_only[item][1])
        else:
            ee += "  <{},{}>\n".format(display_only[item][0], display_only[item][1])
    ee += '}'
    return ee

def find_vertex_and_edge(street_info_dict, points_for_edges):
    # assume the coordinate values with 0.001 of one another are the same
    points_for_edges = []
    if (len(street_info_dict.values()) == 0 or len(street_info_dict.values()) == 1):
        empty_vertex = 'V = {\n}'
        empty_edge = 'E = {\n}'
        return empty_vertex, empty_edge
    else:
        intersections_set = set()
        intersections_list = []
        intersections_dict = {}

        for i in range(len(street_info_dict.keys()) - 1):
            for j in range(i + 1, len(street_info_dict.keys())):
                for m in range(len(street_info_dict.values()[i]) - 1):
                    for n in range(len(street_info_dict.values()[j]) - 1):
                        # line segment a, x values
                        ax1 = street_info_dict.values()[i][m].get_x()
                        ax2 = street_info_dict.values()[i][m+1].get_x()
                        # line segment b, x values
                        bx1 = street_info_dict.values()[j][n].get_x()
                        bx2 = street_info_dict.values()[j][n+1].get_x()
                        #line segment a, y values
                        ay1 = street_info_dict.values()[i][m].get_y()
                        ay2 = street_info_dict.values()[i][m+1].get_y()
                        #line segment b, y values
                        by1 = street_info_dict.values()[j][n].get_y()
                        by2 = street_info_dict.values()[j][n+1].get_y()

                        ax1, ay1 = format_coordinate(ax1, ay1)
                        ax2, ay2 = format_coordinate(ax2, ay2)
                        bx1, by1 = format_coordinate(bx1, by1)
                        bx2, by2 = format_coordinate(bx2, by2)
                        # check if the projections of two  line segments are overlapped
                        if (max(ax1, ax2) < min(bx1, bx2)) or (max(ay1, ay2) < min(by1, by2)) or (max(bx1, bx2) < min(ax1, ax2)) or (max(by1, by2) < min(ay1, ay2)):
                            continue

                        # either one of the line segment has same x values, in which case, the slope cannot compute
                        if (ax2 - ax1) == 0 and (bx2 - bx1) == 0:
                            if (ax1 != bx1):
                                continue
                            else:
                                intersection_x = bx1
                                intersection_y1 = sorted([ay1, ay2, by1, by2])[1]
                                intersection_y2 = sorted([ay1, ay2, by1, by2])[2]
                                intersection_x1, intersection_y1 = format_coordinate(intersection_x, intersection_y1)
                                intersection_x2, intersection_y2 = format_coordinate(intersection_x, intersection_y2)
                                add_to_intersections_list(intersection_x1, intersection_y1, intersections_list)
                                add_to_intersections_list(intersection_x2, intersection_y2, intersections_list)
                                add_to_intersections_list(ax1, ay1, intersections_list)
                                add_to_intersections_list(ax2, ay2, intersections_list)
                                add_to_intersections_list(bx1, by1, intersections_list)
                                add_to_intersections_list(bx2, by2, intersections_list)

                                add_to_edges([Point(intersection_x1, sorted([ay1, ay2, by1, by2])[0]), Point(intersection_x1, intersection_y1), Point(intersection_x1, sorted([ay1, ay2, by1, by2])[-1])], points_for_edges)

                                add_to_edges([Point(intersection_x1, sorted([ay1, ay2, by1, by2])[0]), Point(intersection_x2, intersection_y2), Point(intersection_x2, sorted([ay1, ay2, by1, by2])[-1])], points_for_edges)
                            

                        elif (ax2 - ax1) == 0:
                            ax = ax1
                            # kb = float(by2 - by1)/(bx2 - bx1)
                            kb = float(by2 - by1)/float(bx2 - bx1)
                            cb = float(by2 - kb*bx2)
                            # y = kb*x + cb
                            intersection_x = float(ax)
                            intersection_y = float(intersection_x*kb + cb)


                            if (float(min(bx1, bx2)) <= intersection_x <= float(max(bx1, bx2))) and (float(min(by1, by2)) <= intersection_y <= float(max(by1, by2))) and (float(min(ay1, ay2)) <= intersection_y <= float(max(ay1, ay2))):
                                intersection_x, intersection_y = format_coordinate(intersection_x, intersection_y)
                                add_to_intersections_list(intersection_x, intersection_y, intersections_list)
                                add_to_intersections_list(ax1, ay1, intersections_list)
                                add_to_intersections_list(ax2, ay2, intersections_list)
                                add_to_intersections_list(bx1, by1, intersections_list)
                                add_to_intersections_list(bx2, by2, intersections_list)

                                if ax2 >= ax1:

                                    add_to_edges([Point(ax1, ay1), Point(intersection_x, intersection_y), Point(ax2, ay2)], points_for_edges)
                                else:

                                    add_to_edges([Point(ax2, ay2), Point(intersection_x, intersection_y), Point(ax1, ay1)], points_for_edges)
                                if bx2 >= bx1:

                                    add_to_edges([Point(bx1, by1), Point(intersection_x, intersection_y), Point(bx2, by2)], points_for_edges)
                                else:

                                    add_to_edges([Point(bx2, by2), Point(intersection_x, intersection_y), Point(bx1, by1)], points_for_edges)

                                intersections_set.add(format_coordinate(intersection_x, intersection_y))
                                intersections_set.add((ax1, ay1))
                                intersections_set.add((ax2, ay2))
                                intersections_set.add((bx1, by1))
                                intersections_set.add((bx2, by2))
                            else:
                                continue
                        elif (bx2 - bx1) == 0:
                            bx = bx1
                            ka = float(ay2 - ay1)/(ax2 - ax1)
                            ca = float(ay2 - ka*ax2)
                            intersection_x = float(bx)
                            intersection_y = float(intersection_x*ka + ca)

                            if (float(min(ax1, ax2)) <= intersection_x <= float(max(ax1, ax2))) and (float(min(ay1, ay2)) <= intersection_y <= float(max(ay1, ay2))) and (float(min(by1, by2)) <= intersection_y <= float(max(by1, by2))):

                                intersection_x, intersection_y = format_coordinate(intersection_x, intersection_y)
                                add_to_intersections_list(intersection_x, intersection_y, intersections_list)
                                add_to_intersections_list(ax1, ay1, intersections_list)
                                add_to_intersections_list(ax2, ay2, intersections_list)
                                add_to_intersections_list(bx1, by1, intersections_list)
                                add_to_intersections_list(bx2, by2, intersections_list)

                                if ax2 >= ax1:

                                    add_to_edges([Point(ax1, ay1), Point(intersection_x, intersection_y), Point(ax2, ay2)], points_for_edges)
                                else:

                                    add_to_edges([Point(ax2, ay2), Point(intersection_x, intersection_y), Point(ax1, ay1)], points_for_edges)
                                if bx2 >= bx1:

                                    add_to_edges([Point(bx1, by1), Point(intersection_x, intersection_y), Point(bx2, by2)], points_for_edges)
                                else:

                                    add_to_edges([Point(bx2, by2), Point(intersection_x, intersection_y), Point(bx1, by1)], points_for_edges)

                                intersections_set.add(format_coordinate(intersection_x, intersection_y))
                                intersections_set.add((ax1, ay1))
                                intersections_set.add((ax2, ay2))
                                intersections_set.add((bx1, by1))
                                intersections_set.add((bx2, by2))
                            else:
                                continue
                        else:
                            ka = float(ay2 - ay1)/float(ax2 - ax1)
                            kb = float(by2 - by1)/float(bx2 - bx1)
                            ca = float(ay2 - ka*ax2)
                            cb = float(by2 - kb*bx2)
                            if (ka == kb):
                                if (ca != cb):
                                    continue
                                else:
                                    intersection_x1 = sorted([ax1, ax2, bx1, bx2])[1]
                                    intersection_y1 = sorted([ay1, ay2, by1, by2])[1]
                                    intersection_x2 = sorted([ax1, ax2, bx1, bx2])[2]
                                    intersection_y2 = sorted([ay1, ay2, by1, by2])[2]

                                    intersection_x1, intersection_y1 = format_coordinate(intersection_x1, intersection_y1)
                                    intersection_x2, intersection_y2 = format_coordinate(intersection_x2, intersection_y2)
                                    add_to_intersections_list(intersection_x1, intersection_y1, intersections_list)
                                    add_to_intersections_list(intersection_x2, intersection_y2, intersections_list)
                                    add_to_intersections_list(ax1, ay1, intersections_list)
                                    add_to_intersections_list(ax2, ay2, intersections_list)
                                    add_to_intersections_list(bx1, by1, intersections_list)
                                    add_to_intersections_list(bx2, by2, intersections_list)

                                    if ax2 >= ax1:
                                        if bx2 >= bx1:
                                            if bx1 >= ax1:
                                                if bx2 >= ax2:
                                                    add_to_edges([Point(ax1, ay1), Point(intersection_x1, intersection_y1), Point(bx2, by2)], points_for_edges)
                                                    add_to_edges([Point(ax1, ay1), Point(intersection_x2, intersection_y2), Point(bx2, by2)], points_for_edges)
                                                else:
                                                    add_to_edges([Point(ax1, ay1), Point(intersection_x1, intersection_y1), Point(ax2, ay2)], points_for_edges)
                                                    add_to_edges([Point(ax1, ay1), Point(intersection_x2, intersection_y2), Point(ax2, ay2)], points_for_edges)
                                            else:
                                                if bx2 >= ax2:
                                                    add_to_edges([Point(bx1, by1), Point(intersection_x1, intersection_y1), Point(bx2, by2)], points_for_edges)
                                                    add_to_edges([Point(bx1, by1), Point(intersection_x2, intersection_y2), Point(bx2, by2)], points_for_edges)
                                                else:
                                                    add_to_edges([Point(bx1, by1), Point(intersection_x1, intersection_y1), Point(ax2, ay2)], points_for_edges)
                                                    add_to_edges([Point(bx1, by1), Point(intersection_x2, intersection_y2), Point(ax2, ay2)], points_for_edges)
                                        else:
                                            if bx2 >= ax1:
                                                if bx1 >= ax2:
                                                    add_to_edges([Point(ax1, ay1), Point(intersection_x1, intersection_y1), Point(bx1, by1)], points_for_edges)
                                                    add_to_edges([Point(ax1, ay1), Point(intersection_x2, intersection_y2), Point(bx1, by1)], points_for_edges)
                                                else:
                                                    add_to_edges([Point(ax1, ay1), Point(intersection_x1, intersection_y1), Point(ax2, by2)], points_for_edges)
                                                    add_to_edges([Point(ax1, ay1), Point(intersection_x2, intersection_y2), Point(ax2, by2)], points_for_edges)
                                            else:
                                                if bx1 >= ax2:
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x1, intersection_y1), Point(bx1, by1)], points_for_edges)
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x2, intersection_y2), Point(bx1, by1)], points_for_edges)
                                                else:
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x1, intersection_y1), Point(ax2, ay2)], points_for_edges)
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x2, intersection_y2), Point(ax2, ay2)], points_for_edges)
                                    else:
                                        if bx2 >= bx1:
                                            if bx1 >= ax2:
                                                if bx2 >= ax1:
                                                    add_to_edges([Point(ax2, ay2), Point(intersection_x1, intersection_y1), Point(bx2, by2)], points_for_edges)
                                                    add_to_edges([Point(ax2, ay2), Point(intersection_x2, intersection_y2), Point(bx2, by2)], points_for_edges)
                                                else:
                                                    add_to_edges([Point(ax2, ay2), Point(intersection_x1, intersection_y1), Point(ax1, ay1)], points_for_edges)
                                                    add_to_edges([Point(ax2, ay2), Point(intersection_x2, intersection_y2), Point(ax1, ay1)], points_for_edges)
                                            else:
                                                if bx2 >= ax1:
                                                    add_to_edges([Point(bx1, by1), Point(intersection_x1, intersection_y1), Point(bx2, by2)], points_for_edges)
                                                    add_to_edges([Point(bx1, by1), Point(intersection_x2, intersection_y2), Point(bx2, by2)], points_for_edges)
                                                else:
                                                    add_to_edges([Point(bx1, by1), Point(intersection_x1, intersection_y1), Point(ax1, ay1)], points_for_edges)
                                                    add_to_edges([Point(bx1, by1), Point(intersection_x2, intersection_y2), Point(ax1, ay1)], points_for_edges)
                                        else:
                                            if bx2 >= ax2:
                                                if bx1 >= ax1:
                                                    add_to_edges([Point(ax2, ay2), Point(intersection_x1, intersection_y1), Point(bx1, by1)], points_for_edges)
                                                    add_to_edges([Point(ax2, ay2), Point(intersection_x2, intersection_y2), Point(bx1, by1)], points_for_edges)
                                                else:
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x1, intersection_y1), Point(ax1, ay1)], points_for_edges)
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x2, intersection_y2), Point(ax1, ay1)], points_for_edges)
                                            else:
                                                if bx1 >= ax1:
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x1, intersection_y1), Point(bx1, by1)], points_for_edges)
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x2, intersection_y2), Point(bx1, by1)], points_for_edges)
                                                else:
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x1, intersection_y1), Point(ax1, ay1)], points_for_edges)
                                                    add_to_edges([Point(bx2, by2), Point(intersection_x2, intersection_y2), Point(ax1, ay1)], points_for_edges)

                            else:
                                #y = ka*x + ca
                                #y = kb*x + cb
                                intersection_x = float((cb - ca)/(ka - kb))
                                intersection_y = float(ka*intersection_x + ca)

                                intersection_x, intersection_y = format_coordinate(intersection_x, intersection_y)
                                add_to_intersections_list(intersection_x, intersection_y, intersections_list)
                                add_to_intersections_list(ax1, ay1, intersections_list)
                                add_to_intersections_list(ax2, ay2, intersections_list)
                                add_to_intersections_list(bx1, by1, intersections_list)
                                add_to_intersections_list(bx2, by2, intersections_list)

                                if ax2 >= ax1:

                                    add_to_edges([Point(ax1, ay1), Point(intersection_x, intersection_y), Point(ax2, ay2)], points_for_edges)
                                else:

                                    add_to_edges([Point(ax2, ay2), Point(intersection_x, intersection_y), Point(ax1, ay1)], points_for_edges)
                                if bx2 >= bx1:

                                    add_to_edges([Point(bx1, by1), Point(intersection_x, intersection_y), Point(bx2, by2)], points_for_edges)
                                else:

                                    add_to_edges([Point(bx2, by2), Point(intersection_x, intersection_y), Point(bx1, by1)], points_for_edges)

                                intersections_set.add((intersection_x, intersection_y))
                                intersections_set.add((ax1, ay1))
                                intersections_set.add((ax2, ay2))
                                intersections_set.add((bx1, by1))
                                intersections_set.add((bx2, by2))


        display_vertex_result, reversed_result = display_intersections_list(intersections_list, intersections_dict)
        # print(result)
        edges_result = find_edges(points_for_edges)
        display_edges_result = display_edges(reversed_result, edges_result)

        return display_vertex_result, display_edges_result

def main():
    ### YOUR MAIN CODE GOES HERE
    street_info_dict = {}
    points_for_edges = []
    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    while True:
        try:
            line = sys.stdin.readline()

            if line == '':
                break

            command, street_info = parse_line(line)

            if command == 'a':
                add_street(street_info, street_info_dict)

            if command == 'c':
                change_street(street_info, street_info_dict)

            if command == 'r':
                remove_street(street_info, street_info_dict)

            if command == 'g':
                # TODO find edge
                vertex, edges = find_vertex_and_edge(street_info_dict, points_for_edges)
                print(vertex, file=sys.stdout)
                print(edges, file=sys.stdout)



            print('read a line:', line)
        except Exception as exp:
            print('Error: ' + str(exp), file=sys.stderr)

    print('Finished reading input')
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()
