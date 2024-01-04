import os
from datetime import datetime


class Generator:
    @staticmethod
    def output(data, path=None):
        if path is None:
            return data

        path = os.path.expanduser(path)
        filename = str(datetime.now().strftime("%Y%m%d_%H%M%S")) + ".html"

        # Create the output directory path
        if not os.path.exists(path):
            os.makedirs(path)

        # Write the HTML to disk
        with open(os.path.join(path, filename), "w", encoding="UTF-8") as file:
            file.write(data)
        with open(os.path.join(path, "latest.html"), "w", encoding="UTF-8") as file:
            file.write(data)
