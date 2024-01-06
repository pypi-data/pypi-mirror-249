import time

from timeitpoj.reporting.task_report import TaskReport
from timeitpoj.reporting.timeit_event import TimeitEvent
from timeitpoj.utils.misc import time_to_str


class PrintReportHandler(TimeitEvent):
    def __init__(self, log_func=None):
        if log_func is None:
            log_func = print
        self.log = log_func
        super().__init__("print_report")

    def __print_timeit_report(self, timeit: "TimeIt"):
        def print_report_title_line():
            self.log(f"================= [{timeit.name}] TIMEIT REPORT =================")

        def generate_task_report_dict(tasks):

            report = {}

            for task_timer in tasks:
                task_name = task_timer["name"]

                if task_name in report:
                    report[task_name]["count"] += 1
                    report[task_name]["times"].append(task_timer["elapsed_time"])
                    report[task_name]["avg"] = sum(report[task_name]["times"]) / report[task_name]["count"]
                else:
                    report[task_name] = {
                        "name": task_name,
                        "count": 1,
                        "times": [task_timer["elapsed_time"]],
                        "ratio": 0,
                        "avg": task_timer["elapsed_time"],
                    }

                if len(task_timer["task_timers"]) > 0:
                    report[task_name]["subtasks"] = generate_task_report_dict(task_timer["task_timers"])
            total_time = sum([sum(task["times"]) for task in report.values()])

            for task in report.values():
                task["ratio"] = sum(task["times"]) / total_time

            return report

        def print_report(_report, spacing=0):
            task_report = TaskReport.from_dict(
                {
                    "name": timeit.name,
                    "count": 1,
                    "times": [timeit.elapsed_time],
                    "ratio": 0,
                    "avg": timeit.elapsed_time,
                    "subtasks": _report,
                }
            )
            task_report.internal_time = timeit.internal_timer.internal_time
            task_report.print(spacing=spacing, skip_first=True)

        elapsed_time = timeit.elapsed_time

        generate_report_start = time.time()

        if len(timeit.timer.task_timers) < 1:
            self.log(f"[TIMEIT] {timeit.name} took {time_to_str(elapsed_time)}")
            return

        print_report_title_line()

        self.log(f"[TIMEIT] {timeit.name} took {time_to_str(elapsed_time)}")

        report = generate_task_report_dict(timeit.timer.task_timers)

        print_report(report, spacing=0)

        # print coverage stats

        time_accounted_for = 0
        total_time = elapsed_time + timeit.internal_timer.internal_time

        for task in report.values():
            time_accounted_for += sum(task["times"])

        coverage = time_accounted_for / total_time
        time_unaccounted_for = total_time - time_accounted_for
        self.log(
            f"[{coverage:.2%}% COVERAGE] time accounted for: {time_to_str(time_accounted_for)}, "
            f"time unaccounted for: {time_to_str(time_unaccounted_for)}")

        generate_report_end = time.time()
        generate_report_duration = generate_report_end - generate_report_start

        self.log(f"[TIMEIT] report generation took {time_to_str(generate_report_duration)}")

        print_report_title_line()

    def on_end(self, timeit: "TimeIt"):
        return self.__print_timeit_report(timeit)
