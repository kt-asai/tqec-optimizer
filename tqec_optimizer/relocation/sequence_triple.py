from ..position import Position


class SequenceTriple:
    def __init__(self, module_list, permutations=None):
        self._module_list = module_list
        self._permutation1 = [] if permutations is None else permutations[0]
        self._permutation2 = [] if permutations is None else permutations[1]
        self._permutation3 = [] if permutations is None else permutations[2]
        self._placed = [False for no in range(0, 100)]

    def build_permutation(self):
        # prepare
        for module_ in self._module_list:
            self._permutation1.append(module_)
            self._permutation2.append(module_)
            self._permutation3.append(module_)

        # z direction
        self._permutation3.sort(key=lambda m: (m.pos.z, m.pos.x))
        self._permutation2.sort(key=lambda m: (m.pos.z, m.pos.x))
        self._permutation1.sort(key=lambda m: (m.pos.z, m.pos.x))

        # x direction
        self._permutation2.sort(key=lambda m: (m.pos.x, -m.pos.z), reverse=True)

        return self._permutation1, self._permutation2, self._permutation3

    def recalculate_coordinate(self):
        for module_ in self._permutation3:
            id_ = module_.id
            new_pos = Position(self.__find_x(id_), self.__find_y(id_), self.__find_z(id_))
            module_.set_position(new_pos, True)
            self._placed[id_] = True

        return self._module_list

    def __find_x(self, id_):
        p2_list = set()
        flag = False
        for module_ in self._permutation2:
            if module_.id == id_:
                flag = True
            if not flag:
                continue
            if self._placed[module_.id]:
                p2_list.add(module_)

        placed_module_list = p2_list
        x = 0
        for module_ in placed_module_list:
            x = max(x, module_.pos.x + module_.width)

        return x

    def __find_y(self, id_):
        p1_list = set()
        p2_list = set()
        flag = False
        for module_ in self._permutation1:
            if module_.id == id_:
                flag = True
            if not flag:
                continue
            if self._placed[module_.id]:
                p1_list.add(module_)

        for module_ in self._permutation2:
            if module_.id == id_:
                break
            if self._placed[module_.id]:
                p2_list.add(module_)

        placed_module_list = p1_list & p2_list
        y = 0
        for module_ in placed_module_list:
            y = max(y, module_.pos.y + module_.height)

        return y

    def __find_z(self, id_):
        p1_list = set()
        p2_list = set()
        for module_ in self._permutation1:
            if module_.id == id_:
                break
            if self._placed[module_.id]:
                p1_list.add(module_)

        for module_ in self._permutation2:
            if module_.id == id_:
                break
            if self._placed[module_.id]:
                p2_list.add(module_)

        placed_module_list = p1_list & p2_list
        z = 0
        for module_ in placed_module_list:
            z = max(z, module_.pos.z + module_.depth)

        return z
