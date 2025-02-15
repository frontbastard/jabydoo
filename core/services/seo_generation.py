from together import Together
from core.models import SiteOptions
from django.contrib import messages


class SEOGenerationService:
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
        return self._generate_seo(prompt)

    def _create_prompt(self):
        return (
            f"Generate SEO-friendly title, description for the article '{self.title}' for the site {self.sponsor_name}. "
            f"Consider that the site language is {self.language}. The site type is {self.site_type}. "
            f"Do not use placeholders like [Insert Date]. Do not include any links in the text."
            f"Return content in JSON format like this:\n"
            f'{{"title": "<seo title>", "description": "<seo description>"}}'
        )

    def _generate_seo(self, prompt):
        client = Together(api_key=getattr(SiteOptions.get_options(), "ai_secret_key", ""))
        try:
            response = client.chat.completions.create(
                model=getattr(SiteOptions.get_options(), "ai_model", ""),
                messages=[{"role": "user", "content": prompt}]
            )
            seo_data = response.choices[0].message.content.strip()
            return self._parse_seo_data(seo_data)
        except Exception as e:
            return f"Generation error: {e}"

    def _parse_seo_data(self, seo_data):
        # Assuming the response is in JSON format
        import json
        try:
            data = json.loads(seo_data)
            return {
                "title": data.get("title", "aaa"),
                "description": data.get("description", "bbb"),
            }
        except json.JSONDecodeError:
            return {"title": "ggg", "description": "ggg"}
