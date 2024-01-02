from openai import OpenAI
import httpx
from rmbserver import config
from rmbserver.log import log
from rmbserver.exceptions import PromptTooLong


class OpenAILLM:

    def __init__(self):
        kwargs = {
            "api_key": config.openai_api_key,
            "timeout": 300,
            # "base_url": "https://api.portkey.ai/v1",
            # "default_headers": {
            #     "x-portkey-api-key": "1aqtCtfA6WrZyNhO2PdOk0iQtjg=",
            #     "x-portkey-provider": "openai",
            #     "Content-Type": "application/json"
            # },
        }
        if config.openai_proxy:
            kwargs["http_client"] = httpx.Client(
                proxies=config.openai_proxy,
            )
        self.client = OpenAI(**kwargs)

    def predict(self, prompt, json_format=False):
        log.debug(f"LLM PROMPT: {prompt}")
        max_prompt_length = config.openai_max_token * 2
        if len(prompt) > max_prompt_length:
            raise PromptTooLong(f"Prompt is too long: {len(prompt)} > {max_prompt_length}")

        if json_format:
            kwargs = {
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": prompt}
                ],
            }
        else:
            kwargs = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
            }

        response = self.client.chat.completions.create(
            model=config.openai_model_name,
            temperature=0,
            max_tokens=config.openai_max_token,
            **kwargs
        )
        output = response.choices[0].message.content
        log.debug(f"LLM OUTPUT:  {output}")
        return output, response.usage.prompt_tokens, response.usage.completion_tokens

    def embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(
            input=[text],
            model=config.openai_embedding_model
        ).data[0].embedding

    def embedding_batch(self, text_list):
        text_list = [text.replace("\n", " ") for text in text_list]
        log.info(f"embedding_batch: {text_list}")
        response = self.client.embeddings.create(
            input=text_list,
            model=config.openai_embedding_model,
            encoding_format="float"
        ).data
        return [data.embedding for data in response]


openai_llm = OpenAILLM()
