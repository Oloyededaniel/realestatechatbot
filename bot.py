import discord
from discord.ext import commands
import json
import random
import nltk
import asyncio


# Download necessary NLTK resources
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

# Function to check if message contains keywords
def contains_keywords(message, keywords):
    #Tokenize the message
    message_tokens = word_tokenize(message.lower())
    #Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in message_tokens if word.isalnum() and word not in stop_words]
    # Check if any keyword is present in the filtered tokens
    return any(keyword in filtered_tokens for keyword in keywords)

# Define a list of keywords for each intent
GREETINGS = ["hello", "hi", "yo", "hey", "greetings", "sup", "what's up"]
PROPERTY_REQUESTS = ["find" ,"property", "show","me" ,"some", "search", "list", "properties", "looking","searching",
"available", "listings", "availability"]
COMPANY_INFO_KEYWORDS = ["information", "about", "history", "company", "know", "more","info"]
OFFICE_HOURS_KEYWORDS = ["office", "hours","Company's","store","opened", "open"]
PAYMENT_INFO_KEYWORDS = ["money", "cash", "pay","payment"]
SCHEDULE_APPOINTMENT_KEYWORDS = ["schedule", "book", "appointment","routines","appointments"]
User_feedback = ["feedback","rate","responses","suggestions","ratings"]
ASSIST = ["help","assistance","assist","need","what","can","i","you","do","about","chatbot","radarbot"]
THANKS = ["thanks","thank","you","hat","tip","gratitude","recognition"]
PROPERTY_TAX = ["property","tax","properties","taxes","rates","rate","provinces","Provincial"]
LEGAL = ["legal","court","agreement","contract","aspect","requirements","contracts","requirement","agreements"]

# Define an event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Event handler for processing user messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for different intents based on keywords in the message
    if any(keyword in message.content.lower() for keyword in GREETINGS):
        await greet(message.channel)
        await message.channel.send("I am RadarBot, the Radar Estate Chatbot.")
        await message.channel.send("I can help you find properties based on your preferences.")
        await message.channel.send("To chat with the chatbot type in prompts like:(Find me a Property,Company Info, "
                                   "Office Hours, Legal aspects(Contracts), Rates(Provincial Rates/Tax), "
                                   "Ratings(Feedback), Schedule an Appointment, Assist me, How do i make Payments(For "
                                   "Payments))")

    elif contains_keywords(message.content, User_feedback):
        await feedback(message)

    elif contains_keywords(message.content, PROPERTY_REQUESTS):
        await find_property(message.channel, message.author)

    elif contains_keywords(message.content, PROPERTY_TAX):
        await calculate_property_tax(message.channel, message.author)

    elif contains_keywords(message.content, LEGAL):
        await legal_aspects(message.channel, message.author)

    elif contains_keywords(message.content, COMPANY_INFO_KEYWORDS):
        await company_info(message.channel)

    elif contains_keywords(message.content, OFFICE_HOURS_KEYWORDS):
        await office_hours(message.channel)

    elif contains_keywords(message.content, PAYMENT_INFO_KEYWORDS):
        await payment_info(message.channel)

    elif contains_keywords(message.content, SCHEDULE_APPOINTMENT_KEYWORDS):
        await schedule_appointment(message.channel)

    elif contains_keywords(message.content, ASSIST):
        await assist(message.channel)

    elif contains_keywords(message.content, THANKS):
        await thanks(message.channel)

    else:
        await bot.process_commands(message)


# Define a command to greet users
@bot.command()
async def greet(ctx):
    greetings = ['Hi!', 'Hello!', 'Hey there!',"Good day sir/ma","Greetings","Dear sir/ma","Salutations"]
    await ctx.send(random.choice(greetings))

# Define a command to assist users
@bot.command()
async def assist(ctx):
    await ctx.send("I'm here to assist you in finding properties based on your preferences. "
                   "You can ask me to find properties, provide company information, office hours, payment "
                   "information,Property search"
                   "or schedule an appointment. Feel free to explore the available commands!")

# Define a command for user's thank you message
@bot.command()
async def thanks(ctx):
    await ctx.send("You're welcome! If you have any further questions, feel free to ask or send an email to "
                   "***radarestate@gmail.com***.")

# Define a command to provide company information
@bot.command()
async def company_info(ctx):
    await ctx.send("Our company, Radar Estate, specializes in providing high-quality real estate services. We offer a "
                   "wide range of properties for sale and rent across various locations. If you have any specific "
                   "questions, feel free to ask!")

# Define a command to provide office hours
@bot.command()
async def office_hours(ctx):
    await ctx.send("Our office hours are from Monday to Friday, 9:00 AM to 5:00 PM. We are closed on weekends and "
                   "public holidays. If you need assistance outside of these hours, you can reach out to us via email "
                   "at ***radarestate@gmail.com***.")

# Define a command to provide payment information
@bot.command()
async def payment_info(ctx):
    await ctx.send("To make a payment for a property, you can choose from the following methods: online payment, "
                   "bank transfer, or in-person payment at our office. Once you've selected a property and finalized "
                   "the details, our team will provide you with the necessary payment instructions.")

# Define a command to schedule an appointment
@bot.command()
async def schedule_appointment(ctx):
    await ctx.send("To schedule an appointment to view properties, please contact our team via email at "
                   "***radarestate@gmail.com*** or give us a call during our office hours. We'll be happy to arrange a "
                   "convenient time for you to visit and checkout the houses.")

# Define an event handler for when a command is not found
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't understand that command.")

async def legal_aspects(ctx, author):
    try:
        await ctx.send("What specific legal aspect of real estate transactions would you like to know about? "
                       "For example, contracts or agreements")

        # Wait for user's input
        legal_query_message = await bot.wait_for('message', check=lambda message: message.author == author)
        legal_query = legal_query_message.content.lower()

        # Define responses for different legal aspects
        if "contract" in legal_query:
            await ctx.send("In real estate transactions, contracts play a crucial role. "
                           "They outline the terms and conditions agreed upon by the parties involved, "
                           "including the purchase price, property details, contingencies, and closing date. "
                           "It's essential to review contracts carefully and consider seeking legal advice "
                           "to ensure all aspects are understood before signing.")

        elif "agreement" in legal_query:
            await ctx.send("Real estate agreements refer to the mutual understanding between parties involved "
                           "in a transaction. These agreements may include purchase agreements, lease agreements, "
                           "or rental agreements. They detail the rights and responsibilities of each party, "
                           "such as payment terms, property usage, and duration of the agreement.")

        elif "legal requirements" in legal_query:
            await ctx.send("In real estate transactions, several key legal requirements must be addressed to ensure a "
                           "smooth and legally compliant process. These include verifying property titles to confirm "
                           "clear ownership, disclosing any known defects or issues with the property, and drafting a "
                           "comprehensive purchase agreement that outlines the terms and conditions of the sale. "
                           "Additionally, compliance with zoning regulations, financing and mortgage documentation, "
                           "and addressing tax obligations and liens are crucial aspects that require attention. "
                           "Legal representation can provide valuable guidance throughout the transaction process, "
                           "helping buyers and sellers navigate complex legal requirements and protect their "
                           "interests.")

        else:
            # Prompt the user to type in the right input
            await ctx.send("I'm sorry, I couldn't understand your query regarding legal aspects of real estate "
                           "transactions. Please specify whether you're referring to contracts, agreements, "
                           "or any other legal aspect.")
            # Wait for the user to type in the right input
            await legal_aspects(ctx, author)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Function to handle finding properties based on user input
async def find_property(ctx, author):
    try:
        await ctx.send("May I know your name?")
        name_message = await bot.wait_for('message', check=lambda message: message.author == author)
        name = name_message.content
        await ctx.send(f"\nHello, {name}! How can I assist you?")

        # Gather property search criteria
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
                        "\nIf you have any further questions or need assistance, feel free to reach out to us at "
                        "***radarestate@gmail.com***. We're here to help!"
                    )
                    await ctx.send("\nThank you for using the Radar Estate Chatbot!")
                    return
                else:
                    await ctx.send("Invalid response. Please enter 'yes' or 'no'.")


           #await feedback(ctx)


    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Define property tax rates for different provinces in Canada
PROPERTY_TAX_RATES = {
    "ontario": 0.0121,
    "new brunswick": 0.01785,   
    "alberta": 0.0066,
    "british columbia": 0.0028,
    "saskatchewan" : 0.0129,
    "quebec" : 0.0059,
    "newfoundland and labrador" : 0.0091,
    "nova scotia" : 0.0112,
    "manitoba" : 0.0264,

}

# Function to calculate property tax
async def calculate_property_tax(ctx, author):
    try:
        await ctx.send("Please enter the province (e.g., Ontario) where the property is located:")
        province_message = await bot.wait_for('message', check=lambda message: message.author == author)
        province = province_message.content.lower()

        if province not in PROPERTY_TAX_RATES:
            await ctx.send("Sorry, property tax rate for this province is not available.")
            await calculate_property_tax(ctx, author)
            return

        await ctx.send("Please enter the property value:")
        property_value_message = await bot.wait_for('message', check=lambda message: message.author == author)
        property_value_str = property_value_message.content

        try:
            property_value = float(property_value_str.replace(',', ''))
            if property_value <= 0:
                await ctx.send("Please enter a valid property value (a positive number).")
                # Prompt the user to enter valid input
                await calculate_property_tax(ctx, author)
                return
        except ValueError:
            await ctx.send("Please enter a valid property value (a number).")
            # Prompt the user to enter valid input
            await calculate_property_tax(ctx, author)
            return

        tax_rate = PROPERTY_TAX_RATES[province]
        property_tax = property_value * tax_rate

        await ctx.send(f"The property tax for a property valued at ${property_value:,.2f} in {province.title()} "
                       f"is ${property_tax:,.2f} based on a {tax_rate*100}% tax rate.")

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Function to handle user feedback
async def feedback(message):
    # Send a prompt for feedback or rating
    await message.channel.send("Please provide your feedback and rate the usefulness of the bot's responses on a scale of 1 to 10.")

    # Wait for user feedback
    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    try:
        feedback_message = await bot.wait_for('message', check=check, timeout=150)  # Wait for 150 seconds
        feedback_text = feedback_message.content

        # Check if the user's response is a number from 1 to 10
        if feedback_text.isdigit() and 1 <= int(feedback_text) <= 10:
            await message.channel.send("Thank you for your rating!")
        else:
            await message.channel.send("Invalid response, Please give your ratings from 1 to 10.")
            # Prompt the user to enter valid input
            await feedback(message)
    except asyncio.TimeoutError:
        await message.channel.send("Sorry, you took too long to respond. Feedback submission canceled.")

# Run the bot with your Discord bot token
bot.run('MTIwODUxNzcwNDMzMjM1MzYwNw.GEgl2a.OFF4ef8cRWaRVqYzY5xa9vgppRbYHdF7_aPsoE')
