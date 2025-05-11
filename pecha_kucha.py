import io
import json
import logging
import os
import numpy
from PIL import Image
from PIL.PngImagePlugin import PngInfo

import folder_paths

from .presentation_generation.pptx import Pptx

log = logging.getLogger(__name__)


class GeneratePowerpoint:
    """
    A node to generate a PechaKucha presentation
    """
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.temp_dir = folder_paths.get_temp_directory()
        self.compress_level = 4
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "title": ("STRING", {
                    "multiline": False,
                    "default": "My pecha",
                    "tooltip": "The title of this Presentation"
                }),
                "titles": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "tooltip": "the titles for each slide."
                }),
                "slide_duration": ("INT", {
                    "default": 20,
                    "min": 0,
                    "max": 300,
                    "step": 1,
                    "display": "number",
                    "tooltip": "Each slide duration in seconds."
                }),
                "show_titles": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Show each prompt as slide title. Needs to provide the titles input."
                })
            },
        }

    CATEGORY = "pecha_kucha"
    DESCRIPTION = "Generates a Pecha Kucha generation from a list of images and prompts"
    FUNCTION = "generate_pptx"
    INPUT_IS_LIST = True
    OUTPUT_NODE = True
    RETURN_NAMES = ("filename",)
    RETURN_TYPES = ("STRING",)

    def save_images(self, images, filename_prefix="PechaKucha"):
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.temp_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        log.debug(f"received {len(images)} images")
        for (batch_number, image) in enumerate(images):
            log.debug(f"start saving image {batch_number}, shape: {image.shape}")
            i = 255. * image.cpu().numpy().squeeze()
            img = Image.fromarray(numpy.clip(i, 0, 255).astype(numpy.uint8))
            metadata = None
            metadata = PngInfo()

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            path = os.path.join(full_output_folder, file)
            img.save(path, pnginfo=metadata, compress_level=self.compress_level)
            results.append(path)
            counter += 1

        return results

    def generate_pptx(self, images, title, titles, slide_duration, show_titles):
        log.info(f"start pecha_kucha generation")
        images = self.save_images(images)
        # The following inputs are also considered as list but only contain a single value
        title = title[0]
        slide_duration = slide_duration[0]
        show_titles = show_titles[0]
        output_folder = "./output/pecha_kucha"
        filename = Pptx(output_folder).generate(title, slide_duration, images, show_titles, titles)
        log.info(f"Generated presentation {filename}")
        return (filename,)

    @classmethod
    def IS_CHANGED(s, images, title, titles, slide_duration, show_titles):
        return float("NaN")
