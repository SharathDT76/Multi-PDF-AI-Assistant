def print_documents(documents):

    for i, doc in enumerate(documents, start=1):

        print("=" * 80)
        print(f"Document #{i}")
        print(f"Source : {doc['source']}")
        print(f"Page   : {doc['page']}")
        print("-" * 80)
        print(doc["text"])
        print("=" * 80)
        print()