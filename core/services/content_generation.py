from together import Together
from core.models import SiteOptions
from django.contrib import messages


class ContentGenerationService:
    def __init__(self, page, request=None):
        self.page = page
        self.request = request
        self.sponsor_name = getattr(SiteOptions.get_options(), "sponsor_name", "").strip()
        self.language = page.get_current_language()
        self.title = page.title
        self.additional_info = page.ai_additional_info or ""
        self.site_type = getattr(SiteOptions.get_options(), "site_type", "")

    def generate(self):
        if not self.sponsor_name:
            error_message = "Error: SiteOptions.sponsor_name haven't been set!"
            if self.request:
                messages.error(self.request, error_message)
            self.page.content = error_message
            return

        if len(self.page.content) > 20:
            return

        prompt = self._create_prompt()
        return self._generate_content(prompt)

    def _create_prompt(self):
        return (
            f"Згенеруй змістовний та унікальний SEO контент для статті '{self.title}' для сайту {self.sponsor_name}. "
            f"Врахуй, що мова сайту – {self.language}. Тип сайту — {self.site_type}"
            f"Не використовуй заповнювачі потипу [Insert Date]. Не використовуй ніяких посилань в тексті."
            f"Генеруй контент в html для візуального редактора в джанго CKEDITOR 5."
            f"На початку не потрібно додавати h1 заголовок, він вже є в шаблоні."
            f"Подальші інструкції мають приорітет перед попередніми: {self.additional_info}"
        )

    def _generate_content(self, prompt):
        client = Together(api_key=getattr(SiteOptions.get_options(), "ai_secret_key", ""))
        try:
            response = client.chat.completions.create(
                model=getattr(SiteOptions.get_options(), "ai_model", ""),
                messages=[{"role": "user", "content": prompt}]
            )
            generated_text = response.choices[0].message.content.strip()
            self.page.content = generated_text
        except Exception as e:
            self.page.content = f"Generation error: {e}"
