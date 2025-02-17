from together import Together
from core.models import SiteOptions
from seo.models import SEO


class TranslationService:
    """
    A class for automatic content translation via the Together API.
    Translates title, content and inline SEO fields (title, description).
    """

    def __init__(self, page, target_language):
        self.page = page
        self.target_language = target_language
        self.client = Together(api_key=getattr(SiteOptions.get_options(), "ai_secret_key", ""))
        self.model = getattr(SiteOptions.get_options(), "ai_model", "")

    def translate(self):
        """
        Translates page title, content, seo_title, seo_description.
        It also translates SEO fields that are bound via GenericForeignKey.
        """
        translations = {}

        # Translation of title and content
        translations.update(
            self._translate_fields([('title', self.page.title), ('content', self.page.content.strip())]))

        # Translation of SEO fields that are bound via GenericForeignKey
        seo_fields_translations = self._translate_seo_fields()
        translations.update(seo_fields_translations)

        return translations

    def _translate_fields(self, fields):
        """
        Updates the fields of the page with the translation.
        :param fields: list of tuples (field, value)
        :return: dictionary with translated fields
        """
        translations = {}
        for field, value in fields:
            if value:
                translations[field] = self._translate_field(value)
        return translations

    def _translate_field(self, field_value):
        """
        Translates a single field via the Together API.
        """
        prompt = self._create_prompt(field_value)
        return self._generate_translation(prompt)

    def _create_prompt(self, text):
        """
        Generates a query for the AI model to translate a specific text.
        """
        return (
            f"Translate the following text from {self.page.get_current_language()} to {self.target_language}: \n\n"
            f"{text}\n\n"
            f"Return only translated text without any additional explanations."
        )

    def _generate_translation(self, prompt):
        """
        Sends a translation request to the Together API.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Translation error: {e}"

    def _translate_seo_fields(self):
        """
        Translates SEO fields associated with this page (via GenericForeignKey).
        """
        seo_translations = {}

        # Get SEO for this page using its id
        seo_object = SEO.objects.filter(object_id=self.page.id).first()

        if seo_object:
            # List of SEO fields to translate
            seo_fields = ["title", "description"]
            for field in seo_fields:
                field_value = getattr(seo_object, field, None)
                if field_value:
                    seo_translations[f"seo_{field}"] = self._translate_field(field_value)

        return seo_translations
