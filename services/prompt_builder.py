class PromptBuilder:
    def __init__(self):
        pass

    def build_prompt(self, question, retrieved_chunks):

        prompt = """
You are an AI assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, reply:

"I could not find the answer in the uploaded documents."

Do not make up information.

==================================================
CONTEXT
==================================================

"""

        for chunk in retrieved_chunks:

            prompt += f"""
Source : {chunk['source']}
Page   : {chunk['page']}

Content:
{chunk['content']}

--------------------------------------------------

"""

        prompt += f"""
==================================================
QUESTION
==================================================

{question}

==================================================
ANSWER
==================================================

"""

        return prompt
    