import json
import os
from asyncio import sleep
from pathlib import Path
from bot.settings import BASE_DIR
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command
from discord import Embed, Colour


def update_of_todos(ctx, todos):
    """This will create a todo list from todos"""

    todos = [t.strip() for t in todos.split(",") if t.strip() != ""]

    if Path(f"{BASE_DIR}/todo_list_data.json").is_file():  # Checks file if it exists
        print("File exists")

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
                        for num, todo in enumerate(todos, start=1)
                    }

                else:  # If key exists, this will auto merge the current dictionary with the new dictionary
                    todo_file_read[str(ctx.author.id)] = {
                        **todo_file_read[str(ctx.author.id)],
                        **{
                            num: todo.strip().rstrip()
                            for num, todo in enumerate(
                                todos,
                                start=len(todo_file_read[str(ctx.author.id)]) + 1,
                            )
                        },
                    }

            with open(f"{BASE_DIR}/todo_list_data.json", "w") as update_write:
                # Writes newly updated dictionary and dump it to a json file.
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
                        for num, todo in enumerate(todos, start=1)
                    }
                    json.dump(todo_file_read, fp=update_write)

    else:  # If file does not exist, a new todo list will be created
        print("File does not exist")
        with open(f"{BASE_DIR}/todo_list_data.json", "w+") as to_write:
            todo_dict = {
                ctx.author.id: {
                    num: todo.strip().rstrip()
                    for num, todo in enumerate(todos, start=1)
                }
            }
            json.dump(todo_dict, fp=to_write)


def deletion_of_todos(
    ctx, keys_to_delete
):  # In this function, todos here refers to keys in the dictionary.
    """This will delete some todos using specified keys"""

    k = [c.strip().rstrip() for c in keys_to_delete.split(",") if c.strip() != ""]
    if Path(f"{BASE_DIR}/todo_list_data.json").is_file():
        print("File exists")
        if (
            os.stat(f"{BASE_DIR}/todo_list_data.json").st_size > 0
        ):  # This will check if the file is NOT empty
            with open(f"{BASE_DIR}/todo_list_data.json", "r") as read:
                todo_file_read = json.load(read)
                if (
                    str(ctx.author.id)
                ) in todo_file_read:  # If key does not exist, a new dictionary is created
                    for _ in k:
                        if _ in todo_file_read[str(ctx.author.id)]:
                            todo_file_read[str(ctx.author.id)].pop(_)

                    todo_file_read[str(ctx.author.id)] = {
                        num: todo
                        for num, todo in enumerate(
                            todo_file_read[str(ctx.author.id)].values(), start=1
                        )
                    }
                    with open(f"{BASE_DIR}/todo_list_data.json", "w") as update:
                        json.dump(todo_file_read, fp=update)

                else:
                    return False  # This will be used later for ctx.send
        else:
            return False  # This will be used later for ctx.send

        return True


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
        elif task_type == "delete_todos":
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
                embed_msg = Embed(
                    title=f"{ctx.author}, your todo list is ready!",
                    color=Colour.green(),
                )
                await ctx.send(embed=embed_msg)

                self.add_to_todo_list_tasks[ctx.author.id] -= 1

            elif task_type == "delete_todos":
                seek = deletion_of_todos(ctx=ctx, keys_to_delete=todos)
                if seek:
                    embed_msg = Embed(
                        title=f"{ctx.author}, todos have been deleted",
                        description="Please check using `.show_todos`. Woof!",
                    )
                    await ctx.send(embed=embed_msg)
                else:
                    embed_msg = Embed(
                        title=f"{ctx.author}, failed to delete.",
                        description="Probably file failed to initialize or you have not created a todo list, "
                        "yet.\nPlease check using `.show_todos`. Woof!",
                    )
                    await ctx.send(embed=embed_msg)

                self.delete_from_todo_list_tasks[ctx.author.id] -= 1

        delay_for_completion.start()

    @command(
        brief="Friendo will create a new todo list for you.",
        aliases=["todo", "todos", "todolist"],
    )
    async def todo_list(self, ctx, *, todos=None):
        """Creates a todo list for the user."""

        if ctx.author.id not in self.add_to_todo_list_tasks:
            self.add_to_todo_list_tasks[ctx.author.id] = 0
        if self.add_to_todo_list_tasks[ctx.author.id] < 1:
            await self.todo_list_wrapper(ctx=ctx, task_type="todo_list", todos=todos)

    @command(brief="Friendo deletes todos by specified keys")
    async def delete_todos(self, ctx, *, todos=None):
        """Deletes todos from a todo list for the user."""

        if ctx.author.id not in self.delete_from_todo_list_tasks:
            self.delete_from_todo_list_tasks[ctx.author.id] = 0
        if (
            self.delete_from_todo_list_tasks[ctx.author.id] < 1
        ):  # todos here are keys not long strings.
            await self.todo_list_wrapper(ctx=ctx, task_type="delete_todos", todos=todos)

    @command(brief="Friendo will present you your todo list.", name="showtodos")
    async def show_todos(self, ctx):
        """Shows the todo list of the user."""

        if Path(
            f"{BASE_DIR}/todo_list_data.json"
        ).is_file():  # Checks file if it exists
            print("File exist")

        else:
            with open(Path(f"{BASE_DIR}/todo_list_data.json"), "w") as f:
                f.write("{}")

        if (
            os.stat(f"{BASE_DIR}/todo_list_data.json").st_size > 0
        ):  # This will check if the file is NOT empty

            with open(f"{BASE_DIR}/todo_list_data.json", "r+") as read:
                todo_file_read = json.load(read)
                if str(ctx.author.id) in todo_file_read:
                    if todo_file_read[str(ctx.author.id)]:
                        listings = "".join(
                            [
                                f"{num}: {todo}\n"
                                for num, todo in todo_file_read[
                                    str(ctx.author.id)
                                ].items()
                            ]
                        )
                        embed_show_todos = Embed(
                            title=f"Your todo list is here, {ctx.author}",
                            description=listings,
                            color=Colour.blurple(),
                        )
                        await ctx.send(embed=embed_show_todos)
                    else:
                        await ctx.send(
                            embed=Embed(
                                title="You have no existing entries! Grrrr!",
                                color=Colour.red(),
                            )
                        )
                else:
                    await ctx.send(
                        embed=Embed(
                            title="You have no existing entries! Grrrr!",
                            color=Colour.red(),
                        )
                    )
        else:
            await ctx.send(
                embed=Embed(title="Todo list file empty! Arf!", color=Colour.red())
            )

    @command(
        brief="Friendo will nuke your whole todo list to emptiness.",
        aliases=["deletetodos", "nuketodos"],
    )
    async def nuke_todos(self, ctx):
        """This will delete the whole todo list of a specific user. Good if user has too many todos."""

        if Path(
            f"{BASE_DIR}/todo_list_data.json"
        ).is_file():  # Checks file if it exists
            if (
                os.stat(f"{BASE_DIR}/todo_list_data.json").st_size > 0
            ):  # This will check if the file is NOT empty

                with open(f"{BASE_DIR}/todo_list_data.json", "r+") as read:
                    todo_file_read = json.load(read)
                    if str(ctx.author.id) in todo_file_read:
                        if todo_file_read[str(ctx.author.id)]:
                            todo_file_read[str(ctx.author.id)] = {}
                            embed_nuked_todos = Embed(
                                title=f"NUKED! :exploding_head:",
                                description=f"Your todo list is now empty {ctx.author}.",
                                color=Colour.dark_purple(),
                            )
                            with open(
                                f"{BASE_DIR}/todo_list_data.json", "w+"
                            ) as update:
                                json.dump(todo_file_read, fp=update)
                            await ctx.send(embed=embed_nuked_todos)
                        else:
                            await ctx.send(
                                embed=Embed(
                                    title="You have no existing entries! Grrrr! Nothing to nuke :exploding_head:!",
                                    color=Colour.red(),
                                )
                            )
                    else:
                        await ctx.send(
                            embed=Embed(
                                title="You have no existing entries! Grrrr! Nothing to nuke :exploding_head:!",
                                color=Colour.red(),
                            )
                        )
            else:
                await ctx.send(
                    embed=Embed(
                        title="Todo list file empty! Arf! Nothing to nuke :exploding_head:!",
                        color=Colour.red(),
                    )
                )

        else:
            await ctx.send(
                embed=Embed(
                    title="Todo list file does not exist! Nothing to nuke :exploding_head:",
                    color=Colour.red(),
                )
            )


def setup(bot: Bot) -> None:
    """Load the Todo_List cog."""
    bot.add_cog(TodoList(bot))
