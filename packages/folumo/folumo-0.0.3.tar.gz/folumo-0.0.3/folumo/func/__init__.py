flipFlop_ = {}


def flipFlop(id_):
    if id_ in flipFlop_:
        flipFlop_[id_] = not flipFlop_[id_]
    else:
        flipFlop_[id_] = False

    return flipFlop_[id_]


class Switch:
    def __init__(self, caseNow):
        self.nowArg = caseNow
        self.cases = {}
        self.default_ = None

    def case(self, arg, break_=True):
        def decorator(func):
            self.cases[func] = (arg, break_)

        return decorator

    def default(self, func):
        self.default_ = func

    def run(self):
        case_matched = False
        for func_name in self.cases:
            if self.cases[func_name][0] == self.nowArg:
                func_name()
                if self.cases[func_name][1]:
                    case_matched = True
                    break

        if not case_matched and self.default_:
            self.default_()


def test():
    switch = Switch(1223)

    @switch.case(123)
    def a():
        print(123)

    @switch.default
    def default_case():
        print("Default case executed")

    switch.run()


if __name__ == "__main__":
    test()

