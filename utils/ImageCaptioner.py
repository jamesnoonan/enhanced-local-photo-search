class ImageCaptioner:
    def __init__(self):
        # Load imports on init
        from PIL import Image
        import torch
        from transformers import (
            VisionEncoderDecoderModel,
            ViTImageProcessor, AutoTokenizer,
        )

        # Save references to use in other methods
        self.Image = Image

        model_name = "nlpconnect/vit-gpt2-image-captioning"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = VisionEncoderDecoderModel.from_pretrained(model_name).to(self.device)
        self.processor = ViTImageProcessor.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def caption(self, image_path):
        image = self.Image.open(image_path).convert("RGB")

        pixel_values = self.processor(
            images=image,
            return_tensors="pt"
        ).pixel_values.to(self.device)

        output_ids = self.model.generate(
            pixel_values,
            max_length=32,
            num_beams=4
        )

        return self.tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True
        ).strip()