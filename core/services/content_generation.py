from together import Together
from core.models import SiteOptions
from django.contrib import messages
import json


class BaseGenerationService:
    def __init__(self, page, request=None):
        self.page = page
        self.request = request
        self.sponsor_name = getattr(SiteOptions.get_options(), "sponsor_name", "").strip()
        self.language = page.get_current_language()
        self.title = page.title
        self.site_type = getattr(SiteOptions.get_options(), "site_type", "")

    def generate(self):
        if not self.sponsor_name:
            error_message = "Error: SiteOptions.sponsor_name hasn't been set!"
            if self.request:
                messages.error(self.request, error_message)
            return error_message

        prompt = self._create_prompt()
        return self._generate_content(prompt)

    def _create_prompt(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def _generate_content(self, prompt):
        client = Together(api_key=getattr(SiteOptions.get_options(), "ai_secret_key", ""))
        try:
            response = client.chat.completions.create(
                model=getattr(SiteOptions.get_options(), "ai_model", ""),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Generation error: {e}"


class ContentGenerationService(BaseGenerationService):
    def __init__(self, page, request=None):
        super().__init__(page, request)
        self.additional_info = page.ai_additional_info or ""

    def generate(self):
        if len(self.page.content) > 20:
            return
        return super().generate()

    def _create_prompt(self):
        return (
            f"Generate meaningful and unique SEO content based on the top 10 for the query '{self.title}' (title). "
            f"For the site {self.sponsor_name}. Insert bulleted lists and tables where appropriate. "
            f"The content should not be the same type, look at the `title` and stick to its possible template.  "
            f"Please note that the site language is {self.language}. The site type is {self.site_type}. "
            f"Do not use placeholders like [Insert Date]. Do not use any links in the text. "
            f"You do not need to add an h1 header at the beginning, it is already in the template. "
            f"IMPORTANT: Return the result as valid, structured HTML. Example format: "
            f"<html content is here (not markdown)>"
            f"If there are further instructions, they take precedence over previous ones: {self.additional_info}. "
        )

    def _generate_content(self, prompt):
        generated_text = super()._generate_content(prompt)
        self.page.content = generated_text


class SEOGenerationService(BaseGenerationService):
    def _create_prompt(self):
        return (
            f"Generate SEO-friendly title, description for the article '{self.title}' for the site {self.sponsor_name}. "
            f"Consider that the site language is {self.language}. The site type is {self.site_type}. "
            f"Do not use placeholders like [Insert Date]. Do not include any links in the text. "
            f"Return content in JSON format like this:\n"
            f'{{"title": "<seo title>", "description": "<seo description>"}}'
        )

    def _generate_content(self, prompt):
        seo_data = super()._generate_content(prompt)
        return self._parse_seo_data(seo_data)

    def _parse_seo_data(self, seo_data):
        try:
            data = json.loads(seo_data)
            return {
                "title": data.get("title", "aaa"),
                "description": data.get("description", "bbb"),
            }
        except json.JSONDecodeError:
            return {"title": "ggg", "description": "ggg"}
