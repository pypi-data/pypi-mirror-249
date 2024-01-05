from openai import OpenAI

class Poptimizer:
    def __init__(self, temperature):
        self.client = OpenAI()
        self.temperature = temperature

    def optimize_prompt(self, original_prompt, execute_optimized=False):
        """
        Optimizes a prompt using GPT and optionally executes the optimized prompt.

        :param original_prompt: A string containing the initial prompt.
        :param execute_optimized: A boolean that decides whether to execute the optimized prompt.
        :return: A string containing the improved/optimized prompt or its execution result.
        """
        optimization_prompt = f"""
        Please make the following original prompt more specific by following these instructions:

        - Write clear instructions
        - Split complex tasks into simpler subtasks
        - Specify the steps required to complete a task
        - Use delimiters to clearly indicate distinct parts of the input
        - Specify the desired length of the output

        Original Prompt:
        {original_prompt}"""

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": optimization_prompt}
            ]
        )

        optimized_prompt = completion.choices[0].message.content

        if execute_optimized:
            optimized_result = self.execute_optimized_prompt(optimized_prompt)
            return optimized_prompt, optimized_result

        return optimized_prompt

    def execute_optimized_prompt(self, optimized_prompt):
        """
        Executes an optimized prompt using ChatGPT.

        :param optimized_prompt: A string containing the optimized prompt.
        :return: The result of executing the optimized prompt.
        """
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": optimized_prompt}
            ]
        )

        result = completion.choices[0].message.content
        return result