import requests

def get_question_data():
    url = "https://opentdb.com/api.php"
    parameters = {
        "amount": 10,
        "category": 18,
        "difficulty": "easy",
        "type": "boolean"
    }

    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        return response.json()["results"]
    except (requests.RequestException, KeyError):
        # fallback question list
        return [
            {"question": "The HTML5 standard was published in 2014.", "correct_answer": "True"},
            {"question": "The first computer bug was formed by faulty wires.", "correct_answer": "False"},
            {"question": "FLAC stands for 'Free Lossless Audio Condenser'.", "correct_answer": "False"},
            {"question": "All program codes must be compiled into an executable to run.", "correct_answer": "False"},
            {"question": "Linus Torvalds created Linux and Git.", "correct_answer": "True"},
        ]
