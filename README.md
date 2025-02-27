## Checklist
- .env
  - SITE_DOMAIN
  - SITE_NAME
  - SITE_TYPE
  - ENVIRONMENT
  - DJANGO_DEBUG
  - POSTGRES_XXX
- Admin page Options
  - Site type
  - Secret Key
  - AI model
  - Custom CSS
- Pages
- Menu
- Partners

## Deployment
- `cd /var/www/`
- `git clone git@github.com:frontbastard/jabydoo.git [DOMAIN_NAME]`
- `chmod +x /nginx/deploy_nginx.sh`
- `sudo deploy.sh`

## Rosetta translations
- `django-admin makemessages --all`
  - or just for one lang `django-admin makemessages -l de`
- `python manage.py compilemessages`
- and go to `/rosetta`

## Resources
- https://remixicon.com/
- https://api.together.ai/
- https://dashboard.uptimerobot.com/monitors
