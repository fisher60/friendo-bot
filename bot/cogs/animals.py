"""Commands for the animal module."""
import discord

from discord.ext.commands import Cog, bot, command, context


class AnimalCog(Cog, name='Animals'):
    """Commands for the animal finder."""

    def __init__(self, bot: bot.Bot):
        self.bot = bot

    @command(brief="Gets a random dog breed info and photo", aliases=['dogs'])
    async def dog(self, ctx: context.Context) -> None:
        """Gets random dog breed and facts about it."""
        url = 'https://api.thedogapi.com/v1/images/search'

        async with self.bot.session.get(url) as url:
            data = (await url.json())[0]

        image = data['url']

        try:
            data = data['breeds'][0]
        except IndexError:
            data = data['breeds']

        if not data:
            await self.dog(ctx)

        else:
            try:
                fields = [
                    (
                        'Weight',
                        f"{data['weight']['imperial']}lbs.",
                        True
                    ),
                    (
                        'Height',
                        f"{data['height']['imperial']}in.",
                        True
                    ),
                    (
                        'Breed Group',
                        data['breed_group'],
                        True
                    ),
                    (
                        'Life Span',
                        data['life_span'],
                        True
                    ),
                    (
                        'Bred for',
                        data['bred_for'],
                        False
                    ),
                    (
                        'Temperament',
                        data['temperament'],
                        False
                    )
                ]

                embed = discord.Embed(title=data['name'])
                embed.set_image(url=image)

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await ctx.send(embed=embed)

            except KeyError:
                await self.dog(ctx)

    @command(brief='Returns a random cat fact and image', aliases=['cats'])
    async def cat(self, ctx: context.Context) -> None:
        """Sets url and gets random cat image and fact."""
        url = 'https://api.thecatapi.com/v1/images/search'
        fact_url = 'https://some-random-api.ml/facts/cat'

        await self.animal_fact(ctx, url, fact_url, 'cat')

    @command(brief='Returns a random bird fact and image', aliases=['birds', 'birb', 'birbs'])
    async def bird(self, ctx: context.Context) -> None:
        """Sets url and gets random bird image and fact."""
        url = 'https://some-random-api.ml/img/birb'
        fact_url = 'https://some-random-api.ml/facts/bird'

        await self.animal_fact(ctx, url, fact_url, 'bird')

    @command(brief='Returns a random fox fact and image', aliases=['foxes'])
    async def fox(self, ctx: context.Context) -> None:
        """Sets url and gets random fox image and fact."""
        url = 'https://some-random-api.ml/img/fox'
        fact_url = 'https://some-random-api.ml/facts/fox'

        await self.animal_fact(ctx, url, fact_url, 'fox')

    @command(brief='Returns a random panada fact and image', aliases=['pandas'])
    async def panda(self, ctx: context.Context) -> None:
        """Sets url and gets random panda image and fact."""
        url = 'https://some-random-api.ml/img/panda'
        fact_url = 'https://some-random-api.ml/facts/panda'

        await self.animal_fact(ctx, url, fact_url, 'panda')

    async def animal_fact(self, ctx: context.Context, url: str, fact_url: str, animal: str) -> None:
        """Sends the embed for random animal and it's fact."""
        async with self.bot.session.get(url) as resp:
            if animal == 'cat':
                data = (await resp.json())[0]['url']
            else:
                data = (await resp.json())['link']

        async with self.bot.session.get(fact_url) as resp:
            fact = (await resp.json())['fact']

        embed = discord.Embed(title=f"Enjoy a {animal} picture", description=f"*Fun Fact:*\n{fact}")
        embed.set_image(url=data)
        await ctx.send(embed=embed)


def setup(bot: bot.Bot) -> None:
    """Sets up the cog."""
    bot.add_cog(AnimalCog(bot))
