from asyncio import sleep
from settings import BASE_DIR
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

    async def todos_wrapper(
        self, ctx, text, msg="Todo List!", task_type="todolist", reason=None
    ):
        if task_type == "todolist":
            self.todos[ctx.author.id] += 1
        elif task_type == "del_todolist":
            self.del_todos[ctx.author.id] += 1
        @tasks.loop(count=1)
        async def create_todo_list():
            """Sets a delay for the todo_list to complete."""

            await sleep(2)

        @create_todo_list.after_loop
        async def after_create_todo_list():
            """After the delay is complete, it will message
            the user that his todo list is ready (or a todo is deleted in the todolist)."""

            completion_message = msg

            if task_type == "todolist":
                
                if reason:
                    r = reason.split(",")
                    
                    for td in r:
                        self.the_todo.append(f"{td}\n")
                    
                    with open(
                        f"{BASE_DIR}save_data_td.JSON", "r+"
                    ) as read:  # This will read and convert json to dict.
                        file = json.load(read)
                        file.update([(ctx.author.id, self.the_todo)])
                
                        with open(
                            f"{BASE_DIR}/save_data_td.JSON", "w+"
                        ) as save:  # This will save the dict to json file.
                            json.dump(file, save)
                    
                            completion_message = (
                        f"{ctx.author.mention}, your todo list : {''.join(self.the_todo) + ' -> Ready!' }"
                    )
                
                else:
                    completion_message = (
                        f"{ctx.author.mention}, your todo list entry is empty. "
                        f"Please enter a todo list format (i.e `.todolist Make assignments, Learn Python`) with comma on "
                        f"every todo."
                    )
                
                self.todos[ctx.author.id] -= 1

            elif task_type == 'del_todolist':
                with open(f'{BASE_DIR}/save_data_td.JSON', 'r+') as read:
                    file = json.load(read)
                    r = reason.split(',')
                    if file[ctx.author.id]:
                        exists = [e + '\n' for e in file[ctx.author.id] if e + '\n' in r]
                        not_exists = [ne + '\n' for ne in r if ne + '\n' not in file[ctx.author.id]]
                    
                        for _ in exists:
                            file[ctx.author.id].__delitem__(file[ctx.author.id].index(_))
                    
                        with open(f'{BASE_DIR}/save_data_td.JSON', 'w+') as save:
                            json.dump(file, save)
                    
                        completion_message = (
                            f"{ctx.author.mention}, you have deleted the following todos: {''.join(not_exists)}\n"
                            f"The following entry or entries don't exist: {''.join(not_exists)}"
                        )

                    else:
                        completion_message = (
                            f"{ctx.author.mention}, you have no todos to delete. Maybe you made a mistake?"
                        )
                
                self.del_todolist[ctx.author.id] -= 1

            await ctx.send(completion_message)

        if text.startswith("todolist") or text.startswith('del_todolist'):
            create_todo_list.start()
        else:
            msg = """Please enter a todo list format (i.e `.todo Make assignments, Learn Python`) with comma on every todo.
            To delete a todo in your todolist do the example: `.del_todolist Make assignments, Learn Python.`"""
            await ctx.send(msg)


    @async del_todo_list_wrapper(
        self, ctx, text, msg="Delete Todo in Todo List!", task_type="del_todo_list", reason=None
    ):

    @command(brief="[todo some todos] [reason]")
    async def todolist(self, ctx, text, reason=None):
        """Creates a todo list for the user."""
        if ctx.author.id not in self.todos:
            self.todos[ctx.author.id] = 0
        if self.todos[ctx.author.id] < 1:
            await self.todos_wrapper(
                ctx=ctx, text=text, task_type="todolist", reason=reason
            )

    @command(brief="[del_todolist some todos] [reason]")
    async def del_todolist(self, ctx, text, reason=None):
        """Deletes a todo in the todolist for the user."""
        if ctx.author.id not in self.del_todos:
            self.del_todos[ctx.author.id] = 0
        if self.del_todos[ctx.author.id] < 1:
            await self.todos_wrapper(
                ctx=ctx, text=text, task_type="del_todolist",reason=reason
            )

def setup(bot: Bot) -> None:
    """Load the Todo_List cog."""
    bot.add_cog(TodoList(bot))
