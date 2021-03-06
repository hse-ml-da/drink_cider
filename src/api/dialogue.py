from logging import getLogger
from os.path import join, exists
from typing import Dict

import torch
from transformers import AutoTokenizer


class Dialogue:
    __path_to_model = join("src", "resources", "dialogue_model_weights.pth")
    __n_context_tokens = 512

    def __init__(self):
        self.__logger = getLogger(__file__)
        self.__model = None
        if not exists(self.__path_to_model):
            self.__logger.info(f"Can't find weights for model in {self.__path_to_model}")
        else:
            try:
                self.__tokenizer = AutoTokenizer.from_pretrained("Grossmend/rudialogpt3_medium_based_on_gpt2")
                self.__model = torch.load(self.__path_to_model)
                self.__model.eval()
            except Exception as e:
                self.__logger.error(f"Error during model initialization: {e}")

        self.__history: Dict[int, torch.Tensor] = {}

    @property
    def enabled(self) -> bool:
        return self.__model is not None

    def _get_length_param(self, text: str) -> str:
        tokens_count = len(self.__tokenizer.encode(text))
        if tokens_count <= 15:
            len_param = "1"
        elif tokens_count <= 50:
            len_param = "2"
        elif tokens_count <= 256:
            len_param = "3"
        else:
            len_param = "-"
        return len_param

    def generate_answer(self, message: str, user_id: int) -> str:
        # Encode the new user input, add parameters and return a tensor in PyTorch
        input_ids = self.__tokenizer.encode(f"|0|{self._get_length_param(message)}|{message}|1|-|", return_tensors="pt")

        if user_id in self.__history:
            input_ids = torch.cat([self.__history[user_id], input_ids], dim=-1)[:, -self.__n_context_tokens :]

        # Generated a response
        with torch.no_grad():
            self.__history[user_id] = self.__model.generate(
                input_ids,
                num_return_sequences=1,
                max_length=self.__n_context_tokens,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=50,
                top_p=0.9,
                temperature=0.6,
                mask_token_id=self.__tokenizer.mask_token_id,
                eos_token_id=self.__tokenizer.eos_token_id,
                unk_token_id=self.__tokenizer.unk_token_id,
                pad_token_id=self.__tokenizer.pad_token_id,
                device="cpu",
            )

        return self.__tokenizer.decode(self.__history[user_id][:, input_ids.shape[-1] :][0], skip_special_tokens=True)
