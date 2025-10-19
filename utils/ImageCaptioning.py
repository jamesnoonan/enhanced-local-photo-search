from transformers import pipeline

class ImageCaptioner:
    def __init__(self):
        self.model = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

    def caption(self, image_path):
        response = self.model(image_path)

        if len(response) != 0:
            return response[0]["generated_text"]
        return ""