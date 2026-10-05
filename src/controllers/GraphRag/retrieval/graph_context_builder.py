from controllers.BaseController import BaseController


class GraphContextBuilder(BaseController):

    def __init__(self):
        super().__init__()

    def build(self, results: list[dict]) -> str:
        lines = []

        for result in results:
            source = result.get("source")
            relation = result.get("relation")
            target = result.get("target")

            if not source or not relation or not target:
                continue

            lines.append(
                f"{source} --{relation}--> {target}"
            )

        return "\n".join(lines)