import os
from collections import Counter
from itertools import combinations
from copy import deepcopy


class SudokuError(Exception):
    def __init__(self, message):
        self.message = message


class Sudoku:
    def __init__(self, filename):
        path = os.getcwd() + '/' + filename
        self.name = filename.replace('.txt', '')
        with open(path) as file:
            self.grid = [line.strip() for line in file if line.strip() != '']
        self.check_input()
        self.check_length()

        self.marked_dict = dict()
        self.canceled_dict = dict()
        for box in self.get_all_box_coordinates():
            for coordinate in box:
                if self.grid[coordinate[0]][coordinate[1]] == 0:
                    self.marked_dict[coordinate] = []
        self.highest_frequency = []
        self.update_frequency()

    def update_frequency(self):
        temp = []
        for row in self.grid:
            temp.extend(row)
        self.highest_frequency = Counter(temp).most_common(10)
        if self.highest_frequency[0][0] == 0:
            self.highest_frequency.pop(0)

    def check_input(self):
        for i in range(len(self.grid)):
            line = self.grid[i].replace(' ', '')
            try:
                line = list(map(int, line))
                for e in line:
                    if e not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        raise SudokuError('Incorrect input')
            except ValueError:
                raise SudokuError('Incorrect input')
            self.grid[i] = line

    def check_length(self):
        if len(self.grid) != 9:
            raise SudokuError('Incorrect input')
        for line in self.grid:
            if len(line) != 9:
                raise SudokuError('Incorrect input')

    def preassess(self):
        if not self.check_row() or not self.check_column() or not self.check_grid():
            print('There is clearly no solution.')
            return
        print('There might be a solution.')

    def check_row(self):
        for line in self.grid:
            for num in range(1, 10):
                if line.count(num) > 1:
                    return False
        return True

    def check_column(self):
        for i in range(9):
            line = []
            for j in range(9):
                line.append(self.grid[j][i])
                for num in range(1, 10):
                    if line.count(num) > 1:
                        return False
        return True

    def check_grid(self):
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                mini = self.get_mini_grid(i, j)
                for num in range(1, 10):
                    if mini.count(num) > 1:
                        return False
        return True

    def get_mini_grid(self, start_i, start_j):
        mini_grid = []
        for i in range(start_i, start_i + 3):
            mini_grid.extend(self.grid[i][start_j: start_j+3])
        return mini_grid

    def bare_tex_output(self):
        self.write_latex_head(self.name + '_bare.tex')
        self.write_bare_body(self.name + '_bare.tex')
        self.write_latex_ass(self.name + '_bare.tex')

    def write_latex_head(self, name):
        file = open(name, 'w')
        head = ['\documentclass[10pt]{article}',
                '\\usepackage[left=0pt,right=0pt]{geometry}',
                '\\usepackage{tikz}',
                '\\usetikzlibrary{positioning}',
                '\\usepackage{cancel}',
                '\pagestyle{empty}\n',
                '\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},',
                '                               label=above right:{\\tiny #2},',
                '                               label=below left:{\\tiny #3},',
                '                               label=below right:{\\tiny #4}]{#5};}}\n',
                '\\begin{document}\n',
                '\\tikzset{every node/.style={minimum size=.5cm}}\n',
                '\\begin{center}',
                '\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline\n']
        file.write('\n'.join(head))
        file.close()

    def write_latex_ass(self, name):
        file = open(name, 'a')
        ass = ['\end{tabular}', '\end{center}\n', '\end{document}\n']
        file.write('\n'.join(ass))
        file.close()

    def write_bare_body(self, name):
        file = open(name, 'a')
        for i in range(9):
            line = '% Line ' + str(i+1) + '\n'
            body = []
            for j in range(9):
                if self.grid[i][j] != 0:
                    t = '\\N{}{}{}{}{' + str(self.grid[i][j]) + '}'
                else:
                    t = '\\N{}{}{}{}{}'
                if j != 8:
                    t += ' & '
                else:
                    if i % 3 == 2:
                        t += ' \\\\ \hline\hline'
                        if (i, j) != (8, 8):
                            t += '\n'
                    else:
                        t += ' \\\\ \hline\n'
                if j % 3 == 2:
                    t = t.rstrip(' ') + '\n'
                body.append(t)
            file.write(line + ''.join(body))
        file.close()

    def write_marked_body(self, name):
        file = open(name, 'a')
        for i in range(9):
            line = '% Line ' + str(i + 1) + '\n'
            body = []
            for j in range(9):
                if self.grid[i][j] != 0:
                    t = '\\N{}{}{}{}{' + str(self.grid[i][j]) + '}'
                else:
                    # If the cell is marked
                    marked = self.marked_dict[(i, j)]
                    t1 = []
                    t2 = []
                    t3 = []
                    t4 = []
                    for m in marked:
                        if m == 1 or m == 2:
                            t1.append(str(m))
                        a = '{' + ' '.join(t1) + '}'
                        if m == 3 or m == 4:
                            t2.append(str(m))
                        b = '{' + ' '.join(t2) + '}'
                        if m == 5 or m == 6:
                            t3.append(str(m))
                        c = '{' + ' '.join(t3) + '}'
                        if m == 7 or m == 8 or m ==9:
                            t4.append(str(m))
                        d = '{' + ' '.join(t4) + '}'
                    t = '\\N' + a + b + c + d + '{}'
                if j != 8:
                    t += ' & '
                else:
                    if i % 3 == 2:
                        t += ' \\\\ \hline\hline'
                        if (i, j) != (8, 8):
                            t += '\n'
                    else:
                        t += ' \\\\ \hline\n'
                if j % 3 == 2:
                    t = t.rstrip(' ') + '\n'
                body.append(t)
            file.write(line + ''.join(body))
        file.close()

    def forced_tex_output(self):
        self.force()
        self.write_latex_head(self.name + '_forced.tex')
        self.write_bare_body(self.name + '_forced.tex')
        self.write_latex_ass(self.name + '_forced.tex')

    def marked_tex_output(self):
        self.force()
        self.get_marked()
        self.write_latex_head(self.name + '_marked.tex')
        self.write_marked_body(self.name + '_marked.tex')
        self.write_latex_ass(self.name + '_marked.tex')

    def worked_tex_output(self):
        self.worked()
        self.write_latex_head(self.name + '_worked.tex')
        self.write_worked_body(self.name + '_worked.tex')
        self.write_latex_ass(self.name + '_worked.tex')

    def write_worked_body(self, name):
        file = open(name, 'a')
        for i in range(9):
            line = '% Line ' + str(i + 1) + '\n'
            body = []
            for j in range(9):
                try:
                    marked = self.marked_dict[(i, j)]
                except KeyError:
                    marked = []
                try:
                    canceled = [-1*x for x in self.canceled_dict[(i, j)]]
                except KeyError:
                    canceled = []
                marked.extend(reversed(sorted(canceled)))
                marked = sorted(marked, key=abs)
                t1 = []
                t2 = []
                t3 = []
                t4 = []
                a, b, c, d = '{}', '{}', '{}', '{}'
                for m in marked:
                    if abs(m) == 1 or abs(m) == 2:
                        if m < 0:
                            # o = '\cancel{'+str(abs(m))+'}'
                            t1.append('\cancel{'+str(abs(m))+'}')
                        else:
                            t1.append(str(m))
                    a = '{' + ' '.join(t1) + '}'
                    if abs(m) == 3 or abs(m) == 4:
                        if m < 0:
                            # o = '\cancel{'+str(abs(m))+'}'
                            t2.append('\cancel{'+str(abs(m))+'}')
                        else:
                            t2.append(str(m))
                    b = '{' + ' '.join(t2) + '}'
                    if abs(m) == 5 or abs(m) == 6:
                        if m < 0:
                            # o = '\cancel{'+str(abs(m))+'}'
                            t3.append('\cancel{'+str(abs(m))+'}')
                        else:
                            t3.append(str(m))
                    c = '{' + ' '.join(t3) + '}'
                    if abs(m) == 7 or abs(m) == 8 or abs(m) == 9:
                        if m < 0:
                            # o = '\cancel{'+str(abs(m))+'}'
                            t4.append('\cancel{'+str(abs(m))+'}')
                        else:
                            t4.append(str(m))
                    d = '{' + ' '.join(t4) + '}'
                if self.grid[i][j] != 0:
                    e = '{' + str(self.grid[i][j]) + '}'
                else:
                    e = '{}'
                t = '\\N' + a + b + c + d + e
                if j != 8:
                    t += ' & '
                else:
                    if i % 3 == 2:
                        t += ' \\\\ \hline\hline'
                        if (i, j) != (8, 8):
                            t += '\n'
                    else:
                        t += ' \\\\ \hline\n'
                if j % 3 == 2:
                    t = t.rstrip(' ') + '\n'
                body.append(t)
            file.write(line + ''.join(body))
        file.close()

    def find_preemptive_pair_in_row(self, n):
        marked_dic = dict()
        temp = []
        signal = True
        for i in range(9):
            try:
                marked_dic[(n, i)] = sorted(set(self.marked_dict[(n, i)]))
                temp.extend(sorted(self.marked_dict[(n, i)]))
            except KeyError:
                pass
        marked_comb = []
        empty_cell_num = len(set(temp))
        min_len = min([len(l) for l in marked_dic.values()])
        if min_len < 2:
            min_len = 2
        for l in range(min_len, len(marked_dic.values()) + 1):
            marked_comb.extend(set(combinations(set(temp), l)))
        for comb in marked_comb:
            pre_set = dict()
            for c, e in marked_dic.items():
                if set(e) <= set(comb) and len(e) <= len(comb) and e != []:
                    pre_set[c] = e
            if len(pre_set) == len(comb) and len(pre_set) != empty_cell_num:
                # found one pre-emptive set
                delete_dict = marked_dic.copy()
                for k in pre_set.keys():
                    delete_dict.pop(k)
                # print('### row ###')
                # print(f'Preemptive set is {comb} : {pre_set}, need to delete {delete_dict}')
                signal = self.delete_from_marked(comb, delete_dict, 'row')
                # return signal
        return signal

    def find_preemptive_pair_in_column(self, n):
        marked_dic = dict()
        temp = []
        signal = True
        for i in range(9):
            try:
                marked_dic[(i, n)] = sorted(set(self.marked_dict[(i, n)]))
                temp.extend(sorted(self.marked_dict[(i, n)]))
            except KeyError:
                pass
        marked_comb = []
        empty_cell_num = len(set(temp))
        min_len = min([len(l) for l in marked_dic.values()])
        if min_len < 2:
            min_len = 2
        for l in range(min_len, len(marked_dic.values()) + 1):
            marked_comb.extend(set(combinations(set(temp), l)))
        for comb in marked_comb:
            pre_set = dict()
            for c, e in marked_dic.items():
                if set(e) <= set(comb) and len(e) <= len(comb) and e != []:
                    pre_set[c] = e
            if len(pre_set) == len(comb) and len(pre_set) != empty_cell_num:
                # found one pre-emptive set
                delete_dict = marked_dic.copy()
                for k in pre_set.keys():
                    delete_dict.pop(k)
                # print('### column ###')
                # print(f'Preemptive set is {comb} : {pre_set}, need to delete {delete_dict}')
                signal = self.delete_from_marked(comb, delete_dict, 'column')
                # return signal
        return signal

    def find_preemptive_pair_in_box(self, i, j):
        temp = []
        marked_dic = dict()
        signal = True
        box_c = self.get_box_coordinates(i, j)
        for c in box_c:
            try:
                temp.extend(sorted(self.marked_dict[(c[0], c[1])]))
                marked_dic[(c[0], c[1])] = sorted(self.marked_dict[(c[0], c[1])])
            except KeyError:
                pass
        empty_cell_num = len(set(temp))
        marked_comb = []
        min_len = min([len(l) for l in marked_dic.values()])
        if min_len < 2:
            min_len = 2
        for l in range(min_len, len(marked_dic.values())+1):
            marked_comb.extend(set(combinations(set(temp), l)))
        for comb in marked_comb:
            pre_set = dict()
            for c, e in marked_dic.items():
                if set(e) <= set(comb) and len(e) <= len(comb) and e != []:
                    pre_set[c] = e
            if len(pre_set) == len(comb) and len(pre_set) != empty_cell_num:
                # Found pre-emptive set
                delete_dict = marked_dic.copy()
                for k in pre_set.keys():
                    delete_dict.pop(k)
                # print('### box ###')
                # print(f'Preemptive set is {comb} : {pre_set}, need to delete {delete_dict}')
                signal = self.delete_from_marked(comb, delete_dict, 'box')
                # return signal
        return signal

    def get_all_box_coordinates(self):
        box_c = []
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                temp = []
                for a in range(i, i+3):
                    for b in range(j, j+3):
                        temp.append((a, b))
                box_c.append(temp)
        return box_c

    def get_box_coordinates(self, i, j):
        all_coordinates = self.get_all_box_coordinates()
        if i < 3 and j < 3:
            return all_coordinates[0]
        elif i < 3 and j < 6:
            return all_coordinates[1]
        elif i < 3 and j < 9:
            return all_coordinates[2]
        elif i < 6 and j < 3:
            return all_coordinates[3]
        elif i < 6 and j < 6:
            return all_coordinates[4]
        elif i < 6 and j < 9:
            return all_coordinates[5]
        elif i < 9 and j < 3:
            return all_coordinates[6]
        elif i < 9 and j < 6:
            return all_coordinates[7]
        elif i < 9 and j < 9:
            return all_coordinates[8]

    def get_collumn(self, n):
        return [self.grid[i][n] for i in range(9)]

    def get_marked(self):
        boxes = self.get_all_box_coordinates()
        for box in boxes:
            b = self.get_mini_grid(box[0][0], box[0][1])
            for coordinate in box:
                column = set(self.get_collumn(coordinate[1]))
                row = set(self.grid[coordinate[0]])
                b = set(b)
                try:
                    column.remove(0), row.remove(0), b.remove(0)
                except KeyError:
                    pass
                for num in range(1, 10):
                    try:
                        if num not in column and num not in row and num not in b and num not in self.marked_dict[coordinate]:
                            try:
                                self.marked_dict[coordinate].append(num)
                            except KeyError:
                                break
                                pass
                    except KeyError:
                        pass

    def force(self):
        no_change = False
        while not no_change:
            no_change = True
            for f in self.highest_frequency:
                for i in range(0, 7, 3):
                    for j in range(0, 7, 3):
                        box = self.get_mini_grid(i, j)
                        box_c = self.get_box_coordinates(i, j)
                        potential_force = []
                        if f[0] not in box:
                            # Can insert
                            for c in box_c:
                                # check each coordinate that is empty in box
                                if self.grid[c[0]][c[1]] == 0:
                                    # Can I insert f[0] into grid[c[0]][c[1]] ?
                                    if self.can_insert_row(c[0], f[0]) and self.can_insert_column(c[1], f[0]):
                                        potential_force.append((c, f[0]))
                            if len(potential_force) == 1:
                                self.grid[potential_force[0][0][0]][potential_force[0][0][1]] = potential_force[0][1]
                                self.update_frequency()
                                self.marked_dict.pop((potential_force[0][0][0], potential_force[0][0][1]))
                                no_change = False

    def can_insert_row(self, n, f):
        row = self.grid[n].copy()
        row.append(f)
        if row.count(f) > 1:
            return False
        return True

    def can_insert_column(self, n, f):
        column = self.get_collumn(n)
        column.append(f)
        if column.count(f) > 1:
                return False
        return True

    def delete_from_marked(self, comb, delete_dic, type):
        copy_marked = deepcopy(self.marked_dict)
        for grid_c, marked in delete_dic.items():
            for c in comb:
                if c in self.marked_dict[grid_c]:
                    self.marked_dict[grid_c].remove(c)
                    try:
                        self.canceled_dict[grid_c].append(c)
                    except KeyError:
                        self.canceled_dict[grid_c] = [c]
        not_found = False
        while not not_found:
            c, not_found = self.search_for_singleton()
            if not_found:
                break
            self.grid[c[0]][c[1]] = self.marked_dict[c][0]
            try:
                self.canceled_dict[c].append(self.marked_dict[c].pop())
            except KeyError:
                self.canceled_dict[c] = [self.marked_dict[c].pop()]
            # delete the rest of the nums from the inserted shit
            type_c = []
            type_c.extend([(c[0], i) for i in range(9)])
            type_c.extend([(i, c[1]) for i in range(9)])
            type_c.extend(self.get_box_coordinates(c[0], c[1]))
            type_c = list(sorted(set(type_c)))
            # print(f'Found singleton {self.grid[c[0]][c[1]]} on {c}')
            self.delete_singleton(type_c, self.grid[c[0]][c[1]])
        if copy_marked == self.marked_dict:
            return True
        else:
            return False

    def search_for_singleton(self):
        for c, e in self.marked_dict.items():
            if len(e) == 1:
                return c, False
        return None, True

    def delete_singleton(self, coordinates, num):
        for c in coordinates:
            try:
                self.marked_dict[c].remove(num)
                try:
                    self.canceled_dict[c].append(num)
                except KeyError:
                    self.canceled_dict[c] = [num]
            except ValueError:
                pass
            except KeyError:
                pass

    def worked(self):
        self.force()
        self.get_marked()
        no_change = [False] * 3
        search = True
        while not all(no_change) and search:
            for i in range(9):
                no_change[0] = self.find_preemptive_pair_in_row(i)
            for i in range(9):
                no_change[1] = self.find_preemptive_pair_in_column(i)
            for i in range(0, 7, 3):
                for j in range(0, 7, 3):
                    no_change[2] = self.find_preemptive_pair_in_box(i, j)
            search = self.search_for_singleton()

    def is_finished(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return False
        return True
