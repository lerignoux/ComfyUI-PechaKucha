import logging

from comfy_api.latest import io

log = logging.getLogger(__name__)


class SplitPrompt(io.ComfyNode):
    """
    A simple node to split a prompt into a batch of prompt.
    Inspired from [ComfyUI-Inspire-Pack](https://github.com/ltdrdata/ComfyUI-Inspire-Pack)
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="SplitPrompt",
            display_name="Split prompt",
            description="Split a prompt in a list of prompts",
            category="pecha_kucha",
            inputs=[
                io.String.Input(
                    "prompt",
                    default="First Prompt \nSecond Prompt",
                    multiline=True,
                    tooltip="A multiline prompt that will be split to batch generate.",
                ),
                io.String.Input(
                    "split_on",
                    default="\n",
                    multiline=False,
                    tooltip="Will split the input prompt on this character.",
                ),
                io.Boolean.Input(
                    "trim",
                    default=True,
                    tooltip="Will trim prompts and remove empty ones.",
                ),
            ],
            is_output_node=False,
            outputs=[io.String.Output(display_name="split prompt")],
        )

    OUTPUT_IS_LIST = (True,)

    @classmethod
    def fingerprint_inputs(cls, prompt, split_on="\n", trim=True):
        return f"trim:{trim}_split:{split_on}_prompt:{prompt}"

    @classmethod
    def execute(cls, prompt, split_on="\n", trim=True):
        prompts = prompt.split(split_on)
        if trim:
            prompts = [prompt.strip() for prompt in prompts]
        return (prompts,)
