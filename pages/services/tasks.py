from celery import shared_task

from core.services.ai_content_service import AIContentService


@shared_task
def generate_content_task(page_id):
    """
    Generates content for a specific page.
    """
    from pages.models import Page  # Avoid cyclical imports

    page = Page.objects.filter(id=page_id).first()
    if not page:
        return f"Page {page_id} not found"

    ai_service = AIContentService()
    result = ai_service.generate_content_for_pages([page])  # Send a list from a single page

    if result["success"]:
        return f"Content generated for {page.title}"
    elif result["skipped"]:
        return f"Missing {result['skipped']}"
    else:
        return f"Failed to generate content for {page.title}"
