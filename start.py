import os
import csv
from openai import OpenAI
from dotenv import load_dotenv

model = "gpt-3.5-turbo"
allergies = "mushrooms"
dislike = "onion"
load_dotenv()


client = OpenAI(
    # This is the default and can be omitted
    organization="org-CRPjgX2sXjMrNTB00bMNzjN5",
    api_key=os.getenv("OPENAI_KEY")
)


def init_gpt():
    data = read_csv()
    prompt1 = "You are a planner that will generate a meal plan and ingredients for a family. The data im providing is in the csv format and consists of meals. Base all following questions on this data. Your task will be to generate a meal plan based on the data provided and the family specifc information that will be provided later. It's ok to re use some of the previous meals but try to change at least 2 or 3 of the total amount of meals. Dont provide meals until the user provides the family information."
    # print(prompt1, "\n")
    content = f"{prompt1} The data is: {data}"
    client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": content}],
    )


def read_csv():
    data = ""
    with open('meals.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data += ", ".join(row)

    return data


def send_user_message(message):
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}],
    )
    return completion


def generate_plan():
    adults_amount = 2
    children_amount = 1
    lunch_amount = 7
    dinner_amount = 7
    keyword = "adventurous"
    wanted_meals = "pasta"
    skipped_meals = "pork"

    part1 = f"My family consists of {adults_amount} adults which require 2500 calories per day and {
        children_amount} children which require 1500 calories per day."
    part2 = "The meal plan should include a calorie count for adults and children per meal."
    part3 = f"Under no circumstance should any of the meals should include {allergies} or {
        dislike}. These are banned ingredients. In the event that a recipe from the data provided contains the banned ingredients, find another recipe."
    part4 = f"Generate {lunch_amount} lunch meals and {
        dinner_amount} dinner meals."
    part5 = f"30% of the meals should be new and {keyword} meals."
    part6 = f"This week none of the meals should include {skipped_meals}."
    part7 = f"This week I want at least one meal that includes {wanted_meals}."
    message = f"{part1} {part2} {part3} {part4} {part5} {part6} {part7}"
    # print(message, "\n")
    completion = send_user_message(message)
    chat_resonse = completion.choices[0].message.content
    chat_resonse = chat_resonse.replace(allergies, "")
    chat_resonse = chat_resonse.replace(dislike, "")
    print(chat_resonse, "\n")
    generate_ingredient_list(chat_resonse)


def generate_ingredient_list(meals):
    part1 = "The ingredients must be based on the meal plan for lunch and dinner."
    part2 = "The list should be something that a person can take to the grocery store."
    part3 = "Measurements should be in metric not imperial. The family should be able to use all the ingredients to make the meals."
    part4 = "Take into account the caloric requirements for adults and children."
    part5 = "The products must include the amounts. Good examples of this are as follows: 3 peppers, 500g of chicken breast, one jar of sauce, one can of diced tomatoes. Every ingredient should have an amount. Vegetables should be in units so 4 lemons and not pack."
    part6 = f"Make sure you provide all the necessary ingredients for a meal. Greek salad requires tomatoes, lettuce, onion, cucumber, feta cheese, olive oil. Make sure not to include {
        allergies} or {dislike} in any capacity."
    part7 = "Find alternative ingredients for the previously mentioned banned ingredients. All the ingredients should be specific. Roasted vegetables is not specific enough for an ingredient."
    part8 = f"None of the ingredients should be {allergies} or {
        dislike}. An example is to not include red onions or onion powder if the banned ingredient is an onion. Differentiate the ingredients by meal. Think step by step in order to include all specifications."
    part9 = f"Generate a list of ingredients based on the list of lunch and dinner meals while taking all previous rules into account."
    part99 = f"The meals are: {meals}"
    message = f"{part1} {part2} {part3} {
        part4} {part5} {part6} {part7} {part8} {part9} {part99}"
    # print(f"{part1} {part2} {part3} {part4} {
    #       part5} {part6} {part7} {part8} {part9}", "\n")
    completion = send_user_message(message)
    chat_resonse = completion.choices[0].message.content
    # chat_resonse = chat_resonse.replace(allergies, "")
    # chat_resonse = chat_resonse.replace(dislike, "")
    print(f"{chat_resonse}")


init_gpt()
generate_plan()
