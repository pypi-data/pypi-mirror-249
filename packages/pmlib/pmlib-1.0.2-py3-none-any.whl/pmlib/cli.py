
from argparse import ArgumentParser, Namespace, FileType
from argparse import _SubParsersAction
from typing import List
import shlex
import sys
import os

from loguru import logger
import attrs


@attrs.define(repr=False)
class Parser:
    """
    :param input_str: String list of arguments
    :type input_str: str
    """
    input_str: str = ""

    argv: List = None
    parser: ArgumentParser = None
    subparsers: _SubParsersAction = None

    @logger.catch(reraise=True)
    def __init__(self, input_str: str = ""):
        if input_str == "":
            input_str = " ".join(sys.argv)

        self.input_str = input_str
        self.argv = [input_str]
        self.argv.extend(shlex.split(input_str))

        self.parser = None
        self.subparsers = None

        self.parser = ArgumentParser(
            prog=os.path.basename(__file__),
            description="Help string placeholder",
            add_help=True,
        )
        self.subparsers = self.parser.add_subparsers(
            help="commands",
            required=True,
            dest="command")

        self.build_command_project()
        self.build_command_task()
        self.build_command_uuid()

    def __repr__(self) -> str:
        return f"""<Parser '{" ".join(self.argv)}'>"""

    @logger.catch(reraise=True)
    def parse(self) -> Namespace:
        return self.parser.parse_args()

    @logger.catch(reraise=True)
    def build_command_project(self) -> None:
        """Build the project command as a subparser"""
        parser = self.subparsers.add_parser(
            "project",
            help="Create a new project")

        parser_required = parser.add_argument_group("required")
        parser_required.add_argument(
            "-p", "--project",
            required=True,
            type=str,
            help="Create a new project with this name")

        parser_optional = parser.add_argument_group("optional")
        parser_optional.add_argument(
            "-E", "--send_email",
            required=False,
            action='store_true',
            help="Send an email about the new project event")

        parser_optional_exclusive = parser_optional.add_mutually_exclusive_group()
        parser_optional_exclusive.add_argument(
            "-c", "--create",
            required=False,
            action='store_true',
            help="Create this new project")
        parser_optional_exclusive.add_argument(
            "-m", "--modify",
            required=False,
            action='store_true',
            help="Modify this project")
        parser_optional_exclusive.add_argument(
            "-l", "--log",
            required=False,
            action='store_true',
            help="Show this project's log")
        parser_optional_exclusive.add_argument(
            "-s", "--show",
            required=False,
            action='store_true',
            help="Show this project")

    @logger.catch(reraise=True)
    def build_command_task(self) -> None:
        """Build the task command as a subparser"""
        parser = self.subparsers.add_parser(
            "task",
            help="Manage a task")

        parser_required = parser.add_argument_group("required")
        parser_required.add_argument(
            "-t", "--task",
            required=True,
            type=str,
            help="Task name")
        parser_required.add_argument(
            "-D", "--due",
            required=True,
            type=str,
            help="Set task due")

        parser_optional = parser.add_argument_group("optional")
        parser_optional.add_argument(
            "-E", "--send_email",
            required=False,
            action='store_true',
            help="Send an email about the new task event")
        parser_optional.add_argument(
            "-O", "--owner",
            required=False,
            type=str,
            help="Set task uuid owner")
        parser_optional.add_argument(
            "-S", "--start",
            required=False,
            type=str,
            help="Set task start (default today)")

        parser_optional_exclusive = parser_optional.add_mutually_exclusive_group()
        parser_optional_exclusive.add_argument(
            "-c", "--create",
            required=False,
            action='store_true',
            help="Create this new task")
        parser_optional_exclusive.add_argument(
            "-s", "--show",
            required=False,
            action='store_true',
            help="Show this task")

    @logger.catch(reraise=True)
    def build_command_uuid(self) -> None:
        """Build the uuid (of a task) command as a subparser"""
        parser = self.subparsers.add_parser(
            "uuid",
            help="Manage a task uuid")

        parser_required = parser.add_argument_group("required")
        parser_required.add_argument(
            "-u", "--uuid",
            required=True,
            type=str,
            help="Task uuid")

        parser_optional = parser.add_argument_group("optional")
        parser_optional.add_argument(
            "-E", "--send_email",
            required=False,
            action='store_true',
            help="Send an email about the new task event")
        parser_optional.add_argument(
            "-O", "--owner",
            required=False,
            type=str,
            help="Set task uuid owner")
        parser_optional.add_argument(
            "-C", "--complete",
            required=False,
            action='store_true',
            help="Set this task uuid complete")
        parser_optional.add_argument(
            "-D", "--due",
            required=False,
            type=str,
            help="Set task uuid due")
        parser_optional.add_argument(
            "-S", "--start",
            required=False,
            type=str,
            help="Set task uuid start")

        parser_optional_exclusive = parser_optional.add_mutually_exclusive_group()
        parser_optional_exclusive.add_argument(
            "-d", "--delete",
            required=False,
            action='store_true',
            help="Delete this task uuid")
        parser_optional_exclusive.add_argument(
            "-m", "--modify",
            required=False,
            action='store_true',
            help="Modify this task uuid")
        parser_optional_exclusive.add_argument(
            "-s", "--show",
            required=False,
            action='store_true',
            help="Show this task uuid")

if __name__=="__main__":
    parser = Parser()
    args = parser.parse()
    print(args)
