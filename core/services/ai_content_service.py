import json

import together
from django.contrib.contenttypes.models import ContentType
from together import Together

from core.models import SiteOptions
from seo.models import SEO


class AIContentService:
    """
    A service for content generation using Together AI.
    """

    def __init__(self):
        together.api_key = getattr(SiteOptions.get_options(), "ai_secret_key", "")
        self.options = SiteOptions.get_options()

    def generate_text(self, prompt, max_tokens=500, temperature=0.7):
        """
        Executes a query to Together AI and returns the generated text.
        """
        client = Together(api_key=self.options.ai_secret_key)
        try:
            response = client.chat.completions.create(
                model=self.options.ai_model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Generation error: {e}"

    def generate_seo(self, content, page_title, max_tokens=150):
        """
        Generate SEO title and description based on the page content and title.
        Returns a JSON object with title and description.
        """
        prompt = (
            f"Generate an SEO-friendly title and meta description for the article generated based on the query '{page_title}'.\n\n"
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

        generated_text = self.generate_text(prompt, max_tokens)

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
            generated_text = self.generate_text(prompt)

            if generated_text:
                page.content = generated_text
                # Now generate SEO
                seo_title, seo_description = self.generate_seo(generated_text, page.title)
                if seo_title and seo_description:
                    # Save SEO data
                    self.update_seo_fields(page, seo_title, seo_description)
                page.save()
                results["success"].append(page)
            else:
                results["failed"].append(page)

        return results

    def update_seo_fields(self, page, seo_title, seo_description):
        # Визначаємо ContentType для сторінки
        content_type = ContentType.objects.get_for_model(page)

        # Спробуй отримати або створити SEO об'єкт
        seo_object, created = SEO.objects.get_or_create(
            content_type=content_type,
            object_id=page.id
        )

        # Оновлюємо SEO поля
        seo_object.title = seo_title
        seo_object.description = seo_description
        seo_object.save()
