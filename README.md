## Checklist
- settings
  - Language
- Admin page Options
  - Brand name
  - Site type
  - Secret Key
  - AI models
  - Custom CSS
- Menu Items
- Generate content
- Partners

## Deployment
- `cd /var/www/`
- `git clone git@github.com:frontbastard/jabydoo.git [DOMAIN_NAME]`
- `cd [DOMAIN_NAME]`
- customize .env `nano .env`
  - SITE_DOMAIN
  - SITE_TYPE
  - ENVIRONMENT
  - DJANGO_DEBUG
- `chmod +x deploy.sh`
- `sudo ./deploy.sh`

## Rosetta translations
- `django-admin makemessages --all`
  - or just for one lang `django-admin makemessages -l de`
- `python manage.py compilemessages`
- and go to `/rosetta`

## Resources
- https://remixicon.com/
- https://api.together.ai/
- https://dashboard.uptimerobot.com/monitors
