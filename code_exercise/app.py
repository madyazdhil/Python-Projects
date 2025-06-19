from flask import Flask, render_template, request, session, redirect, url_for
import requests
import json
import re
import os
from time import sleep
from requests.exceptions import HTTPError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

API_KEYS = [
    os.environ.get('API_KEY_1'),
    os.environ.get('API_KEY_2'),
    os.environ.get('API_KEY_3')
]
current_key_index = 0


def markdown_to_html(text):
    print(f"Input to markdown_to_html: {text}")
    text = text.replace('\\*\\*', '**').replace('\\*', '*').replace('\\`', '`')
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\d|\s)\*(.*?)\*(?!\d|\s)', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    text = text.replace('\n', '<br>')
    print(f"Output from markdown_to_html: {text}")
    return text

def call_api(user_input, max_retries=3, initial_delay=1):
    global current_key_index
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            headers = {
                "Authorization": f"Bearer {API_KEYS[current_key_index]}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.environ.get('REFERER_URL', 'http://your-site-url.com'),
                "X-Title": "Code Quest"
            }
            data = {
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "messages": [{"role": "user", "content": user_input}]
            }
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=10
            )
            response.raise_for_status()
            response_json = response.json()
            print("API Response:", response.text)
            if 'choices' not in response_json:
                print("Error: 'choices' key not found in API response")
                return {'error': 'Invalid API response: choices key missing'}
            return response_json
        except HTTPError as e:
            if e.response.status_code == 429:
                print(f"Rate limit hit with key {current_key_index + 1}, switching API key...")
                current_key_index = (current_key_index + 1) % len(API_KEYS)
                print(f"Retrying with new key {current_key_index + 1} in {delay} seconds...")
                sleep(delay)
                delay *= 2
                continue
            print(f"API Request failed: {str(e)}")
            return {'error': f'API Request failed: {str(e)}'}
        except requests.exceptions.RequestException as e:
            print(f"API Request failed: {str(e)}")
            return {'error': f'API Request failed: {str(e)}'}
        except ValueError as e:
            print(f"Invalid JSON response: {str(e)}")
            return {'error': f'Invalid JSON response: {str(e)}'}
    return {'error': 'Max retries reached due to rate limiting'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
    language = request.form.get('language')
    concepts = request.form.getlist('concept')
    hero_name = request.form.get('heroName')
    challenge_count = int(request.form.get('challengeCount', 1))
    difficulty = request.form.get('difficulty')
    custom_challenge = request.form.get('customChallenge', '')

    topics = ', '.join(concepts)
    if custom_challenge:
        topics += f", {custom_challenge}"
    user_input = f"I am a student age 12 years old learning the basics of {language} programming language and I just covered these topics: {topics}. I want you to give me the first of {challenge_count} exercises based on the above topics to strengthen my understanding. Please respond with one question in this format: <h4>Below will be the questions and instructions</h4><p>Instructions</p><p>[Instructions here]</p><p>Output expected</p><p>[Output example]</p>."
    response = call_api(user_input)

    if 'error' in response:
        error_message = f"Failed to fetch question: {response['error']}"
        if 'rate limit' in response['error'].lower():
            error_message = "We're hitting the API rate limit. Please wait a moment and try again."
        print(f"Error in /home: {error_message}")
        return render_template('index.html', error=error_message)

    question_raw = response['choices'][0]['message']['content']
    session['hero_name'] = hero_name
    session['language'] = language
    session['attempts_left'] = 3
    session['question_number'] = 1
    session['total_questions'] = challenge_count
    session['original_question'] = question_raw
    session['current_question'] = markdown_to_html(question_raw)
    session['concepts'] = concepts
    session['custom_challenge'] = custom_challenge
    session['correct_answers'] = 0
    session['user_answers'] = []

    return render_template('QuestionsAnswer.html',
                           question=session['current_question'],
                           hero_name=hero_name,
                           language=language,
                           attempts_left=session['attempts_left'],
                           question_number=session['question_number'],
                           total_questions=session['total_questions'],
                           original_question=question_raw,
                           feedback='',
                           show_next_button=False)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_code = request.form.get('user_code')
    hero_name = session.get('hero_name', 'Student')
    language = session.get('language', 'Python')
    attempts_left = int(session.get('attempts_left', 3))
    question_number = int(session.get('question_number', 1))
    total_questions = int(session.get('total_questions', 1))
    original_question = session.get('original_question', '')
    correct_answers = session.get('correct_answers', 0)
    user_answers = session.get('user_answers', [])
    feedback = ''
    show_next_button = False

    print(f"Processing answer: user_code='{user_code}', attempts_left={attempts_left}, question_number={question_number}, correct_answers={correct_answers}")

    if attempts_left > 0 or 'strawberry ice cream' in user_code.lower():
        user_input = f"""
        The student's answer is: {user_code}. Check if it is correct for the previous question. If incorrect, provide feedback on where to improve, using newlines for separation instead of HTML tags. Do not include the instructions or expected output in the feedback. Do not provide the next question or correct code unless the answer is correct, 'strawberry ice cream' is included, or after 3 incorrect attempts. Use this format:

        ===QUESTION===
        <h4>Below will be the questions and instructions</h4>
        <p>Instructions</p>
        <p>{original_question}</p>
        ===FEEDBACK===
        [Provide feedback here as plain text with newlines for separation]
        ===END_FEEDBACK===
        <p>Output expected</p>
        <p>[Output example]</p>

        If the answer is fully correct with no feedback needed, return: 'this solution is correct'.
        If the answer is correct but has minor feedback (e.g., formatting improvements, variable naming suggestions), return: 'correct with feedback' followed by the feedback text.
        If the answer is incorrect, return feedback explaining the errors and how to fix them.
        """
        response = call_api(user_input)

        if 'error' in response:
            feedback = f"API Error: {response['error']}"
            is_correct = False
            print(f"API error: {feedback}")
        elif 'choices' in response:
            feedback_content = response['choices'][0]['message']['content']
            print(f"Feedback content: {feedback_content}")
            if feedback_content.strip() == 'this solution is correct':
                is_correct = True
                feedback = ''
                correct_answers += 1
                user_answers.append({'question': original_question, 'answer': user_code, 'correct': True})
                session['correct_answers'] = correct_answers
                session['user_answers'] = user_answers
                print(f"Answer is correct (exact match), correct_answers={correct_answers}")
            elif '===FEEDBACK===' in feedback_content and '===END_FEEDBACK===' in feedback_content:
                try:
                    feedback_section = feedback_content.split('===FEEDBACK===')[1].split('===END_FEEDBACK===')[0].strip()
                    if feedback_section == 'this solution is correct':
                        is_correct = True
                        feedback = ''
                        correct_answers += 1
                        user_answers.append({'question': original_question, 'answer': user_code, 'correct': True})
                        session['correct_answers'] = correct_answers
                        session['user_answers'] = user_answers
                        print(f"Answer is correct (feedback section), correct_answers={correct_answers}")
                    elif feedback_section.startswith('correct with feedback'):
                        is_correct = True
                        feedback_text = feedback_section.replace('correct with feedback', '').strip()
                        feedback = markdown_to_html(feedback_text)
                        correct_answers += 1
                        user_answers.append({'question': original_question, 'answer': user_code, 'correct': True})
                        session['correct_answers'] = correct_answers
                        session['user_answers'] = user_answers
                        show_next_button = True
                        print(f"Answer is correct with feedback, correct_answers={correct_answers}, feedback={feedback}")
                    elif feedback_section.lower().startswith('the code is correct') or 'is correct' in feedback_section.lower() or 'acceptable' in feedback_section.lower():
                        is_correct = True
                        feedback = markdown_to_html(feedback_section)
                        correct_answers += 1
                        user_answers.append({'question': original_question, 'answer': user_code, 'correct': True})
                        session['correct_answers'] = correct_answers
                        session['user_answers'] = user_answers
                        show_next_button = True
                        print(f"Answer is correct with feedback (detected explicit correctness), correct_answers={correct_answers}, feedback={feedback}")
                    else:
                        is_correct = False
                        feedback = markdown_to_html(feedback_section)
                        if attempts_left == 1:
                            user_answers.append({'question': original_question, 'answer': user_code, 'correct': False})
                            session['user_answers'] = user_answers
                        print(f"Feedback extracted: {feedback}")
                except IndexError as e:
                    feedback = 'Unable to process feedback due to malformed response. Please try again.'
                    is_correct = False
                    print(f"Feedback parsing error: {str(e)}")
            else:
                feedback = markdown_to_html(feedback_content)
                is_correct = False
                if attempts_left == 1:
                    user_answers.append({'question': original_question, 'answer': user_code, 'correct': False})
                    session['user_answers'] = user_answers
                print(f"Feedback (no markers): {feedback}")
        else:
            feedback = 'Invalid API response: No choices found.'
            is_correct = False
            if attempts_left == 1:
                user_answers.append({'question': original_question, 'answer': user_code, 'correct': False})
                session['user_answers'] = user_answers
            print("Invalid API response")

        if is_correct or 'strawberry ice cream' in user_code.lower():
            print("Advancing to next question or completing exercise")
            if question_number < total_questions and not show_next_button:
                user_input = f"I am a student age 12 years old learning the basics of {language} programming language and I just covered these topics: {', '.join(session['concepts'])}{', ' + session['custom_challenge'] if session['custom_challenge'] else ''}. I want you to give me the next exercise (question #{question_number + 1}) out of {total_questions} based on the above topics to strengthen my understanding. Please respond with one question in this format: <h4>Below will be the questions and instructions</h4><p>Instructions</p><p>[Instructions here]</p><p>Output expected</p><p>[Output example]</p>."
                response = call_api(user_input)
                if 'error' in response:
                    feedback = f"API Error for next question: {response['error']}"
                    print(f"Next question API error: {feedback}")
                    return render_template('QuestionsAnswer.html',
                                           question=session['current_question'],
                                           hero_name=hero_name,
                                           language=language,
                                           attempts_left=attempts_left,
                                           question_number=question_number,
                                           total_questions=total_questions,
                                           original_question=original_question,
                                           feedback=feedback,
                                           show_next_button=False)
                else:
                    next_question = response['choices'][0]['message']['content']
                    session['current_question'] = markdown_to_html(next_question)
                    session['original_question'] = next_question
                    session['question_number'] = question_number + 1
                    session['attempts_left'] = 3
                    feedback = ''
                    print(f"New question loaded: question_number={question_number + 1}")
                    return render_template('QuestionsAnswer.html',
                                           question=session['current_question'],
                                           hero_name=hero_name,
                                           language=language,
                                           attempts_left=session['attempts_left'],
                                           question_number=session['question_number'],
                                           total_questions=session['total_questions'],
                                           original_question=next_question,
                                           feedback=feedback,
                                           show_next_button=False)
            else:
                if is_correct and not show_next_button:
                    print("Last question correct, redirecting to result")
                    return redirect(url_for('result'))
                else:
                    session['finished'] = False
                    if not is_correct:
                        attempts_left -= 1
                        session['attempts_left'] = attempts_left
                        print(f"Incorrect answer, attempts_left={attempts_left}")
                        if attempts_left == 0:
                            feedback = markdown_to_html(feedback + '\nNo attempts left for this question.')
                            print("No attempts left, feedback updated")
        else:
            attempts_left -= 1
            session['attempts_left'] = attempts_left
            print(f"Incorrect answer, attempts_left={attempts_left}")
            if attempts_left == 0:
                feedback = markdown_to_html(feedback + '\nNo attempts left for this question.')
                print("No attempts left, feedback updated")

    return render_template('QuestionsAnswer.html',
                           question=session['current_question'],
                           hero_name=hero_name,
                           language=language,
                           attempts_left=session['attempts_left'],
                           question_number=session['question_number'],
                           total_questions=total_questions,
                           original_question=session['original_question'],
                           feedback=feedback,
                           show_next_button=show_next_button)

@app.route('/result', methods=['GET'])
def result():
    hero_name = session.get('hero_name', 'Student')
    correct_answers = session.get('correct_answers', 0)
    total_questions = session.get('total_questions', 1)
    concepts = session.get('concepts', [])
    custom_challenge = session.get('custom_challenge', '')
    user_answers = session.get('user_answers', [])

    topics = ', '.join(concepts)
    if custom_challenge:
        topics += f", {custom_challenge}"
    user_input = f"""
    The student completed {total_questions} coding exercises in {session.get('language', 'Python')}, covering these topics: {topics}.
    Here are their answers:
    {json.dumps(user_answers, indent=2)}
    Provide a summary feedback for the student, highlighting:
    - What they did well (e.g., correct solutions, use of concepts).
    - Areas for improvement (e.g., common mistakes, formatting, clarity).
    Use a friendly tone suitable for a 12-year-old, with newlines for separation. Do not include HTML tags.
    """
    response = call_api(user_input)
    feedback = ''
    if 'error' in response:
        feedback = f"API Error: {response['error']}"
        print(f"Feedback API error: {feedback}")
    elif 'choices' in response:
        feedback = markdown_to_html(response['choices'][0]['message']['content'])
        print(f"Summary feedback: {feedback}")

    concept_display_names = {
        'variables': 'Creating magical variables',
        'data-types': 'Solving data type puzzles',
        'conditional-statements': 'Making smart decisions (if, else)',
        'for-loop': 'Building powerful for loops',
        'while-loop': 'Keeping the code flowing (while loops)',
        'do-while-loop': 'Trying first with do-while loops',
        'functions': 'Casting magic spells (functions)',
        'operators': 'Being a math wizard (operators)',
        'input-output': 'Talking to computers (input/output)',
        'comments': 'Writing secret notes (comments)',
        'error-handling': 'Calling the code ambulance (error handling)',
        'arrays': 'Filling treasure chests (arrays)'
    }
    mastered_topics = [f"✨ {concept_display_names.get(concept, concept)}" for concept in concepts]
    if custom_challenge:
        mastered_topics.append(f"✨ {custom_challenge}")

    session.clear()
    return render_template('result.html',
                           hero_name=hero_name,
                           correct_answers=correct_answers,
                           total_questions=total_questions,
                           mastered_topics=mastered_topics,
                           feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)