import os
from typing import Dict
import disnake
from disnake.ext import commands
from datetime import datetime, timedelta
from disnake.ext.commands.errors import CommandError
import timeago
from aiohttp_client_cache import CachedSession, SQLiteBackend
from tinydb.queries import Query
from db_utils import getDb


class Weather(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.key = os.getenv("WEATHER_KEY")
        self.url = "http://api.weatherapi.com/v1/current.json?key={}&q={}"

    def get_session(self) -> CachedSession:
        return CachedSession(cache=SQLiteBackend(
            cache_name="weather_cache",
            expire_after=timedelta(minutes=30),
            allowed_codes=(200,),  # cache successful responses only
        ))

    def make_embed(self, weatherInfo, measurementUnits):
        current: Dict = weatherInfo["current"]
        last_updated_epoch = current["last_updated_epoch"]
        last_updated_date = datetime.fromtimestamp(last_updated_epoch)
        now = datetime.now()
        last_updated_ago = timeago.format(last_updated_date, now)
        if measurementUnits == "Metric":
            temp = f"{current['temp_c']} C"
            feels_like = f"{current['feelslike_c']} C"
            wind_speed = f"{current['wind_kph']} kph"
        elif measurementUnits == "Imperial":
            temp = f"{current['temp_f']} F"
            feels_like = f"{current['feelslike_f']} F"
            wind_speed = f"{current['wind_mph']} mph"
        else:
            print(f"unrecognized value of measurementUnits={measurementUnits}")
            print("Expected 'Metric' or 'Imperial'")
            raise CommandError

        return (disnake.Embed(title=f"Weather for {weatherInfo['location']['name']}, {weatherInfo['location']['country']}")
                .add_field("Temperature", temp)
                .add_field("Feels like", feels_like)
                .add_field("Condition", current["condition"]["text"])
                .add_field("Wind speed", wind_speed)
                .add_field("Wind direction", current["wind_dir"])
                .add_field("Last updated ", last_updated_ago)
                .set_thumbnail("http:" + current["condition"]["icon"]))

    @commands.slash_command()
    async def weather(self, inter: disnake.ApplicationCommandInteraction, location: str) -> None:
        """Get the weather

        Parameters
        ----------
        location: A city name, zip/postcode, or airport code
        """
        await inter.response.defer()

        db = getDb()
        User = Query()
        row = db.table("users").get(User.id == inter.author.id)
        measurementUnits = row['measurementUnits'] if row else "Metric"

        async with self.get_session() as session:
            resp = await session.get(self.url.format(self.key, location))
            weatherInfo = await resp.json()
            if weatherInfo.get("error"):
                return await inter.send(weatherInfo["error"]["message"])

        embed = self.make_embed(weatherInfo, measurementUnits)
        await inter.send(embed=embed)


def setup(bot):
    bot.add_cog(Weather(bot))
