from pydantic import BaseModel


class RetrievedDocument(BaseModel):
    score: floa
    text: str

class DataChunk(BaseModel):
    """
    Represents a chunk of data extracted from a document.
    """

    text: str
    metadata: dic
