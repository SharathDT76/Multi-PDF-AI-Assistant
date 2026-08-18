import re


class QuestionPreprocessor:

    def __init__(self):
        pass

    def process(self, question):

        question = question.strip()

        question = re.sub(r"\s+", " ", question)

        question = re.sub(r"[!?]{2,}", "?", question)

        replacements = {

            "string builder": "StringBuilder",

            "hash map": "HashMap",

            "array list": "ArrayList",

            "linked list": "LinkedList"

        }

        lower = question.lower()

        for key, value in replacements.items():

            lower = lower.replace(key, value.lower())

        return lower