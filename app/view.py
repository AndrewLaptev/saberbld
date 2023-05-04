class View:
    def __init__(self, preambule: str) -> None:
        self.preambule = preambule

    def _draw_graph(self, graph: dict, sym="|") -> None:
        for dep in graph:
            if isinstance(graph[dep], dict):
                print(sym, dep)
                self._draw_graph(graph[dep], sym + "_ _ ")
            else:
                print(sym, dep)

    def _generate_list_graph(self, graph: dict) -> list[str]:
        lt_graph = []
        for dep in graph:
            if isinstance(graph[dep], dict):
                lt_graph.extend(self._generate_list_graph(graph[dep]))
                lt_graph.append(dep)
            else:
                lt_graph.append(dep)

        return lt_graph
    
    def print_list(self, items: list) -> None:
        print("\n".join(items))

    def print_graph(self, graph: dict) -> None:
        print(self.preambule)
        self._draw_graph(graph)

    def print_list_graph(self, graph: dict) -> None:
        print(self.preambule)
        print(", ".join(self._generate_list_graph(graph)))
