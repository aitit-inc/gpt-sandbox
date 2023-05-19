def system_prompt():
    return None

class AIConfig:
    """
    AIのためのコンフィグクラス

    Attributes:
        ai_name: AIの名前
        ai_role: AIの役割
        ai_goals: AIに達成させたい目標
    """
    def __init__(self, ai_name: str = "", ai_role: str = "", ai_goals: list = []):
        self.ai_name = ai_name
        self.ai_role = ai_role
        self.ai_goals = ai_goals

    def construct_full_prompt(self):
        """
        最初のプロンプトを生成
        (System prompt)
        """

        prompt_start = (
            "Your decisions must always be made independently without"
            " seeking user assistance. Play to your strengths as an LLM and pursue"
            " simple strategies with no legal complications."
            ""
        )

        full_prompt = (
            f"You are {self.ai_name}, {self.ai_role}\n{prompt_start}\n\nGOALS:\n\n"
        )
        for i, goal in enumerate(self.ai_goals):
            full_prompt += f"{i+1}. {goal}\n"

        return full_prompt
    
