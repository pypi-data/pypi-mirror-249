import requests
import json
from .utils import Optimizers

session = requests.Session()


class TGPT:
    def __init__(
        self,
        max_tokens: int = 600,
        temperature: float = 0.2,
        top_k: int = -1,
        top_p: float = 0.999,
        model: str = "llama-2-13b-chat",
        brave_key: str = "qztbjzBqJueQZLFkwTTJrieu8Vw3789u",
        timeout: int = 30,
    ):
        """Instantiate TGPT

        Args:
            brave_key (str, optional): Brave API access key. Defaults to "qztbjzBqJueQZLFkwTTJrieu8Vw3789u".
            model (str, optional): Text generation model name. Defaults to "llama-2-13b-chat".
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            temperature (float, optional): Charge of the generated text's randomness. Defaults to 0.2.
            top_k (int, optional): Chance of topic being repeated. Defaults to -1.
            top_p (float, optional): Sampling threshold during inference time. Defaults to 0.999.
            timeput (int, optional): Http requesting timeout. Defaults to 30
        """
        self.max_tokens_to_sample = max_tokens
        self.model = model
        self.stop_sequences = ["</response>", "</s>"]
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.chat_endpoint = "https://ai-chat.bsg.brave.com/v1/complete"
        self.stream_chunk_size = 64
        self.timeout = timeout
        self.last_response = {}
        self.headers = {
            "Content-Type": "application/json",
            "x-brave-key": brave_key,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/110.0",
        }
        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        session.headers.update(self.headers)

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
    ) -> dict:
        """Chat with AI

        Args:
            prompt (str): Prompt to be sent
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`
        Returns:
           dict : {}
        ```json
        {
            "completion": "\nNext: domestic cat breeds with short hair >>",
            "stop_reason": null,
            "truncated": false,
            "stop": null,
            "model": "llama-2-13b-chat",
            "log_id": "cmpl-3kYiYxSNDvgMShSzFooz6t",
            "exception": null
        }
        ```
        """
        if optimizer:
            if optimizer in self.__available_optimizers:
                prompt = getattr(Optimizers, optimizer)(prompt)
            else:
                raise Exception(
                    f"Optimizer is not one of {self.__available_optimizers}"
                )

        session.headers.update(self.headers)
        payload = {
            "max_tokens_to_sample": self.max_tokens_to_sample,
            "model": self.model,
            "prompt": f"[INST] {prompt} [/INST]",
            "self.stop_sequence": self.stop_sequences,
            "stream": stream,
            "top_k": self.top_k,
            "top_p": self.top_p,
        }

        def for_stream():
            response = session.post(
                self.chat_endpoint, json=payload, stream=True, timeout=self.timeout
            )
            if (
                not response.ok
                or not response.headers.get("Content-Type")
                == "text/event-stream; charset=utf-8"
            ):
                raise Exception(
                    f"Failed to generate response - ({response.status_code}, {response.reason}) - {response.text}"
                )

            for value in response.iter_lines(
                decode_unicode=True,
                delimiter="" if raw else "data:",
                chunk_size=self.stream_chunk_size,
            ):
                try:
                    resp = json.loads(value)
                    self.last_response.update(resp)
                    yield value if raw else resp
                except json.decoder.JSONDecodeError:
                    pass

        def for_non_stream():
            response = session.post(
                self.chat_endpoint, json=payload, stream=False, timeout=self.timeout
            )
            if (
                not response.ok
                or not response.headers.get("Content-Type", "") == "application/json"
            ):
                raise Exception(
                    f"Failed to generate response - ({response.status_code}, {response.reason}) - {response.text}"
                )
            resp = response.json()
            self.last_response.update(resp)
            return resp

        return for_stream() if stream else for_non_stream()

    def chat(self, prompt: str, stream: bool = False, optimizer: str = None) -> str:
        """Generate response `str`
        Args:
            prompt (str): Prompt to be sent
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`
        Returns:
            str: Response generated
        """

        def for_stream():
            for response in self.ask(prompt, True, optimizer):
                yield self.get_message(response)

        def for_non_stream():
            return self.get_message(self.ask(prompt, False, optimizer))

        return for_stream() if stream else for_non_stream()

    def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (dict): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert isinstance(response, dict), "Response should be of dict data-type only"
        return response.get("completion")


if __name__ == "__main__":
    bot = TGPT()
    while True:
        print(bot.ask(input(">>")))
        # for entry in bot.chat(input('>>'),True):
        #   print(entry)
