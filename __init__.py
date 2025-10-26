from comfy_api.latest import ComfyExtension, io

from .download_pecha_kucha import DownloadPechaKucha
from .pecha_kucha import GeneratePowerpoint
from .split_prompt import SplitPrompt

WEB_DIRECTORY = "./web"


class PechaKucha(ComfyExtension):
    # must be declared as async
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [
            DownloadPechaKucha,
            GeneratePowerpoint,
            SplitPrompt,
        ]


# can be declared async or not, both will work
async def comfy_entrypoint() -> PechaKucha:
    return PechaKucha()


__all__ = ["WEB_DIRECTORY"]
