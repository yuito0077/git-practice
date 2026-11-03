import json
import re
from typing import Dict, Any, List, Tuple

class RewardVerifier:
    def __init__(self):
        # Execution-grounded rewards
        self.reward_syntax = 1.0
        self.reward_execution = 2.0
        self.reward_success = 5.0
        self.penalty_syntax = -1.0
        self.penalty_execution = -1.0

    def verify_json_syntax(self, output_text: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Extracts JSON from text and checks if it's valid tool syntax.
        Expected format: ```json\n{...}\n```
        """
        match = re.search(r'```json\s*(\{.*?\})\s*```', output_text, re.DOTALL)
        if not match:
            return False, {}

        try:
            tool_call = json.loads(match.group(1))
            if "tool" in tool_call and "args" in tool_call:
                return True, tool_call
            return False, {}
        except json.JSONDecodeError:
            return False, {}

    def simulate_tool_execution(self, tool_call: Dict[str, Any]) -> bool:
        """
        Simulate the execution of a tool to ground the reward.
        In a real scenario, this would call actual tools (e.g., search, calculate).
        """
        tool_name = tool_call.get("tool")
        args = tool_call.get("args", {})

        # Simple mocked execution logic
        if tool_name == "calculator" and "expression" in args:
            expr = str(args["expression"])
            # Validate that expression only contains allowed characters to prevent ACE
            if re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expr):
                try:
                    # Safe to eval because of regex restricting to digits and math operators
                    eval(expr, {"__builtins__": {}}, {})
                    return True
                except Exception:
                    return False
            return False
        elif tool_name == "search" and "query" in args:
            return len(args["query"]) > 0

        return False

    def evaluate_step(self, output_text: str, is_final_step: bool = False, success: bool = False) -> float:
        """
        Evaluate a single step of the multi-step execution.
        """
        reward = 0.0

        if is_final_step:
            if success:
                reward += self.reward_success
            return reward

        # 1. Check syntax
        is_valid_syntax, tool_call = self.verify_json_syntax(output_text)
        if is_valid_syntax:
            reward += self.reward_syntax

            # 2. Check execution
            is_valid_execution = self.simulate_tool_execution(tool_call)
            if is_valid_execution:
                reward += self.reward_execution
            else:
                reward += self.penalty_execution
        else:
            reward += self.penalty_syntax

        return reward

def test_verifier():
    verifier = RewardVerifier()

    # Test valid syntax and valid execution
    text1 = 'Here is my tool call:\n```json\n{"tool": "calculator", "args": {"expression": "2+2"}}\n```'
    r1 = verifier.evaluate_step(text1)
    print(f"Test 1 Reward (Expected {verifier.reward_syntax + verifier.reward_execution}): {r1}")

    # Test valid syntax, invalid execution
    text2 = 'Here is my tool call:\n```json\n{"tool": "calculator", "args": {"expression": "2 / 0"}}\n```'
    r2 = verifier.evaluate_step(text2)
    print(f"Test 2 Reward (Expected {verifier.reward_syntax + verifier.penalty_execution}): {r2}")

    # Test invalid syntax
    text3 = 'Here is my tool call:\n```json\n{"tool": "calculator", "args": \n```'
    r3 = verifier.evaluate_step(text3)
    print(f"Test 3 Reward (Expected {verifier.penalty_syntax}): {r3}")

if __name__ == "__main__":
    test_verifier()
