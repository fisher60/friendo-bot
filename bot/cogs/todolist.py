from asyncio import sleep
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command
import json


class TodoList(Cog):
    """A simple command that creates a todo_list that will benefit the users."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.index = 0
        self.todos = {}
        self.the_todo = []

    async def todos_wrapper(
            self, ctx, text, msg="Todo List!", task_type="todo_list", reason=None
    ):
        if task_type == "todo_list":
            self.todos[ctx.author.id] += 1

        @tasks.loop(count=1)
        async def create_todo_list():
            """Sets a delay for the todo_list to complete."""

            await sleep(2)

        @create_todo_list.after_loop
        async def after_create_todo_list():
            """After the delay is complete, it will message
            the user that his todo list is ready."""

            completion_message = msg

            if task_type == 'todo_list':
                if reason:
                    r = reason.split(',')
                    for num, td in enumerate(r):
                        self.the_todo.append(f"{num}. {td}\n")
                    completion_message = (
                        f"{ctx.author.mention}, your todo list : {''.join(self.the_todo) + ' -> Ready!' }"
                    )
                else:
                    completion_message = (
                        f"{ctx.author.mention}, your todo list is empty. "
                        f"Please enter a todo list format (i.e .todo Make assignments, Learn Python) with comma on "
                        f"every todo."
                    )
                self.todos[ctx.author.id] -= 1

            await ctx.send(completion_message)

        if text.startswith("todo"):
            create_todo_list.start()
        else:
            msg = "Please enter a todo list format (i.e .todo Make assignments, Learn Python) with comma on every todo."
            await ctx.send(msg)

    @command(brief="[todo some todos] [reason]")
    async def todo_list(self, ctx, text, reason=None):
        """Creates a todo list for the user"""
        if ctx.author.id not in self.todos:
            self.todos[ctx.author.id] = 0
        if self.todos[ctx.author.id] < 1:
            await self.todos_wrapper(
                ctx=ctx, text=text, task_type='todo_list', reason=reason
            )

    @command(brief="[delete todo some todos] [reason]")
    async def del_todo_list(self, ctx, text, reason=None):
        ...


def setup(bot: Bot) -> None:
    """Load the Todo_List cog."""
    bot.add_cog(TodoList(bot))
