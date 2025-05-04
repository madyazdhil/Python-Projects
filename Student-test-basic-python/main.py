
from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'mine'


# -------------------------------------------------
# Questions
# -------------------------------------------------
data_types_questions = [
    "Create a variable called 'item_name' and store a string representing a product name.",
    "Create a variable called 'quantity' and store an integer representing the number of items in stock.",
    "Create a variable called 'price' and store a floating-point number representing the price of an item.",
    "Create a variable called 'is_available' and store a boolean value indicating if the item is in stock.",
    "Write a line of code that prints the data type of the 'price' variable.",
]

variable_questions = [
    "Create a variable called 'fullname' and store your full name in it.",
    "Create two variables, 'num1' with the value 10 and 'num2' with the value 5. Then, create a new variable 'sum_result' that stores their sum.",
    "Create a variable called 'message' with the string 'Hello'. Then, create another variable called 'recipient' with a name. Concatenate these two variables and store the result in a new variable called 'greeting_message'.",
    "Create a variable 'counter' and initialize it to 0. ",
    "Write two different ways to increment the value of 'counter' by 1.",
    "You have two variables, 'a' with the value 5 and 'b' with the value 10. Write code to swap the values of 'a' and 'b' using a temporary variable.",
]

input_output_questions = [
    "Write code that prompts the user to enter their name and then prints a greeting message including their name.",
    "Write code that asks the user to enter two numbers and then prints their product.",
    "Write code that prompts the user for their favorite color and favorite food, and then prints a sentence using this information.",
    "Ask the user for their age and convert the input to an integer. Then, print a message indicating their age next year.",
    "Write code that asks the user to enter a value and then prints both the entered value and its data type.",
]

function_questions = [
    "Define a function called 'greet' that takes one argument (a name) and prints a greeting message.",
    "Define a function called 'add_numbers' that takes two numbers as arguments and returns their sum.",
    "Define a function called 'is_even' that takes an integer as an argument and returns True if it's even, and False otherwise.",
    "Write a function called 'calculate_area' that takes the length and width of a rectangle as arguments and returns its area.",
    "Define a function called 'reverse_string' that takes a string as an argument and returns its reversed version.",
]

conditionals_questions = [
    "Write code that asks the user for a number and prints 'Positive' if the number is greater than 0, 'Negative' if it's less than 0, and 'Zero' if it's 0.",
    "Write code that asks the user for their age. If they are 18 or older, print 'You are eligible to vote.' Otherwise, print 'You are not yet eligible to vote.'",
    "Write code that asks the user for a score. Based on the score, print a grade (e.g., A, B, C). You can define your own grading scale.",
    "Write code that asks the user for a username and password. Check if the entered username is 'admin' and the password is 'secret'. If both are correct, print 'Login successful'. Otherwise, print 'Login failed'.",
    "Write code that asks the user to enter two numbers. Determine and print the larger of the two numbers (or if they are equal).",
]

random_module_questions = [
    "Write code that simulates rolling a six-sided die and prints the result.",
    "Write code that simulates flipping a coin and prints either 'Heads' or 'Tails'.",
    "Write code that generates a random integer between 1 and 10 (inclusive) and prints it.",
    "Write code that chooses a random element from a list of colors: ['red', 'green', 'blue', 'yellow', 'purple'] and prints the chosen color.",
    "Write code that generates a random floating-point number between 0 and 1 and then multiplies it by 10 to get a random float between 0 and 10.",
]

looping_questions = [
    "Write a `for` loop that prints the numbers from 1 to 5.",
    "Write a `while` loop that asks the user to enter numbers and keeps printing them until the user enters 0.",
    "Create a list of fruits: ['apple', 'banana', 'cherry']. Use a `for` loop to print each fruit in the list.",
    "Write a `for` loop that iterates through the numbers from 1 to 10 and prints only the even numbers.",
    "Write a `while` loop that counts down from 10 to 1 and prints each number.",
]

array_questions = [
    "Create a list called 'numbers' with the values [1, 2, 3, 4, 5]. Print the element at index 2.",
    "Create a list of student names. Use a loop to print each name in the list.",
    "Create a list of test scores. Write code to calculate and print the average score.",
    "Create a list of numbers. Write code to find and print the largest number in the list.",
    "Create an empty list called 'even_numbers'. Use a loop to iterate through numbers from 1 to 10. If a number is even, append it to the 'even_numbers' list. Finally, print the list.",
]

#-------------------------------------------------
#ANSWER
# -------------------------------------------------

data_types_answers = [
    "`item_name = \"Product X\"`",
    "`quantity = 100`",
    "`price = 25.99`",
    "`is_available = True`",
    "`print(type(price))`",
]

variable_answers = [
    "`fullname = \"Your Name\"`",
    "`num1 = 10\nnum2 = 5\nsum_result = num1 + num2`",
    "`message = \"Hello\"\nrecipient = \"User\"\ngreeting_message = message + \", \" + recipient`",
    "`counter = 0`",
    "`counter = counter + 1\ncounter += 1`",
    "`a = 5\nb = 10\ntemp = a\na = b\nb = temp`",
]

input_output_answers = [
    "`name = input(\"Enter your name: \")\nprint(f\"Hello, {name}!\")`",
    "`num1_str = input(\"Enter the first number: \")\nnum2_str = input(\"Enter the second number: \")\nnum1 = float(num1_str)\nnum2 = float(num2_str)\nproduct = num1 * num2\nprint(f\"The product is: {product}\")`",
    "`favorite_color = input(\"What is your favorite color? \")\nfavorite_food = input(\"What is your favorite food? \")\nprint(f\"Your favorite color is {favorite_color} and your favorite food is {favorite_food}.\")`",
    "`age_str = input(\"Enter your age: \")\nage = int(age_str)\nnext_year_age = age + 1\nprint(f\"Next year you will be {next_year_age} years old.\")`",
    "`value = input(\"Enter a value: \")\nprint(f\"You entered: {value}\")\nprint(f\"The data type is: {type(value)}\")`",
]

function_answers = [
    """```python
def greet(name):
    print(f"Hello, {name}!")
```""",
    """```python
def add_numbers(num1, num2):
    return num1 + num2
```""",
    """```python
def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False
```""",
    """```python
def calculate_area(length, width):
    return length * width
```""",
    """```python
def reverse_string(text):
    return text[::-1]
```""",
]

conditionals_answers = [
    """```python
number_str = input("Enter a number: ")
number = int(number_str)
if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")
```""",
    """```python
age_str = input("Enter your age: ")
age = int(age_str)
if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are not yet eligible to vote.")
```""",
    """```python
score_str = input("Enter your score: ")
score = int(score_str)
if 90 <= score <= 100:
    grade = "A"
elif 80 <= score < 90:
    grade = "B"
elif 70 <= score < 80:
    grade = "C"
elif 60 <= score < 70:
    grade = "D"
else:
    grade = "F"
print(f"Your grade is: {grade}")
```""",
    """```python
username = input("Enter your username: ")
password = input("Enter your password: ")
if username == "admin" and password == "secret":
    print("Login successful")
else:
    print("Login failed")
```""",
    """```python
num1_str = input("Enter the first number: ")
num2_str = input("Enter the second number: ")
num1 = float(num1_str)
num2 = float(num2_str)
if num1 > num2:
    print(f"{num1} is larger than {num2}")
elif num2 > num1:
    print(f"{num2} is larger than {num1}")
else:
    print("The numbers are equal")
```""",
]

random_module_answers = [
    """```python
import random
dice_roll = random.randint(1, 6)
print(dice_roll)
```""",
    """```python
import random
coin_flip = random.choice(["Heads", "Tails"])
print(coin_flip)
```""",
    """```python
import random
random_int = random.randint(1, 10)
print(random_int)
```""",
    """```python
import random
colors = ['red', 'green', 'blue', 'yellow', 'purple']
chosen_color = random.choice(colors)
print(chosen_color)
```""",
    """```python
import random
random_float = random.random()
scaled_float = random_float * 10
print(scaled_float)
```""",
]

looping_answers = [
    """```python
for i in range(1, 6):
    print(i)
```""",
    """```python
while True:
    num_str = input("Enter a number (0 to stop): ")
    num = int(num_str)
    if num == 0:
        break
    print(num)
```""",
    """```python
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(fruit)
```""",
    """```python
for number in range(1, 11):
    if number % 2 == 0:
        print(number)
```""",
    """```python
count = 10
while count >= 1:
    print(count)
    count -= 1
```""",
]

array_answers = [
    "`numbers = [1, 2, 3, 4, 5]\nprint(numbers[2])`",
    """```python
student_names = ["Alice", "Bob", "Charlie"]
for name in student_names:
    print(name)
```""",
    """```python
test_scores = [80, 90, 75, 85, 95]
average_score = sum(test_scores) / len(test_scores)
print(f"Average score: {average_score}")
```""",
    """```python
numbers = [15, 3, 22, 8, 19]
largest_number = max(numbers)
print(f"Largest number: {largest_number}")
```""",
    """```python
even_numbers = []
for i in range(1, 11):
    if i % 2 == 0:
        even_numbers.append(i)
print(even_numbers)
```""",
]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/start_quiz", methods=['POST'])
def start_quiz():
    selected_topics = request.form.getlist('topics')
    session['selected_topics'] = selected_topics
    session['current_topic_index'] = 0
    session['current_question_index'] = 0
    session['questions'] = {}
    session['score'] = 0


    for topic in selected_topics:
        questions = globals().get(f"{topic}_questions", [])
        answers = globals().get(f"{topic}_answers", [])
        if questions and answers:
            # Get 2 random unique indices
            indices = random.sample(range(len(questions)), min(2, len(questions)))
            session['questions'][topic] = [
                {'question': questions[i], 'answer': answers[i]}
                for i in indices
            ]

    return redirect(url_for('show_question'))


@app.route("/quiz")
def show_question():
    selected_topics = session.get('selected_topics', [])
    if not selected_topics:
        return redirect(url_for('home'))

    current_topic_index = session.get('current_topic_index', 0)
    current_question_index = session.get('current_question_index', 0)
    current_topic = selected_topics[current_topic_index]

    # Get current question data
    questions_for_topic = session['questions'].get(current_topic, [])
    if current_question_index >= len(questions_for_topic):
        session['current_topic_index'] += 1
        session['current_question_index'] = 0
        return redirect(url_for('show_question'))

    current_question = questions_for_topic[current_question_index]


    topic_display_names = {
        'data_types': 'Data Types',
        'variable': 'Variables',
        'input_output': 'Input & Output',
        'function': 'Functions',
        'conditionals': 'Conditionals',
        'random_module': 'Random Module',
        'looping': 'Looping',
        'array': 'Arrays'
    }

    # Calculate progress
    total_questions = sum(len(q) for q in session['questions'].values())
    answered_questions = (current_topic_index * 2) + current_question_index

    return render_template("quiz.html",
                         question=current_question['question'],
                         current_topic=topic_display_names.get(current_topic, current_topic),
                         selected_topics=[topic_display_names.get(t, t) for t in selected_topics],
                         current_topic_index=current_topic_index,
                         current_question_index=current_question_index,
                         total_questions=total_questions,
                         answered_questions=answered_questions)


@app.route("/check_answer", methods=['POST'])
def check_answer():
    user_answer = request.form.get('answer', '').strip()
    selected_topics = session.get('selected_topics', [])
    current_topic_index = session.get('current_topic_index', 0)
    current_question_index = session.get('current_question_index', 0)

    if not selected_topics or current_topic_index >= len(selected_topics):
        return {'status': 'error', 'message': 'Session expired. Please start again.'}, 400

    current_topic = selected_topics[current_topic_index]
    questions_for_topic = session['questions'].get(current_topic, [])
    current_question = questions_for_topic[current_question_index]['question']

    if current_question_index >= len(questions_for_topic):
        return {'status': 'error', 'message': 'No more questions in this topic.'}, 400

    # Check answer based on question type
    is_correct = False
    clean_user = user_answer.replace('`', '').replace('```python', '').replace('```', '').strip()

    # Data Types and Variables
    if "Create a variable called" in current_question or "Create two variables" in current_question:
        # Get all variable names from the question
        var_names = [part.split("'")[1] for part in current_question.split("'") if "'" in part]

        # Check if all required variables are present
        vars_present = all(
            any(var_part in clean_user for var_part in [f"{var} =", f"{var}="])
            for var in var_names
        )

        # Check for valid value assignments
        valid_value_checks = [
            '"' in clean_user or "'" in clean_user,  # strings
            "True" in clean_user or "False" in clean_user,  # booleans
            any(c.isdigit() for c in clean_user)  # numbers
        ]
        has_valid_assignments = any(valid_value_checks)

        is_correct = vars_present and has_valid_assignments

    # Arrays/Lists
    elif "list" in current_question.lower() or "array" in current_question.lower():
        if '[' in clean_user and ']' in clean_user and ',' in clean_user:
            is_correct = True

    # Functions
    elif "Define a function" in current_question:
        func_name = current_question.split("'")[1]  # Get function name from question
        if f"def {func_name}(" in clean_user and '):' in clean_user:
            is_correct = True

    # Conditionals
    elif "if" in current_question.lower():
        if 'if ' in clean_user and ':' in clean_user:
            is_correct = True

    # Loops
    elif "loop" in current_question.lower():
        if ('for ' in clean_user and 'in ' in clean_user and ':' in clean_user) or \
                ('while ' in clean_user and ':' in clean_user):
            is_correct = True

    # Input/Output - More flexible checking
    elif "input" in current_question.lower() or "print" in current_question.lower():
        # For product calculation question
        if "product" in current_question.lower():
            # Check for two input statements and a multiplication
            input_count = clean_user.lower().count('input(')
            multiply_ops = clean_user.count('*') or 'product' in clean_user.lower()
            print_count = clean_user.lower().count('print(')

            if input_count >= 2 and multiply_ops and print_count >= 1:
                is_correct = True
        else:
            # General input/output check
            if 'input(' in clean_user and 'print(' in clean_user:
                is_correct = True

    # Random Module
    elif "random" in current_question.lower():
        if 'import random' in clean_user and ('random.' in clean_user):
            is_correct = True

    # If none of the specific checks matched, do a general check
    if not is_correct:
        # Check if the answer contains key elements from the question
        key_elements = [word for word in current_question.split() if word not in ['a', 'an', 'the', 'is', 'and', 'or']]
        matched_elements = sum(1 for elem in key_elements if elem.lower() in clean_user.lower())
        if matched_elements / len(key_elements) > 0.6:  # 60% match
            is_correct = True

    if is_correct:
        session['score'] += 1
        return {'status': 'correct', 'message': 'Good Job! Your did paid attention huh?!.'}
    else:
        return {'status': 'incorrect',
                'message': 'Wrong!!\n. Please recheck and remember the syntax rules.'}


@app.route("/next_question")
def next_question():
    selected_topics = session.get('selected_topics', [])
    if not selected_topics:
        return redirect(url_for('home'))

    current_topic_index = session.get('current_topic_index', 0)
    current_question_index = session.get('current_question_index', 0)

    # Check if we've finished all questions in current topic
    questions_in_current_topic = len(session['questions'][selected_topics[current_topic_index]])
    if current_question_index >= questions_in_current_topic - 1:
        # Move to next topic
        session['current_topic_index'] += 1
        session['current_question_index'] = 0
    else:
        # Move to next question in current topic
        session['current_question_index'] += 1

    # Check if we've finished all topics
    if session['current_topic_index'] >= len(selected_topics):
        return redirect(url_for('quiz_complete'))

    return redirect(url_for('show_question'))

@app.route("/quiz_complete")
def quiz_complete():
    score = session.get('score', 0)
    total_questions = sum(len(q) for q in session.get('questions', {}).values())
    return render_template("complete.html", score=score, total_questions=total_questions)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)