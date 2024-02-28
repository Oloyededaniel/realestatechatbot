import discord
from discord.ext import commands
import json
import random
import nltk

nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Import functions from Radarestate.py
from Radarestate import preprocess_input, search_properties, greet, get_user_info

# Initialize intents
intents = discord.Intents.default()
intents.messages = True

# Initialize the bot with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

GREETINGS = ["hello", "hi", "yo", "hey", "greetings", "sup", "what's up"]
PROPERTY_REQUESTS = ["find me a property", "show me some properties", "search properties", "list properties", "property search", "looking for a property","searching for a property",
"show property available", "property listings", "property search","show me properties"]


# Define an event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(keyword in message.content.lower() for keyword in GREETINGS):
        await greet(message.channel)
        await message.channel.send("I am RadarBot, the Radar Estate Chatbot.")
        await message.channel.send("I can help you find properties based on your preferences.")

    elif any(keyword in message.content.lower() for keyword in PROPERTY_REQUESTS):
        await find_property(message.channel, message.author)
        #await feedback(message.channel)

    else:
        await bot.process_commands(message)


# Define a command to greet users
@bot.command()
async def greet(ctx):
    greetings = ['Hi!', 'Hello!', 'Hey there!',"Howdy","Greetings","sup"]
    await ctx.send(random.choice(greetings))

# Define a command to assist users
@bot.command()
async def assist(ctx):
    await ctx.send('I can help you find properties based on your preferences.')

# Define an event handler for when a command is not found
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't understand that command.")

# Define a command to handle user messages
async def find_property(ctx, author):
    try:
        await ctx.send("May I know your name?")
        name_message = await bot.wait_for('message', check=lambda message: message.author == author)
        name = name_message.content
        await ctx.send(f"\nHello, {name}! How can I assist you?")

        while True:
            await ctx.send("What is your budget?")
            budget_message = await bot.wait_for('message', check=lambda message: message.author == author)
            budget_str = budget_message.content
            try:
                budget = float(budget_str.replace(',', ''))
                if budget <= 0:
                    await ctx.send("Please enter a valid budget (a positive number).")
                else:
                    break
            except ValueError:
                await ctx.send("Please enter a valid budget (a number).")

        while True:
            await ctx.send("Where are you looking for properties?")
            location_message = await bot.wait_for('message', check=lambda message: message.author == author)
            location = location_message.content

            # Load locations from the dataset
            with open('data.json', 'r') as f:
                property_data = json.load(f)
            locations = {property['area'].lower() for property in property_data["property"]}

            if location.lower() not in locations:
                await ctx.send("Sorry, that location is not available. Please provide a valid location.")
                continue
            else:
                break

        await ctx.send("How many bedrooms do you need?")
        while True:
            bedrooms_message = await bot.wait_for('message', check=lambda message: message.author == author)
            try:
                bedrooms = int(bedrooms_message.content)
                if bedrooms <= 0:
                    await ctx.send("Please enter a valid number of bedrooms (a positive integer).")
                else:
                    break
            except ValueError:
                await ctx.send("Please enter a valid number of bedrooms (a positive integer).")

        await ctx.send("How many bathrooms do you need?")
        while True:
            bathrooms_message = await bot.wait_for('message', check=lambda message: message.author == author)
            try:
                bathrooms = int(bathrooms_message.content)
                if bathrooms <= 0:
                    await ctx.send("Please enter a valid number of bathrooms (a positive integer).")
                else:
                    break
            except ValueError:
                await ctx.send("Please enter a valid number of bathrooms (a positive integer).")

        await ctx.send("\nThank you for providing the details. Let's find properties within your criteria:")

        with open('data.json', 'r') as f:
            property_data = json.load(f)

        property_types = set(property['type'].lower() for property in property_data["property"])

        while True:
            await ctx.send("Ask me about a property [Duplex or Studio or Single Family or type 'quit' to exit].")
            user_input_message = await bot.wait_for('message', check=lambda message: message.author == author)
            user_input = user_input_message.content.lower()

            if user_input.lower() == "quit":
                await ctx.send("\nThank you for using the Radar Estate Chatbot!")
                break

            if user_input not in property_types:
                await ctx.send(
                    "Sorry, that property type is not available. Please choose one of the following property types:")
                await ctx.send(", ".join(property_types))
                continue

            query = preprocess_input(user_input)

            search_results = search_properties(query, property_data)

            found_matching_properties = False
            count = 0
            for result in search_results:
                price = result["price"]
                if (
                    price <= budget
                    and result["area"].lower() == location.lower()
                    and result["beds"] >= bedrooms
                    and result["baths"] >= bathrooms
                ):
                    found_matching_properties = True
                    count += 1
                    response = (
                        f"\n***Property {count}:***\n"
                        f"ID: {result['id']}\n"
                        f"Type: {result['type']}\n"
                        f"Location: {result['area']}\n"
                        f"Address: {result['address']}\n"
                        f"City: {result['city']}\n"
                        f"Price: ${price:,.2f}\n"
                        f"Bedrooms: {result['beds']}\n"
                        f"Bathrooms: {result['baths']}\n"
                        f"Floorspace: {result['floorspace']} sq ft\n"
                        f"Maintenance: ${result['maintenance']:,.2f}\n"
                        f"Parking: {result['parking']} vehicles\n"
                        f"Construction: {', '.join(result['construction'])}\n"
                    )
                    await ctx.send(response)

            if not found_matching_properties:
                await ctx.send("\nNo properties found matching your search.")

            await ctx.send("\nDo you have any other questions? (yes/no): ")
            while True:
                choice_message = await bot.wait_for('message', check=lambda message: message.author == author)
                choice = choice_message.content.lower()
                if choice == "yes":
                    break
                elif choice == "no":
                    await ctx.send(
                        "\nIf you have any further questions or need assistance, feel free to reach out to us at *radarestate@gmail.com*. We're here to help!"
                    )
                    await ctx.send("\nThank you for using the Radar Estate Chatbot!")
                    return
                else:
                    await ctx.send("Invalid response. Please enter 'yes' or 'no'.")

           # await feedback(ctx)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


# Define a command to handle user feedback
@bot.command()
async def feedback(ctx):
    await ctx.send("Please provide your feedback or rate the usefulness of the bot's responses on a scale of 1 to 5.")

    # Wait for user feedback
    feedback_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    feedback_text = feedback_message.content

    await ctx.send("Thank you for your feedback!")



# Run the bot with your Discord bot token
bot.run('MTIwODUxNzcwNDMzMjM1MzYwNw.GEgl2a.OFF4ef8cRWaRVqYzY5xa9vgppRbYHdF7_aPsoE')
