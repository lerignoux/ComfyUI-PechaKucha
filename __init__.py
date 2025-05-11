from .pecha_kucha import GeneratePowerpoint
from .split_prompt import SplitPrompt
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GeneratePowerpoint": GeneratePowerpoint,
    "SplitPrompt": SplitPrompt
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GeneratePowerpoint": "Generate PechaKucha Powerpoint",
    "SplitPrompt": "Split Prompt (To Batch)"
}

__all__ = [NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS]
