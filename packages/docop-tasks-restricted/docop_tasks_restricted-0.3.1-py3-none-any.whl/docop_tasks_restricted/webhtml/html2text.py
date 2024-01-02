"""Extract plain text content of the HTML string.
- input: HTML text in the `html` field
- output: plaintext in the `text` field
"""

import trafilatura

extracted = trafilatura.extract(document["html"])
cleaned = extracted.replace('\n', ' ').replace('¶', ':').replace('\"', "'")

document["text"] = cleaned