class QueryExpander:

    def __init__(self):

        self.expansions = {

            "dfs": [
                "Depth First Search",
                "Graph Traversal",
                "Tree Traversal"
            ],

            "bfs": [
                "Breadth First Search",
                "Level Order Traversal"
            ],

            "hashmap": [
                "Hash Map",
                "Dictionary",
                "Key Value Pair"
            ],

            "stringbuilder": [
                "Mutable String",
                "append",
                "insert",
                "delete",
                "reverse"
            ],

            "binary tree": [
                "Root",
                "Left Child",
                "Right Child",
                "Tree Traversal"
            ]

        }

    def expand(self, question):

        expanded = [question]

        lower = question.lower()

        for keyword, values in self.expansions.items():

            if keyword in lower:

                expanded.extend(values)

        return list(dict.fromkeys(expanded))