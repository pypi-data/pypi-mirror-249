import openai

class GPTIntegration:
    def __init__(self, api_key, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
        """
        Initializes the GPT Integration with necessary parameters.
        Args:
            api_key (str): Your OpenAI API key.
            model (str): Identifier for the model to be used. Default is "gpt-3.5-turbo".
            temperature (float): Controls randomness. Lower is more deterministic.
            max_tokens (int): Maximum length of the token output.
            top_p (float): Controls diversity.
            frequency_penalty (float): Decreases the likelihood of previously used tokens.
            presence_penalty (float): Increases the likelihood of new tokens.
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.client = openai.OpenAI(api_key=self.api_key)

    def query_gpt(self, system_message, user_messages):
        if not isinstance(user_messages, list):
            user_messages = [user_messages]

        chat_messages = [{"role": "system", "content": system_message}] + \
                        [{"role": "user", "content": msg} for msg in user_messages]

        chat_completion = self.client.chat.completions.create(
            messages=chat_messages, model=self.model
        )
        return chat_completion
