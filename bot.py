import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
import os

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable privileged message content intent

# Initialize the bot with a command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def flightinfo(ctx, flight_number: str):
    load_dotenv()
    api_key = os.getenv('API_KEY')  
    url = f'http://api.aviationstack.com/v1/flights?access_key={api_key}&flight_iata={flight_number}'
    response = requests.get(url)
    data = response.json()

    # Print the raw response for debugging
    print(data)

    if 'data' in data and len(data['data']) > 0:
        flight = data['data'][0]  # Assuming the first result is the flight you're looking for

        # Safely get nested data with .get(), providing default values
        airline = flight.get('airline', {}).get('name', 'Unknown airline')
        flight_date = flight.get('flight_date', 'Unknown date')

        departure = flight.get('departure', {})
        departure_airport = departure.get('airport', 'Unknown departure airport')
        departure_time = departure.get('estimated', 'Unknown departure time')
        departure_gate = departure.get('gate', 'Unknown gate')

        arrival = flight.get('arrival', {})
        arrival_airport = arrival.get('airport', 'Unknown arrival airport')
        arrival_time = arrival.get('estimated', 'Unknown arrival time')
        arrival_gate = arrival.get('gate', 'Unknown gate')

        # Check if aircraft data is available before accessing it
        if flight.get('aircraft'):
            aircraft_type = flight['aircraft'].get('registration', 'Unknown aircraft type')
        else:
            aircraft_type = 'Unknown aircraft type'

        message = (
            f"**Flight {flight_number} Information**\n"
            f"**Airline**: {airline}\n"
            f"**Date**: {flight_date}\n\n"
            f"**Departure**:\n"
            f"  - Airport: {departure_airport}\n"
            f"  - Time: {departure_time}\n"
            f"  - Gate: {departure_gate}\n\n"
            f"**Arrival**:\n"
            f"  - Airport: {arrival_airport}\n"
            f"  - Time: {arrival_time}\n"
            f"  - Gate: {arrival_gate}\n\n"
            f"**Aircraft Type**: {aircraft_type}"
        )
    else:
        message = f"No information found for flight {flight_number}."

    await ctx.send(message)

@bot.command()
async def aerospace_news(ctx):
    load_dotenv()
    api_key_news = os.getenv('API_KEY_NEWS')  
    url = f'https://newsapi.org/v2/everything?q=aerospace&sortBy=publishedAt&apiKey={api_key_news}'
    response = requests.get(url)
    data = response.json()

    message = "**Latest Aerospace News:**\n\n"
    
    if data.get('status') == 'ok' and data.get('totalResults') > 0:
        articles = data.get('articles', [])
        message = "**Latest Aerospace News:**\n\n"

        for article in articles[:5]:
            title = article.get('title', 'No title available')
            description = article.get('description', 'No description available')
            url = article.get('url', 'No URL available')

            if title != 'No title available' and url != 'No URL available':
                message += f"**{title}**\n{description}\n[Read more]({url})\n\n"
    else:
        message = "No aerospace news found at the moment."

    await ctx.send(message)

#TOKEN
load_dotenv()
bot.run(os.getenv('TOKEN'))

