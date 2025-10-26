import logging
import os
import numpy
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from comfy_api.latest import io
import folder_paths

from .presentation_generation.pptx import Pptx

log = logging.getLogger(__name__)


class GeneratePowerpoint(io.ComfyNode):
    """
    A node to generate a PechaKucha presentation
    """

    INPUT_IS_LIST = True
    output_dir = folder_paths.get_output_directory()
    temp_dir = folder_paths.get_temp_directory()
    compress_level = 4

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="GeneratePowerpoint",
            display_name="Generate PechaKucha Powerpoint",
            description="Generates a Pecha Kucha generation from a list of images and prompts",
            category="pecha_kucha",
            inputs=[
                io.Image.Input("images"),
                io.String.Input(
                    "title",
                    default="My pecha",
                    multiline=False,
                    tooltip="The title of this Presentation.",
                ),
                io.String.Input(
                    "titles",
                    default="",
                    multiline=False,
                    tooltip="the titles for each slide.",
                ),
                io.Int.Input(
                    "slide_duration",
                    default=20,
                    min=0,
                    max=300,
                    step=1,
                    display_mode=io.NumberDisplay.number,
                    tooltip="Each slide duration in seconds.",
                ),
                io.Boolean.Input(
                    "show_titles",
                    default=False,
                    tooltip="Show each prompt as slide title. Needs to provide the titles input.",
                ),
            ],
            is_output_node=True,
            outputs=[io.String.Output(display_name="filename")],
        )

    @classmethod
    def save_images(cls, images, filename_prefix="PechaKucha"):
        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix, cls.temp_dir, images[0].shape[1], images[0].shape[0]
            )
        )
        results = list()
        log.debug(f"received {len(images)} images")
        for batch_number, image in enumerate(images):
            log.debug(f"start saving image {batch_number}, shape: {image.shape}")
            i = 255.0 * image.cpu().numpy().squeeze()
            img = Image.fromarray(numpy.clip(i, 0, 255).astype(numpy.uint8))
            metadata = None
            metadata = PngInfo()

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            path = os.path.join(full_output_folder, file)
            img.save(path, pnginfo=metadata, compress_level=cls.compress_level)
            results.append(path)
            counter += 1

        return results

    @classmethod
    def execute(cls, images, title, titles, slide_duration, show_titles):
        log.info(f"start pecha_kucha generation")
        images = cls.save_images(images)
        # The following inputs are also considered as list but only contain a single value
        title = title[0]
        slide_duration = slide_duration[0]
        show_titles = show_titles[0]
        output_folder = "./output/pecha_kucha"
        filename = Pptx(output_folder).generate(
            title, slide_duration, images, show_titles, titles
        )
        log.info(f"Generated presentation {filename}")
        return io.NodeOutput(
            filename,
        )

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        return float("NaN")
