from logging import getLogger
from os.path import join, exists
from urllib.request import URLopener

import torch
from transformers import AutoTokenizer


class Dialogue:
    __link_to_model = "https://voudy-data.s3.eu-north-1.amazonaws.com/dialogpt2_quant.pth"
    __path_to_model = join("src", "resources", "dialogue_model_weights.pth")

    def __init__(self):
        self.__logger = getLogger(__file__)
        self.__model = None
        try:
            self.__tokenizer = AutoTokenizer.from_pretrained("Grossmend/rudialogpt3_medium_based_on_gpt2")
            if not exists(self.__path_to_model):
                self.__logger.info("Can't find the weights for model, so download it")
                url_opener = URLopener()
                url_opener.retrieve(self.__link_to_model, self.__path_to_model)
            torch.backends.quantized.engine = "qnnpack"
            self.__model = torch.load(self.__path_to_model)
            self.__model.eval()
        except Exception as e:
            self.__logger.error(f"Error during model initialization: {e}")

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

    def generate_answer(self, message: str) -> str:
        # Encode the new user input, add parameters and return a tensor in PyTorch
        input_ids = self.__tokenizer.encode(f"|0|{self._get_length_param(message)}|{message}|1|-|", return_tensors="pt")

        # Generated a response
        with torch.no_grad():
            chat_history_ids = self.__model.generate(
                input_ids,
                num_return_sequences=1,
                max_length=256,
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

        return self.__tokenizer.decode(chat_history_ids[:, input_ids.shape[-1] :][0], skip_special_tokens=True)
