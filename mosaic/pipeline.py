from .prompt_optimizer import PromptOptimizer
from .model_selector import ModelSelector
from typing import Dict, Any, List

class Executor:
    def execute(self, model: str, prompt: str) -> str:
        # Dummy executor for testing purposes
        return f"Executed on {model} with prompt: {prompt}"

class Pipeline:
    def __init__(self):
        self.prompt_optimizer = PromptOptimizer()
        self.model_selector = ModelSelector()
        self.executor = Executor()
        self.traces: List[Dict[str, Any]] = []

    def add_trace(self, trace: Dict[str, Any]):
        self.traces.append(trace)

    def run(self, llm_input_prompt: str, route_decision: Dict[str, Any]) -> str:
        # Optimize prompt
        optimized_prompt = self.prompt_optimizer.optimize(
            llm_input_prompt,
            category=route_decision.get('category', 'general')
        )

        # Add trace step
        self.add_trace({
            'step': 5.8,
            'name': '生成前プロンプト最適化 (Prompt Optimizer)',
            'detail': '意図明確化・トーン調整・出力品質最大化'
        })

        # Select model
        selected_model = self.model_selector.select_model(
            category=route_decision.get('category', 'general'),
            offline=route_decision.get('offline', False),
            requires_quick_decision=route_decision.get('requires_quick_decision', False)
        )

        # Execute
        result = self.executor.execute(selected_model, optimized_prompt)
        return result
