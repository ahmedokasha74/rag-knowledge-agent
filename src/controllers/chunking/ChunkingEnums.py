from enum import Enum


class ChunkingType(str, Enum):

    TOKEN = "token"

    SEMANTIC = "semantic"

    RECURSIVE = "recursive"