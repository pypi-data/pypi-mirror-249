from openai import OpenAI

class Poptimizer:
    """
    Poptimizer (Prompt Optimizer) is a class designed to optimize prompts for ChatGPT models.
    It enhances original prompts to be more specific, clear, and structured, thus improving
    the quality of responses from the AI model.

    Attributes:
        client (OpenAI): An instance of the OpenAI client.
        temperature (float): A temperature setting for the AI model, influencing the creativity
                             and variability of responses.

    Methods:
        optimize_prompt(original_prompt, execute_optimized=False): Optimizes a given prompt and
                                                                   optionally executes it.
        execute_optimized_prompt(optimized_prompt): Executes an optimized prompt and returns the
                                                    AI's response.
    """

    def __init__(self, temperature):
        """
        Initializes the Poptimizer with a specific temperature setting for the AI responses.

        Args:
            temperature (float): Temperature setting for the AI model's responses.
        """
        self.client = OpenAI()
        self.temperature = temperature

    def optimize_prompt(self, original_prompt, execute_optimized=False):
        """
        Optimizes a prompt using GPT and optionally executes the optimized prompt.

        Args:
            original_prompt (str): The initial prompt to be optimized.
            execute_optimized (bool): If True, executes the optimized prompt and returns its result.

        Returns:
            str: The optimized prompt.
            tuple: The optimized prompt and its execution result, if execute_optimized is True.
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
        Executes an optimized prompt using ChatGPT and returns the result.

        Args:
            optimized_prompt (str): The optimized prompt to be executed.

        Returns:
            str: The result of executing the optimized prompt.
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