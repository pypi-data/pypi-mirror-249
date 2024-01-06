class Summary:
    def __init__(self, name, times, count, ratio, children):
        self.name = name
        self.times = times if isinstance(times, list) else [times]
        self.count = count
        self.ratio = ratio
        self.children = children

        self.internal_time = None
        pass
