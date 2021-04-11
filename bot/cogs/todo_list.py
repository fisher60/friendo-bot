from asyncio import sleep
import json
import logging
import os
from pathlib import Path
from typing import Tuple
import aiofiles

from discord import Colour, Embed
from discord.ext import tasks
from discord.ext.commands import Cog, Context, command

from bot.bot import Friendo

log = logging.getLogger(__name__)

TODO_FILE = Path.cwd() / 'todo_list_data.json'


async def update_of_todos(ctx: Context, todos: str) -> None:
    """This will create a todo list from todos."""
    todos = [t.strip() for t in todos.split(",") if t.strip() != ""]

    if TODO_FILE.is_file():  # Checks file if it exists
        log.info("todo_list_data.json exists")

        # This will check if the file is NOT empty
        if os.stat(TODO_FILE).st_size > 0:

            async with aiofiles.open(TODO_FILE, "r") as read:
                todo_file_read = json.loads(await read.read())

                # If key does not exist, a new dictionary is created
                if str(ctx.author.id) not in todo_file_read:
                    todo_file_read[str(ctx.author.id)] = {
                        num: todo.strip().rstrip()
                        for num, todo in enumerate(todos, start=1)
                    }

                # If key exists, this will auto merge the current dictionary with the new dictionary
                else:
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

            async with aiofiles.open(TODO_FILE, "w") as update_write:
                # Writes newly updated dictionary and dump it to a json file.
                await update_write.write(json.dumps(todo_file_read))

        # If file is empty, this elif block will run
        elif os.stat(TODO_FILE).st_size == 0:
            async with aiofiles.open(TODO_FILE, "w") as update_write:
                await update_write.write(json.dumps({}))

                async with aiofiles.open(TODO_FILE, "r") as read:
                    todo_file_read = json.loads(await read.read())
                    todo_file_read[str(ctx.author.id)] = {
                        num: todo.strip().rstrip()
                        for num, todo in enumerate(todos, start=1)
                    }
                    await update_write.write(json.dump(todo_file_read))

    # If file does not exist, a new todo list will be created
    else:
        log.info("todo_list_data.json does not exist")
        async with aiofile.open(TODO_FILE, "w+") as to_write:
            todo_dict = {
                ctx.author.id: {
                    num: todo.strip().rstrip()
                    for num, todo in enumerate(todos, start=1)
                }
            }
            await to_write.write(json.dumps(todo_dict))


async def deletion_of_todos(ctx: Context, keys_to_delete: str) -> bool:
    """This will delete some todos using specified keys."""
    k = [c.strip().rstrip() for c in keys_to_delete.split(",") if c.strip() != ""]
    if TODO_FILE.is_file():
        log.info("todo_list_data.json exists")
        if (
                os.stat(TODO_FILE).st_size > 0
        ):  # This will check if the file is NOT empty
            async with aiofile.open(TODO_FILE, "r") as read:
                todo_file_read = json.loads(await read.read())
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
                    async with aiofiles.open(TODO_FILE, "w") as update:
                        await update.write(json.dumps(todo_file_read))

                else:
                    return False  # This will be used later for ctx.send
        else:
            return False  # This will be used later for ctx.send

        return True


class TodoList(Cog):
    """A simple command that creates a todo_list that will benefit the users."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @staticmethod
    async def todo_list_wrapper(ctx: Context, task_type: str = "todo_list", *,
                                todos: Tuple[str] = None) -> None:
        """Wrapper function for todo list to allow the todos to be created on function call."""
        pass

        @tasks.loop(count=1)
        async def delay_for_completion() -> None:
            """Sets a pseudodelay for the todo list to complete."""
            await sleep(1)

        @delay_for_completion.after_loop
        async def genesis_of_todo_list() -> None:
            """After the delay is complete, this function will execute."""
            if task_type == "todo_list":
                await update_of_todos(ctx=ctx, todos=todos)
                embed_msg = Embed(
                    title=f"{ctx.author}, your todo list is ready!",
                    color=Colour.green(),
                )
                await ctx.send(embed=embed_msg)

            elif task_type == "delete_todos":
                seek = await deletion_of_todos(ctx=ctx, keys_to_delete=todos)
                if seek:
                    embed_msg = Embed(
                        title=f"{ctx.author}, todos have been deleted",
                        description="Please check using `.showtodos`. Woof!",
                    )
                    await ctx.send(embed=embed_msg)
                else:
                    embed_msg = Embed(
                        title=f"{ctx.author}, failed to delete.",
                        description="Probably file failed to initialize or you have not created a todo list, "
                                    "yet.\nPlease check using `.show_todos`. Woof!",
                    )
                    await ctx.send(embed=embed_msg)

        delay_for_completion.start()

    @command(brief="Friendo will create a new todo list for you.", aliases=("todo", "todos", "todolist"))
    async def todo_list(self, ctx: Context, *, todos: str = None) -> None:
        """Creates a todo list for the user."""
        await self.todo_list_wrapper(ctx=ctx, task_type="todo_list", todos=todos)

    @command(brief="Friendo deletes todos by specified keys")
    async def delete_todos(self, ctx: Context, *, todos: str = None) -> None:
        """Deletes todos from a todo list for the user."""
        await self.todo_list_wrapper(ctx=ctx, task_type="delete_todos", todos=todos)

    @command(brief="Friendo will present you your todo list.", name="showtodos")
    async def show_todos(self, ctx: Context) -> None:
        """Shows the todo list of the user."""
        if TODO_FILE.is_file():
            log.info("todo_list_data.json exists")

        else:
            async with aiofiles.open(TODO_FILE, "w") as f:
                await f.write(f"{''}")

        # This will check if the file is NOT empty
        if os.stat(TODO_FILE).st_size > 0:
            async with aiofiles.open(TODO_FILE, "r+") as read:
                todo_file_read = json.loads(await read.read())

                if str(ctx.author.id) in todo_file_read:
                    if todo_file_read[str(ctx.author.id)]:
                        listings = "".join(
                            [f"{num}: {todo}\n" for num, todo in todo_file_read[str(ctx.author.id)].items()])
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
    async def nuke_todos(self, ctx: Context) -> None:
        """This will delete the whole todo list of a specific user. Good if user has too many todos."""
        if TODO_FILE.is_file():
            if os.stat(TODO_FILE).st_size > 0:

                async with aiofiles.open(TODO_FILE, "r+") as read:
                    todo_file_read = json.loads(await read.read())
                    if str(ctx.author.id) in todo_file_read:
                        if todo_file_read[str(ctx.author.id)]:
                            todo_file_read[str(ctx.author.id)] = {}
                            embed_nuked_todos = Embed(
                                title="NUKED! :exploding_head:",
                                description=f"Your todo list is now empty {ctx.author}.",
                                color=Colour.dark_purple(),
                            )
                            async with aiofiles.open(
                                    TODO_FILE, "w+"
                            ) as update:
                                await update.write(json.dumps(todo_file_read))
                            await ctx.send(embed=embed_nuked_todos)
                        else:
                            await ctx.send(
                                embed=Embed(
                                    title="You have no existing entries! Nothing to nuke :exploding_head:!",
                                    color=Colour.red(),
                                )
                            )
                    else:
                        await ctx.send(
                            embed=Embed(
                                title="You have no existing entries! Nothing to nuke :exploding_head:!",
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


def setup(bot: Friendo) -> None:
    """Load the Todo_List cog."""
    bot.add_cog(TodoList(bot))
