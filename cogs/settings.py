from disnake.ext import commands
import disnake
from db_utils import getDb
from tinydb import Query


class UnitSelection(disnake.ui.Select):
    def __init__(self):
        # The placeholder is what will be shown when no option is chosen
        super().__init__(
            placeholder="Units of measurement",
            options=[
                disnake.SelectOption(
                    label="Metric", description="Use metric units (celsius, meters)"
                ),
                disnake.SelectOption(
                    label="Imperial", description="Use imperial units (fahrenheit, miles)"
                ),
            ],
        )

    async def callback(self, inter: disnake.MessageInteraction):
        id = inter.author.id
        db = getDb()
        User = Query()
        db.table("users").upsert(
            {"id": id, "measurementUnits": self.values[0]},
            User.id == id
        )
        await inter.response.send_message(
            f"Successfully set units of measurement! {self.values[0]}", ephemeral=True
        )


class SettingsView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(UnitSelection())


class Settings(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def settings(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send("Your personal settings:", view=SettingsView(), ephemeral=True)


def setup(bot):
    bot.add_cog(Settings(bot))
