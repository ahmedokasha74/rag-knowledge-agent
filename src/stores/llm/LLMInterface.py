from abc import ABC, abstractmethod

class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_id: str):#بتجيب ال id بتاع الموديل اللي عايز تستخدمه في توليد النصوص
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass#بتجيب ال id بتاع الموديل اللي عايز تستخدمه في توليد النصوص وكمان حجم ال embedding اللي عايز تستخدمه

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        pass#بتجيب ال prompt اللي عايز تولد منه النصوص وكمان ال chat_history لو فيه و max_output_tokens لو عايز تحدد عدد الكلمات اللي عايز تولدها و temperature لو عايز تتحكم في تنوع النصوص اللي بتتولد

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        pass#بتجيب النص اللي عايز تحول ل embedding وكمان نوع ال document لو عايز تحدد نوع ال document اللي بتستخدمه في توليد ال embedding

    @abstractmethod
    def embed_texts(self, texts: list[str], document_type: str = None):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass#بتجيب ال prompt اللي عايز تولد منه النصوص وكمان ال role اللي عايز تحدده في ال chat_history زي user او assistant او system