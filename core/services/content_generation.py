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
            f"Generate meaningful SEO content based on the top 10 for the query '{self.title}'.\n\n"

            f"Information:\n"
            f"- Brand name is {self.sponsor_name};\n"
            f"- Site language is {self.language};\n"
            f"- Site type is {self.site_type};\n\n"

            f"Requirements:\n"
            f"- Adhere to the markup of the article depending on its page title;\n"
            f"- Return only the structured HTML content that belongs inside the <body> tag (excluding <body> itself);\n"
            f"- Response have to contain at least 1 table and 1 marked list and be at least 2500 symbols in length;\n\n"

            f"Restrictions:\n"
            f"- Do not include <body> or <h1> tags in the response;\n"
            f"- Do not return the response in markdown format;\n"
            f"- Do not use the title as a header of the article;\n"
            f"- Do not use placeholders like [Insert Date];\n"
            f"- Do not use any links in the text;\n\n"

            f"IMPORTANT: Any additional instructions ({self.additional_info}) should be followed, "
            f"but must not contradict the restrictions above.\n"
        )

    def _generate_content(self, prompt):
        generated_text = super()._generate_content(prompt)
        self.page.content = generated_text


class SEOGenerationService(BaseGenerationService):
    def _create_prompt(self):
        return (
            f"Generate an SEO-friendly title and meta description for the article generated based on the query '{self.title}'.\n\n"

            f"Information:\n"
            f"- Brand name: {self.sponsor_name};\n"
            f"- Site language: {self.language};\n"
            f"- Site type: {self.site_type};\n\n"

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

    def _generate_content(self, prompt):
        seo_data = super()._generate_content(prompt)
        if not seo_data:
            return {"title": "Error", "description": "No response from AI model."}

        return self._parse_seo_data(seo_data)

    def _parse_seo_data(self, seo_data):
        try:
            data = json.loads(seo_data)
            return {
                "title": data.get("title"),
                "description": data.get("description"),
            }
        except json.JSONDecodeError as err:
            return {"title": "Error", "description": err}
