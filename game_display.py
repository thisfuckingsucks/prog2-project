


class Display:
    def __init__(self):
        self.__objects = []
        self.n = 0

    def add(self, object, n1=0, n2=None):
        if not self.__objects:
            self.__objects.append(object)
            self.n += 1
        else:
            if n2 is None:
                n2 = self.n - 1
            if n1 == n2:
                if object.z > self.__objects[n1].z:
                    self.__objects.append(object)
                    self.n += 1
                elif object.z < self.__objects[n1].z:
                    self.__objects.insert(n1 - 1, object)
                    self.n += 1
            else:
                check = (n1 + n2)//2
                if self.__objects[check].z <= object.z <= self.__objects[check + 1].z:
                    self.__objects.index(check, object)
                    self.n += 1
                elif object.z > self.__objects[check + 1].z:
                    self.add(object, check + 1, n2)
                elif object.z < self.__objects[check].z:
                    self.add(object, n1, check)

    def top(self):
        if not self.__objects:
            return 0
        else:
            return self.__objects[-1].z

    def reorder(self, o):
        self.__objects.remove(o)
        self.n -= 1
        self.add(o)

    def render(self, screen):
        for o in self.__objects:
            o.render(screen)

    def show(self):
        for o  in self.__objects:
            print(o, f"z: {o.z}", f"n: {self.n}")