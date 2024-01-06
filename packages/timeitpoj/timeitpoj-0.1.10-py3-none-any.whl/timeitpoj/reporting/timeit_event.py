class TimeitEvent:
    def __init__(self, handler_name: str):
        self.handler_name = handler_name

    def on_start(self, timeit: "TimeIt"):
        """
        code to run when the root timer starts
        :param timeit: the timeit object
        :return:
        """
        pass

    def on_timer_start(self, timeit: "TimeIt"):
        """
        code to run when a timer starts
        :param timeit: the timeit object
        :return:
        """
        pass

    def on_timer_end(self, timeit: "TimeIt"):
        """
        code to run when a timer ends
        :param timeit: the timeit object
        :return:
        """
        pass

    def on_end(self, timeit: "TimeIt"):
        """
        code to run when the root timer ends
        :param timeit: the timeit object
        :return:
        """
        pass
