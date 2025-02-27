import base64
import json

import requests
import together
from django.contrib.contenttypes.models import ContentType
from django.core.files import File as DjangoFile
from django.core.files.base import ContentFile
from django.utils.text import slugify
from filer.models import File, Image
from together import Together

from core.models import SiteOptions
from core.services.ai_image_service import AIImageService
from seo.models import SEO


class AIContentService:
    """
    A service for content generation using Together AI.
    """

    def __init__(self):
        self.options = SiteOptions.get_options()

    def generate_text(self, prompt, model):
        """
        Executes a query to Together AI and returns the generated text.
        """
        if not prompt or not isinstance(prompt, str):
            return "Error: Invalid prompt"

        if not model:
            return "Error: Model hasn't been defined"

        client = Together(api_key=self.options.ai_secret_key)
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Generation error: {e}"

    def generate_seo(self, page_title, page_content):
        """
        Generate SEO title and description based on the page content and title.
        Returns a JSON object with title and description.
        """
        prompt = (
            f"Generate an SEO-friendly title and meta description for the article generated "
            f"based on the query '{page_title}' and '{page_content}'.\n\n"
            f"Information:\n"
            f"- Brand name: {self.options.sponsor_name};\n"
            f"- Site type: {self.options.site_type};\n\n"
            f"Requirements:\n"
            f"- The title should be engaging, relevant, and include the main keyword from the query;\n"
            f"- The title must be between 50-60 characters long;\n"
            f"- The meta description should summarize the article concisely and persuasively;\n"
            f"- The meta description must be between 140-160 characters long;\n"
            f"- Both elements should be naturally readable and encourage user engagement.\n\n"
            f"Restrictions:\n"
            f"- Do not use clickbait or misleading phrases;\n"
            f"- Do not include duplicate information from the article title in the meta description;\n"
            f"- Do not use placeholders like [Insert Keyword] or [Insert Date];\n"
            f"- Do not use any links;\n"
            f"- Do not exceed the recommended character limits.\n\n"
            f"Return only a valid JSON object (without any explanations or formatting) like this:\n"
            f'{{"title": "<title>", "description": "<description>"}}'
        )

        generated_text = self.generate_text(prompt, model=self.options.ai_chat_model)

        if generated_text:
            try:
                # Parse the JSON response
                seo_data = json.loads(generated_text)
                seo_title = seo_data.get("title", "")
                seo_description = seo_data.get("description", "")
                return seo_title, seo_description
            except json.JSONDecodeError:
                return None, None
        else:
            return None, None

    def generate_content_for_pages(self, queryset):
        """
        Generates content for the transferred pages and returns the results.
        """
        results = {"success": [], "skipped": [], "failed": []}

        for page in queryset:
            if not page.title or not page.slug:
                results["skipped"].append(f"{page} (no title or slug)")
                continue

            prompt = (
                f"Generate meaningful SEO content based on the top 10 for the query '{page.title}'.\n"
                f"Brand name is {self.options.sponsor_name}. "
                f"Site language is {page.get_current_language()}. "
                f"Site type is {self.options.site_type}.\n"
                f"Adhere to the markup of the article depending on its page title. "
                f"Return only the structured HTML content (not markdown) for the <body> tag. "
                f"Response have to contain at least 1 table and 1 marked list and be at least 2500 symbols in length.\n"
                f"Do not include <body> or <h1> tags in the response. "
                f"Do not use the title as a header of the article. "
                f"Do not use placeholders like [Insert Date]. "
                f"Do not use any links in the text.\n"
                f"{page.ai_additional_info}.\n "
            )

            if len(page.content) > 20:
                generated_text = page.content
            else:
                generated_text = self.generate_text(prompt, model=self.options.ai_chat_model)

            if generated_text:
                page.content = generated_text
                # Now generate SEO
                seo_title, seo_description = self.generate_seo(page.title, page_content=page.content)
                if seo_title and seo_description:
                    # Save SEO data
                    self.update_seo_fields(page, seo_title, seo_description)

                if not page.image:
                    # Image generation
                    image_url = self.generate_image_for_page(
                        f"Generate meaningful image for page title '{page.title}'.\n"
                        f"The focus is on '{self.options.site_type}'. The image should be without words."
                    )
                    if image_url:
                        self.save_image_from_url(image_url, page)

                page.save()
                results["success"].append(page)
            else:
                results["failed"].append(page)

        return results

    def update_seo_fields(self, page, seo_title, seo_description):
        # Define the ContentType for the page
        content_type = ContentType.objects.get_for_model(page)

        # Try to get or create an SEO object
        seo_object, created = SEO.objects.get_or_create(
            content_type=content_type,
            object_id=page.id
        )

        # Update SEO fields
        seo_object.title = seo_title
        seo_object.description = seo_description

        seo_object.save()

    def generate_image_for_page(self, title):
        """
        Generates an image for the page using the title as a prompt.
        """
        ai_image_service = AIImageService()
        return ai_image_service.generate_image(prompt=title, model=self.options.ai_image_model)

    def save_image_from_url(self, image_url, page):
        """
        Saves a base64 image to the page model's image field using Django Filer.
        """
        try:
            if not image_url:
                return "Error: No image URL"

            response = requests.get(image_url)

            # Check if the image was uploaded successfully
            if response.status_code != 200:
                return f"Error: Unable to fetch image (Status code {response.status_code})"

            # Decode base64 images into binary data
            image_data = response.content

            # Generate a file name
            file_name = f"{slugify(page.title)}_image.png"

            # Creating a ContentFile object without base64 encoding
            content_file = ContentFile(image_data)

            image_file = Image.objects.create(
                file=DjangoFile(content_file, file_name),
                name=file_name,
            )

            page.image = image_file
            page.save()

            return image_file
        except Exception as e:
            return f"Error saving image: {str(e)}"
