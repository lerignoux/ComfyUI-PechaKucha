import logging

from comfy_api.latest import io, ui

log = logging.getLogger(__name__)


class DownloadPechaKucha(io.ComfyNode):
    """
    A simple node to view/download a generated PechaKucha Powerpoint.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="DownloadPechaKucha",
            display_name="Download a generated PechaKucha Powerpoint",
            description="Download a generated pecha kucha presentation",
            category="pecha_kucha",
            inputs=[
                io.String.Input(
                    "filename",
                    default="",
                    multiline=False,
                    tooltip="The path of this Presentation.",
                )
            ],
            is_output_node=True,
            outputs=[],
        )

    @classmethod
    def fingerprint_inputs(cls, filename):
        return float("NaN")

    @classmethod
    def execute(cls, filename):
        return io.NodeOutput(filename, ui=ui.PreviewText(filename, cls=cls))
