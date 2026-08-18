class ResponseBuilder:

    def __init__(self):
        pass

    def build(
        self,
        question,
        answer,
        chunks,
        metadata=None
    ):

        response = {

            "success": True,

            "question": question,

            "answer": answer,

            "sources": chunks

        }

        if metadata:

            response["metadata"] = metadata

        return response