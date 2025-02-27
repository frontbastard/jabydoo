from together import Together
from core.models import SiteOptions


class AIImageService:
    """
    A service for image generation using Together AI.
    """

    def __init__(self):
        self.api_key = getattr(SiteOptions.get_options(), "ai_secret_key", "")
        self.client = Together(api_key=self.api_key)

    def generate_image(self, model, prompt, width=1440, height=704):
        """
        Executes a query to Together AI and returns the generated image as base64 JSON.
        """
        if not model:
            return "Error: Model hasn't been defined"

        try:
            response = self.client.images.generate(
                prompt=prompt,
                width=width,
                height=height,
                model=model,
            )
            return response.data[0].url
        except Exception as e:
            return f"Error generating image: {str(e)}"
