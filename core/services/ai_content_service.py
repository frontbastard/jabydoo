import json
from abc import ABC, abstractmethod

import requests
import validators
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.files import File as DjangoFile
from django.core.files.base import ContentFile
from django.utils.text import slugify
from filer.models import Image
from together import Together

from core.models import SiteOptions
from seo.models import SEO


class AIClient(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, model: str) -> str:
        pass

    @abstractmethod
    def generate_image(self, prompt: str, model: str, width: int, height: int) -> str:
        pass


class TogetherAIClient(AIClient):
    def __init__(self, api_key: str):
        self.client = Together(api_key=api_key)

    def generate_text(self, prompt: str, model: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Generation error: {e}"

    def generate_image(self, prompt: str, model: str, width: int, height: int) -> str:
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


class ContentGenerationService:
    def __init__(self, ai_client: AIClient, options: SiteOptions):
        self.ai_client = ai_client
        self.options = options

    def generate_text(self, prompt: str) -> str:
        return self.ai_client.generate_text(prompt, self.options.ai_chat_model)

    def generate_image(self, prompt: str) -> str:
        return self.ai_client.generate_image(prompt, self.options.ai_image_model, 1440, 704)

    def generate_seo(self, page_title: str, page_content: str) -> dict:
        prompt = (
            f"Generate an SEO-friendly title and meta description for '{page_title}' "
            f"for a website on the topic of '{self.options.activity}'.\n"
            f"Title: 50-60 characters.\nDescription: 140-160 characters.\n"
            f"Respond ONLY with a JSON object in the following format (without any additional text): "
            f"{{'title': '<title>', 'description': '<description>'}}"
        )
        generated_text = self.generate_text(prompt)
        try:
            return json.loads(generated_text)
        except json.JSONDecodeError:
            return {}


class FileService:
    @staticmethod
    def save_image_from_url(image_url: str, page: object) -> Image:
        response = requests.get(image_url)
        if response.status_code != 200:
            raise ValueError(f"Unable to fetch image (Status code {response.status_code})")

        image_data = response.content
        file_name = f"{slugify(page.title)}_image.png"
        content_file = ContentFile(image_data)

        image_file = Image.objects.create(
            file=DjangoFile(content_file, file_name),
            name=file_name,
        )

        page.image = image_file
        page.save()
        return image_file


class AIContentService:
    def __init__(self, ai_client: AIClient, content_service: ContentGenerationService, file_service: FileService):
        self.ai_client = ai_client
        self.content_service = content_service
        self.file_service = file_service

    def generate_content_for_page(self, page):
        if not page.title or not page.slug:
            return {"status": "skipped", "message": "No title or slug"}

        prompt = (
            f"Generate structured SEO content (minimum 2500 symbols) for the page title '{page.title}',"
            f"site name is {self.content_service.options.brand_name}, "
            f"for a website on the topic of '{self.content_service.options.activity}'. No links in the response.\n"
            f"Respond only with an HTML content for a WYSIWYG editor. Do not include <html>, <body>, or <h1> tags. \n"
            f"Start with <h2> for headings. Return only valid HTML without any additional text or explanations.\n\n"
            f"Create HTML content with the following requirements:\n"
            f"- Use only tags allowed in the body of an HTML document\n"
            f"- Start with <h2> for the main heading\n"
            f"- Include at least one table and one unordered list\n"
            f"- Do not use <h1>, <html>, <body>, or any other structural tags\n"
            f"- Ensure all tags are properly closed\n"
            f"{page.ai_additional_info}."
        )
        generated_text = self.content_service.generate_text(prompt)

        if not generated_text:
            return {"status": "failed", "message": "Failed to generate content"}

        page.content = generated_text
        seo_data = self.content_service.generate_seo(page.title, page.content)
        if seo_data:
            self.update_seo_fields(page, seo_data)

        if self.content_service.options.ai_image_model and not page.image:
            image_url = self.content_service.generate_image(
                f"Generate an image for the article '{page.title}' "
                f"for a topic of '{self.content_service.options.activity}'. Don't use text on images. \n"
                f"The image should match the website's theme and the article's content."
            )
            if image_url and validators.url(image_url):
                self.file_service.save_image_from_url(image_url, page)
            else:
                messages.warning(None, "AI image generation failed. Skipping image.")

        page.save()
        return {"status": "success", "page": page}

    def update_seo_fields(self, page, seo_data):
        content_type = ContentType.objects.get_for_model(page)
        seo_object, created = SEO.objects.get_or_create(content_type=content_type, object_id=page.id)
        seo_object.title = seo_data.get("title", "")
        seo_object.description = seo_data.get("description", "")
        seo_object.save()
