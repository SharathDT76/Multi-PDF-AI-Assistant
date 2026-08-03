print(">>> NEW PromptBuilder Loaded <<<")
class PromptBuilder:

    def __init__(self):
        pass

    def build_prompt(self, question, retrieved_chunks):

        prompt = """
You are an AI assistant specialized in answering questions from uploaded PDF documents.

Instructions:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If the answer is not present in the context, reply:
   "I could not find the answer in the uploaded documents."
4. If multiple chunks contribute to the answer, combine them naturally.
5. Mention the source document and page number whenever possible.

==================================================
CONTEXT
==================================================

"""

        for i, chunk in enumerate(retrieved_chunks, start=1):

            prompt += f"""
Chunk {i}

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