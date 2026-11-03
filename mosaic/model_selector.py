class ModelSelector:
    def select_model(self, category: str, offline: bool = False, requires_quick_decision: bool = False) -> str:
        if offline or requires_quick_decision:
            return 'local-3b' # Tier 0: Quick decisions or offline

        if category in ['general', 'qa']:
            return 'gemini-3.8-flash' # Tier 2: General conversation / Q&A

        if category in ['complex_reasoning', 'coding', 'deep_analysis']:
            # Either 'claude-sonnet-5-5' (Tier 3) or 'gemini-3.8-flash' could be used
            # Defaulting to claude-sonnet-5-5 for most complex tasks here
            return 'claude-sonnet-5-5'

        # Default fallback
        return 'gemini-3.8-flash'
