#  Copyright (c) 2023 Jari Van Melckebeke
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
import logging
import time
from distutils.util import strtobool
import os
from functools import wraps
from typing import List

from timeitpoj.reporting.events.print_report_action import PrintReportHandler
from timeitpoj.reporting.timeit_event import TimeitEvent
from timeitpoj.timer.internal_timer import InternalTimer
from timeitpoj.timer.timer import Timer


class TimeIt:
    """
    Jari's infamous timeit class for all your performance measuring needs

    Usage:
    with TimeIt("my timer") as timer:
        # do stuff
        with timer("my subtimer"):
            # do stuff
            with timer("my subtimer 2"):
                # do stuff


    or as a decorator:
    @TimeIt.as_decorator("my timer", include=True)
    def my_function(*args, timer, **kwargs):
        # do stuff

    """

    def __init__(self, name: str,
                 handlers: List[TimeitEvent] = None,
                 log_func=None):
        """
        creates a new TimeIt object
        the TimeIt object is a manager for the root timer
        :param name: the name of the timer (used for reporting)
        :param handlers: the handlers that will be used for reporting
        """
        if log_func is None:
            log_func = print

        self.internal_timer = InternalTimer()
        self.timer = None
        self.log = log_func

        with self.internal_timer:
            if handlers is None:
                handlers = [PrintReportHandler(log_func=self.log)]

            self.name = name
            self.handlers = handlers

            self.start_time = None
            self.end_time = None
            self.active = bool(strtobool(os.getenv("TIME_IT", "true")))

            if not self.active:
                self.log("TimeIt is disabled, no reports will be printed")

    def handle_start(self):
        """
        handles the start of the root timer
        """
        for handler in self.handlers:
            handler.on_start(self)

    def handle_end(self):
        """
        handles the end of the root timer
        """
        for handler in self.handlers:
            handler.on_end(self)

    def __enter__(self):
        """
        when entering the context manager, the root timer is started
        """
        with self.internal_timer:
            self.start_time = time.time()
            if self.timer is None:
                self.timer = Timer(self.name, self.internal_timer, None)
                self.handle_start()
            return self.timer.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        when exiting the context manager, the root timer is stopped and a report is printed
        note: currently printing the report happens always (unless TIME_IT is set to false), however,
        this is planned to be changed in the future
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.end_time = time.time()
        if self.active:
            self.handle_end()

    def __call__(self, name, *args, **kwargs):
        """
        when calling the TimeIt object, a new task is created within the current running timer
        :param name: the name of the (sub)task that is being timed
        :param args:
        :param kwargs:
        :return:
        """
        if self.timer is None:
            self.timer = Timer(name, self.internal_timer, None)

        return self.timer(name)

    @property
    def elapsed_time(self):
        """
        the elapsed time of the root timer
        :return:
        """

        if self.end_time is None:
            return None

        return self.end_time - self.start_time if self.end_time is not None else None

    @classmethod
    def as_decorator(cls, name=None, include=False, log_func=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal name
                if name is None:
                    name = func.__name__
                with cls(name, log_func=log_func) as timer:
                    if include:
                        return func(*args, timer=timer, **kwargs)
                    else:
                        return func(*args, **kwargs)

            return wrapper

        return decorator
