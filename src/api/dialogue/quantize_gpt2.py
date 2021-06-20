from argparse import ArgumentParser

import torch
from torch._C._autograd import ProfilerActivity
from torch.autograd.profiler import record_function
from torch.profiler import profile
from transformers import Conv1D, GPT2PreTrainedModel, AutoModelForCausalLM

from src.api.dialogue.dialogue import Dialogue


def _conv1d_to_linear(module: torch.nn.Module) -> torch.nn.Linear:
    in_size, out_size = module.weight.shape
    linear = torch.nn.Linear(in_size, out_size)
    linear.weight.data = module.weight.data.T.contiguous()
    linear.bias.data = module.bias.data
    return linear


def _convert_conv1d_model_to_linear(model: torch.nn.Module) -> None:
    """in-place
    This is for Dynamic Quantization, as Conv1D is not recognized by PyTorch, convert it to nn.Linear
    """
    for name in list(model._modules):
        module = model._modules[name]
        if isinstance(module, Conv1D):
            linear = _conv1d_to_linear(module)
            model._modules[name] = linear
        else:
            _convert_conv1d_model_to_linear(module)


def quantize_model(model: GPT2PreTrainedModel) -> GPT2PreTrainedModel:
    assert isinstance(model, GPT2PreTrainedModel)
    _convert_conv1d_model_to_linear(model)
    torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8, inplace=True)
    return model


def main():
    arparser = ArgumentParser()
    arparser.add_argument("-m", "--model_name", type=str, default="Grossmend/rudialogpt3_medium_based_on_gpt2")
    arparser.add_argument("-o", "--out_path", type=str, required=True)
    args = arparser.parse_args()

    model = AutoModelForCausalLM.from_pretrained(args.model_name).eval()

    dialogue = Dialogue(model)
    inp = "Привет! Что делаешь?"
    out = dialogue.generate_answer(inp)
    print(f"Original output:\n-{inp}\n-{out}\n")

    model = quantize_model(model)
    torch.save(model, args.out_path)

    dialogue = Dialogue(args.out_path)
    inp = "Привет! Что делаешь?"
    out = dialogue.generate_answer(inp)
    print(f"Quantized output:\n-{inp}\n-{out}\n")


if __name__ == "__main__":
    main()
