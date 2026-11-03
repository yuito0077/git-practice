from typing import Optional
import re

class PromptOptimizer:
    def optimize(self, prompt: str, category: str = 'general', context: Optional[str] = None) -> str:
        # Professional instructions to be prepended
        instruction = "You are a highly intelligent and helpful AI assistant. "
        instruction += "Please respond in a clear, concise, and natural Japanese tone. "
        instruction += "Use structured formatting (like bullet points or bold text) if it helps clarity. "
        instruction += "Ensure your answers are factually grounded and accurate.\n\n"

        # Context if available
        if context:
            instruction += f"Context information:\n{context}\n\n"

        instruction += "User Prompt:\n"

        # We append the original prompt directly so that masks remain intact
        optimized_prompt = instruction + prompt

        return optimized_prompt
