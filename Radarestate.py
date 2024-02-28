import json
import random
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocess_input(input_text):
    tokens = word_tokenize(input_text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    return filtered_tokens

def search_properties(query, property_data):
    results = []
    for property_info in property_data['property']:
        property_features = property_info["type"] + " " + property_info["area"]
        if all(term.lower() in property_features.lower() for term in query):
            results.append(property_info)
    return results

def get_user_info():
    name = input("Please enter your name: ")
    budget = float(input("What is your budget? $").replace(',', ''))
    location = input("Where are you looking for properties? ")
    bedrooms = int(input("How many bedrooms do you need? "))
    bathrooms = int(input("How many bathrooms do you need? "))
    return name, budget, location, bedrooms, bathrooms

def greet():
    greetings = ['Hi!', 'Hello!', 'Hey there!']
    return random.choice(greetings)

def main():
    print(greet())
    print("I am RadarBot, the Radar Estate Chatbot.")
    print("I can help you find properties based on your preferences.")

    name = input("May I know your name? ")
    print(f"\nHello, {name}! Let's find the perfect property for you.")

    budget, location, bedrooms, bathrooms = None, None, None, None

    while not all((budget, location, bedrooms, bathrooms)):
        try:
            if not budget:
                budget = float(input("What is your budget? $").replace(',', ''))

            if not location:
                location = input("Where are you looking for properties? ")

            if not bedrooms:
                bedrooms = int(input("How many bedrooms do you need? "))

            if not bathrooms:
                bathrooms = int(input("How many bathrooms do you need? "))

        except ValueError:
            print("Please enter a valid input.")

    print("\nThank you for providing the details. Let's find properties within your criteria:")

    with open('data.json', 'r') as f:
        property_data = json.load(f)

    while True:
        user_input = input("Ask me about a property: ")
        if user_input.lower() == "quit":
            print("\nThank you for using the Radar Estate Chatbot!")
            break

        query = preprocess_input(user_input)

        search_results = search_properties(query, property_data)

        found_matching_properties = False
        count = 0
        for result in search_results:
            price = result["price"]
            if price <= budget and result["area"].lower() == location.lower() and result["beds"] >= bedrooms and result["baths"] >= bathrooms:
                found_matching_properties = True
                count += 1
                print(f"\nProperty {count}:")
                print("ID:",result["id"])
                print("Type:", result["type"])
                print("Location:", result["area"])
                print("Address:", result["address"])
                print("City:", result["city"])
                print("Price: ${:,.2f}".format(price))
                print("Bedrooms:", result["beds"])
                print("Bathrooms:", result["baths"])
                print("Floorspace:", result["floorspace"], "sq ft")
                print("Maintenance: ${:,.2f}".format(result["maintenance"]))
                print("Parking:", result["parking"],"vehicles")
                print("Construction:", ", ".join(result["construction"]))

        if not found_matching_properties:
            print("\nNo properties found matching your search.")

        choice = input("\nDo you have any other questions? (yes/no): ")
        if choice.lower() != "yes":
            print("\nIf you have any further questions or need assistance, feel free to reach out to us at "
                  "radarestate@gmail.com. We're here to help!")
            print("\nThank you for using the Radar Estate Chatbot!")
            break

if __name__ == '__main__':
    main()
