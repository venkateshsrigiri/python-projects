from question_model import Question
from data import get_question_data
from quiz_brain import QuizBrain
from ui import QuizInterface

question_data = get_question_data()

question_bank = [
    Question(q["question"], q["correct_answer"])
    for q in question_data
]

quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)
