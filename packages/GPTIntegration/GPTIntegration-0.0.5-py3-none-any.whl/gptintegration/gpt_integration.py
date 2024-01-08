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

    def query_gpt_with_history(self, messages, model):
        """
        Queries the GPT model using a list of historical messages.
        Args:
            messages (list of dict): A list of messages with each message being a dict containing 'role' and 'content'.
        """
        if model is not None:
            self.model = model
        for message in messages:
            if not all(key in message for key in ['role', 'content']):
                raise ValueError("Each message must have 'role' and 'content' keys.")

        chat_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        chat_completion = self.client.chat.completions.create(
            messages=chat_messages, model=self.model
        )
        return chat_completion
