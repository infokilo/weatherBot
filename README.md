# weatherBot
A simple weather bot for Discord. 

## Running on your own machine
### Setup

1. Install requirements: `poetry install`

1. Set up environment variables

    1. Make a file called ".env" and paste the following in:
    
        ```
        ENV=production
        BOT_TOKEN=<your bot's token>
        WEATHER_KEY=<an API key for https://www.weatherapi.com/ >
        ```
    
    1. Add the BOT_TOKEN and WEATHER_KEY
  
1. Start the bot: `poetry run python3 main.py`

