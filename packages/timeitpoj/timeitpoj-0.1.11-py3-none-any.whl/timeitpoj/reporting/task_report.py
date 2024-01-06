import logging
from typing import Union, List
from timeitpoj.utils import constants
from timeitpoj.utils.misc import reformat_units, format_percentage, time_to_str

PADDING_SECONDS = len("seconds")


class TaskReport:
    def __init__(self,
                 name: str,
                 times: Union[List[float], float],
                 count: int,
                 ratio: float,
                 children: List["TaskReport"],
                 padding_name: int,
                 log_func=None):
        if log_func is None:
            def pprint(*args, **kwargs):
                print("TIMEITPOJ", *args, **kwargs)

            log_func = pprint
        self.log = log_func

        self.name = name
        self.times = times if isinstance(times, list) else [times]
        self.count = count
        self.ratio = ratio
        self.children = children
        self.internal_time = None
        self.padding_name = padding_name
        self.unit_padding = PADDING_SECONDS
        self.avg_duration_padding = len(self.formatted_avg_duration)

    @property
    def avg_duration(self):
        return sum(self.times) / len(self.times)

    @property
    def total_duration(self):
        return sum(self.times)

    @property
    def formatted_duration(self):
        return reformat_units(self.total_duration)

    @property
    def formatted_padding(self):
        return len(" ".join(f"{value} {unit}" for value, unit in self.formatted_duration))

    @property
    def formatted_avg_duration(self):
        return time_to_str(self.avg_duration)

    def __print_child(self, child, spacing, last_child, child_unit_padding, child_avg_duration_padding):
        prefix = "│" if not last_child else " "
        connector = "└──" if last_child else "├──"

        self.log(" " * spacing + f"{connector} {child}")

        if child.children:
            child.print(
                prefix=prefix, spacing=spacing + constants.DEFAULT_SPACING, skip_first=True,
                unit_padding=child_unit_padding, avg_duration_padding=child_avg_duration_padding
            )

    def print(self, prefix="", spacing=0, skip_first=False, unit_padding=PADDING_SECONDS, avg_duration_padding=0):
        self.unit_padding = unit_padding
        self.avg_duration_padding = avg_duration_padding

        if not skip_first:
            self.log(self)

        if self.children:
            child_unit_padding = max(child.formatted_padding for child in self.children)
            child_avg_duration_padding = max(len(child.formatted_avg_duration) for child in self.children)

            for i, child in enumerate(self.children):
                last_child = i == len(self.children) - 1 or len(child.children) > 1
                self.__print_child(
                    child, spacing, last_child, child_unit_padding, child_avg_duration_padding
                )

        if self.internal_time is not None:
            internal_time = self.internal_time
            internal_time_ratio = internal_time / self.total_duration
            formatted = reformat_units(internal_time, start_unit="seconds")

            formatted_str = " ".join(f"{value:{constants.DURATION_FORMAT}} {unit}" for value, unit in formatted)

            self.log(" " * spacing + f"└── {format_percentage(internal_time_ratio)} "
                                     f"internal time: {formatted_str}")

    @classmethod
    def from_dict(cls, task_report_dict: dict, padding_name=0, log_func=None):
        children = []
        if "subtasks" in task_report_dict:
            for child in task_report_dict["subtasks"].values():
                children.append(cls.from_dict(child, padding_name=len(child["name"]), log_func=log_func))

        return cls(
            name=task_report_dict["name"],
            times=task_report_dict["times"],
            count=task_report_dict["count"],
            ratio=task_report_dict["ratio"],
            children=children,
            padding_name=padding_name,
            log_func=log_func
        )

    def __str__(self):
        ratio_str = f"{format_percentage(self.ratio)} " if self.ratio < 1 else ""
        name_str = f"{self.name:{self.padding_name}}" if self.padding_name > 0 else self.name
        count_str = f"{self.count} times" if self.count > 1 else ""
        avg_duration_str = f"avg {time_to_str(self.avg_duration):{self.avg_duration_padding}}" if self.count > 1 else ""

        formatted_duration = " ".join(
            f"{value:{constants.DURATION_FORMAT}} {unit:{self.unit_padding}}" for value, unit in self.formatted_duration
        )

        to_print = [
            constants.PREFIX,
            f"{ratio_str}{name_str}",
            formatted_duration,
            f"{count_str}",
            f"{avg_duration_str}"
        ]

        to_print = [x for x in to_print if x != ""]
        return constants.SEPERATOR.join(to_print)

    def __repr__(self):
        return str(self)
