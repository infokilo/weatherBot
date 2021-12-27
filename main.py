from keep_alive import keep_alive
import os
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv("ENV")
if ENV == "production":
    TOKEN = os.getenv("BOT_TOKEN")
    test_guilds = None
else:
    TOKEN = os.getenv("TEST_TOKEN")
    test_guilds = [917650270480109609]

if not TOKEN:
    name = "BOT_TOKEN" if ENV == "production" else "TEST_TOKEN"
    raise AttributeError(f"{name} environment variable not found")

prefix = commands.when_mentioned
bot = commands.Bot(command_prefix=prefix, test_guilds=test_guilds)
bot.help_command = None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.slash_command()
async def ping(inter):
    await inter.send("Pong! Bot latency: " + str(1000 * bot.latency) + "ms")


@bot.command(aliases=["reload"])
@commands.is_owner()
async def refresh(ctx):
    for cog in cogs:
        bot.reload_extension(cog)

    print('Reloaded all cogs!')
    await ctx.send("Reloaded all cogs!")


cogs = [
    "cogs.weather",
    "cogs.settings",
]

for cog in cogs:
    bot.load_extension(cog)

keep_alive()

bot.run(TOKEN)
