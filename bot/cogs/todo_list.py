from asyncio import sleep
from pathlib import Path
from bot.settings import BASE_DIR
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command
import json
import os


def update_of_todos(ctx, todos):
    """This will create a todo list from todos"""

    if Path(f"{BASE_DIR}/todo_list_data.json").is_file():  # Checks file if it exists
        print("File exist")

        if (
            os.stat(f"{BASE_DIR}/todo_list_data.json").st_size > 0
        ):  # This will check if the file is NOT empty

            with open(f"{BASE_DIR}/todo_list_data.json", "r") as read:
                todo_file_read = json.load(read)

                if (
                    str(ctx.author.id)
                ) not in todo_file_read:  # If key does not exist, a new dictionary is created
                    todo_file_read[str(ctx.author.id)] = {
                        num: todo.strip().rstrip()
                        for num, todo in enumerate(todos.split(","), start=1)
                    }

                else:  # If key exists, this will auto merge the current dictionary with the new dictionary
                    todo_file_read[str(ctx.author.id)] = {
                        **todo_file_read[str(ctx.author.id)],
                        **{
                            num: todo.strip().rstrip()
                            for num, todo in enumerate(
                                todos.split(","),
                                start=len(todo_file_read[str(ctx.author.id)]) + 1,
                            )
                        },
                    }

            with open(f"{BASE_DIR}/todo_list_data.json", "w") as update_write:
                # Writes newly updated dictionary and dump it to a json file.
                print(todo_file_read)
                json.dump(todo_file_read, fp=update_write)

        elif (
            os.stat(f"{BASE_DIR}/todo_list_data.json").st_size == 0
        ):  # If file is empty, this elif block will run
            with open(f"{BASE_DIR}/todo_list_data.json", "w") as update_write:
                json.dump({}, fp=update_write)

                with open(f"{BASE_DIR}/todo_list_data.json", "r") as read:
                    todo_file_read = json.load(read)
                    todo_file_read[str(ctx.author.id)] = {
                        num: todo.strip().rstrip()
                        for num, todo in enumerate(todos.split(","), start=1)
                    }
                    json.dump(todo_file_read, fp=update_write)

    else:  # If file does not exist, a new todo list will be created
        print("File does not exist")
        with open(f"{BASE_DIR}/todo_list_data.json", "w+") as to_write:
            todo_dict = {
                ctx.author.id: {
                    num: todo.strip().rstrip()
                    for num, todo in enumerate(todos.split(","), start=1)
                }
            }
            json.dump(todo_dict, fp=to_write)


class TodoList(Cog):
    """A simple command that creates a todo_list that will benefit the users."""

    def __init__(self, bot: Bot):
        self.bot = bot

        self.add_to_todo_list_tasks = {}
        self.delete_from_todo_list_tasks = {}

    async def todo_list_wrapper(self, ctx, task_type="todo_list", *, todos=None):
        """Wrapper function for todo list to allow the todos to be created on function call"""

        if task_type == "todo_list":
            self.add_to_todo_list_tasks[ctx.author.id] += 1
        elif task_type == "delete_todo":
            self.delete_from_todo_list_tasks[ctx.author.id] += 1

        @tasks.loop(count=1)
        async def delay_for_completion():
            """Sets a delay for the todo list to complete"""

            await sleep(1)

        @delay_for_completion.after_loop
        async def genesis_of_todo_list():
            """
            After the delay is complete, this function will execute.
            """

            if task_type == "todo_list":
                update_of_todos(ctx=ctx, todos=todos)
                await ctx.send(f"{ctx.author.mention}, your to do list is ready!")

            self.add_to_todo_list_tasks[ctx.author.id] -= 1

        delay_for_completion.start()

    @command(brief="Friendo will create a new todo list for you.")
    async def todo_list(self, ctx, *, todos=None):
        """Creates a todolist for the user."""

        if ctx.author.id not in self.add_to_todo_list_tasks:
            self.add_to_todo_list_tasks[ctx.author.id] = 0
        if self.add_to_todo_list_tasks[ctx.author.id] < 1:
            await self.todo_list_wrapper(ctx=ctx, task_type="todo_list", todos=todos)

    @command(brief="Friendo will present you your todo list.")
    async def show_todos(self, ctx):
        if Path(
            f"{BASE_DIR}/todo_list_data.json"
        ).is_file():  # Checks file if it exists
            print("File exist")

            if (
                os.stat(f"{BASE_DIR}/todo_list_data.json").st_size > 0
            ):  # This will check if the file is NOT empty

                with open(f"{BASE_DIR}/todo_list_data.json", "r+") as read:
                    todo_file_read = json.load(read)
                    if str(ctx.author.id) in todo_file_read:
                        listings = "".join(
                            [
                                f"{num}: {todo}\n"
                                for num, todo in todo_file_read[
                                    str(ctx.author.id)
                                ].items()
                            ]
                        )
                        await ctx.send(
                            f"Your todo list is ready, {ctx.author.mention}:\n{listings}"
                        )
                    else:
                        await ctx.send("You have no existing entries")
            else:
                await ctx.send("Todo list file empty!")

        else:
            await ctx.send("Todo list file does not exist!")


def setup(bot: Bot) -> None:
    """Load the Todo_List cog."""
    bot.add_cog(TodoList(bot))
