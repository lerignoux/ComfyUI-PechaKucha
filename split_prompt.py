import logging

log = logging.getLogger(__name__)


class SplitPrompt:
    """
    A simple node to split a prompt into a batch of prompt.
    Inspired from [ComfyUI-Inspire-Pack](https://github.com/ltdrdata/ComfyUI-Inspire-Pack)
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {"multiline": True, "default": "First Prompt \nSecond Prompt", "tooltip": "A multiline prompt that will be split to batch generate"}
                )
            },
            "optional": {
                "split_on": (
                    "STRING",
                    {"default": '\n', "tooltip": "Will split the input prompt on this character"}
                ),
                "trim": (
                    "BOOLEAN",
                    {"default": True, "tooltip": "Will trim prompts and remove empty ones"}
                ),
            }
        }

    CATEGORY = "pecha_kucha"
    DESCRIPTION = "Split a prompt in a list of prompts"
    FUNCTION = "split"
    OUTPUT_IS_LIST = (True,)
    RETURN_NAMES = ("Split Prompts",)
    RETURN_TYPES = ("STRING",)

    @staticmethod
    def IS_CHANGED(prompt, split_on='\n', trim=True):
        return f"trim:{trim}_split:{split_on}_prompt:{prompt}"

    @staticmethod
    def split(prompt, split_on='\n', trim=True):
        prompts = prompt.split(split_on)
        if trim:
            prompts = [prompt.strip() for prompt in prompts]
        return (prompts,)
