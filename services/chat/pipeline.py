from services.retrieval.retriever import Retriever
from services.retrieval.query_expander import QueryExpander

from services.llm.prompt_builder import PromptBuilder
from services.llm.llm import LLMService

from services.chat.response_builder import ResponseBuilder
from services.chat.preprocessor import QuestionPreprocessor


class ChatPipeline:

    def __init__(self):

        self.preprocessor = QuestionPreprocessor()
        self.query_expander = QueryExpander()

        self.retriever = Retriever()

        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()

        self.response_builder = ResponseBuilder()

    def execute(self, question):

        # --------------------------------------------------
        # 1. Preprocess
        # --------------------------------------------------

        question = self.preprocessor.process(
            question
        )

        # --------------------------------------------------
        # 2. Query Expansion
        # --------------------------------------------------

        expanded_queries = (
            self.query_expander.expand(question)
        )

        # --------------------------------------------------
        # 3. Hybrid Retrieval
        # --------------------------------------------------

        chunks = self.retriever.search(
            expanded_queries,
            top_k=5
        )

        # --------------------------------------------------
        # 4. No relevant information
        # --------------------------------------------------

        if not chunks:

            return self.response_builder.build(
                question=question,
                answer=(
                    "I could not find enough relevant "
                    "information in the uploaded documents."
                ),
                chunks=[]
            )

        # --------------------------------------------------
        # 5. Prompt
        # --------------------------------------------------

        prompt = self.prompt_builder.build_prompt(
            question,
            chunks
        )

        # --------------------------------------------------
        # 6. LLM
        # --------------------------------------------------

        answer = self.llm.generate_response(
            prompt
        )

        # --------------------------------------------------
        # 7. Response
        # --------------------------------------------------

        return self.response_builder.build(
            question=question,
            answer=answer,
            chunks=chunks
        )