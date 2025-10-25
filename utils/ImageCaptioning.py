from transformers import pipeline
from widgets.ProgressDialog import show_progress_dialog


class ImageCaptioner:
    def __init__(self):
        progress = show_progress_dialog("Loading model... (This may take a couple minutes)", 1)
        self.model = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
        progress.setValue(1)
        progress.close()

    def caption(self, image_path):
        response = self.model(image_path)

        if len(response) != 0:
            return response[0]["generated_text"]
        return ""