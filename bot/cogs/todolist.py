from asyncio import sleep
from bot.settings import BASE_DIR
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command
import json


class TodoList(Cog):
    """A simple command that creates a todo_list that will benefit the users."""

    def __init__(self, bot: Bot):
        self.bot = bot

        self.index = 0
        self.todos = {}
        self.del_todos = {}
        self.the_todo = []
        self.del_the_todo = []

    async def todos_wrapper(
        self, ctx, msg="Todo List!", task_type="todolist", *, some_todos=None
    ):
        if task_type == "todolist":
            self.todos[ctx.author.id] += 1

        @tasks.loop(count=1)
        async def create_todo_list():
            """Sets a delay for the todo_list to complete."""

            await sleep(2)

        @create_todo_list.after_loop
        async def after_create_todo_list():
            """After the delay is complete, it will message
            the user that his todolist is ready (or a todo is deleted in the todolist)."""

            if task_type == "todolist":
                print("some_todos:", some_todos)
                if some_todos:
                    r = some_todos.split(",")
                    for td in r:
                        if td == "":
                            continue
                        else:
                            self.the_todo.append(f"{td.strip(' ').rstrip(' ')}\n")

                    with open(f"{BASE_DIR}/save_data_td.JSON", "r+") as read:
                        file = json.load(read)
                        file.update([(str(ctx.author.id), self.the_todo)])

                        with open(f"{BASE_DIR}/save_data_td.JSON", "w+") as save:
                            json.dump(file, save)

                            completion_message = f"{ctx.author.mention}, your todo list:\n{''.join(self.the_todo) + '-> Ready!'}"
                            await ctx.send(completion_message)
                else:
                    completion_message = (
                        f"{ctx.author.mention}, your todo list entry is empty. "
                        f"Please enter a todo list format (i.e `.todolist Make assignments, Learn Python`) with comma "
                        f"on "
                        f"every todo."
                    )
                    await ctx.send(completion_message)

                self.todos[ctx.author.id] -= 1
            elif task_type == "del_todos":
                if some_todos:
                    r = some_todos.split(",")
                    for td in r:
                        if td == "":
                            continue
                        else:
                            self.del_the_todo.append(f"{td.strip(' ').rstrip(' ')}\n")

                    with open(f"{BASE_DIR}/save_data_td.JSON", "r+") as read:
                        f = json.load(read)
                        new = [
                            x
                            for x in f[str(ctx.author.id)]
                            if x not in self.del_the_todo
                        ]
                        removed = [
                            x for x in f[str(ctx.author.id)] if x in self.del_the_todo
                        ]
                        f[str(ctx.author.id)] = new
                        with open(f"{BASE_DIR}/save_data_td.JSON", "w+") as save:
                            json.dump(f, save)
                            completion_message = (
                                f"{ctx.author.mention}, your todo list after deletion:\n{''.join(new)}\n"
                                f"Removed todos:\n{''.join(removed)}"
                            )
                            await ctx.send(completion_message)
                else:
                    completion_message = (
                        f"{ctx.author.mention}, your todo list entry is empty. "
                        f"Please enter a todo list format (i.e `.del_todos Make assignments, Learn Python`) with comma "
                        f"on "
                        f"every todo."
                    )
                    await ctx.send(completion_message)

        create_todo_list.start()

    @command(brief="A simple todolist in text")
    async def todolist(self, ctx, *, some_todos=None):
        """Creates a todolist for the user."""

        if ctx.author.id not in self.todos:
            self.todos[ctx.author.id] = 0
        if self.todos[ctx.author.id] < 1:
            await self.todos_wrapper(
                ctx=ctx, task_type="todolist", some_todos=some_todos
            )

    @command(brief="Deletes some todos from a todolist")
    async def del_todos(self, ctx, *, some_todos=None):
        """Deletes todos from a todolist for the user."""

        if ctx.author.id not in self.del_todos:
            self.del_todos[ctx.author.id] = 0
        if self.del_todos[ctx.author.id] < 1:
            await self.todos_wrapper(
                ctx=ctx, task_type="del_todos", some_todos=some_todos
            )

    @command(brief="Checks your current todolist")
    async def check_todos(self, ctx):
        """Reads json and shows current todolist of user."""

        with open(f"{BASE_DIR}/save_data_td.JSON", "r+") as read:
            file = json.load(read)
            try:
                await ctx.send(
                    f"Your current todolist:\n{''.join(file[str(ctx.author.id)])}"
                )
            except KeyError:
                await ctx.send("No todolist found. You have yet to create a todolist.")

    @command(brief="Destroys all todos from your todolist in one go")
    async def empty_todolist(self, ctx):
        """Empties the user's todolist."""

        with open(f"{BASE_DIR}/save_data_td.JSON", "r+") as read:
            file = json.load(read)
            try:
                if file[str(ctx.author.id)]:
                    temporary = file.pop(str(ctx.author.id))
                    with open(f"{BASE_DIR}/save_data_td.JSON", "w+") as save:
                        json.dump(file, save)
                        await ctx.send(
                            f"Successfully deleted your todolist.\nYour todolist before deletion:\n{''.join(temporary)}"
                        )
                else:
                    await ctx.send("Your todolist is already empty.")
            except KeyError:
                await ctx.send("Todolist empty. You have yet to create a todolist.")


def setup(bot: Bot) -> None:
    """Load the Todo_List cog."""
    bot.add_cog(TodoList(bot))
