## Deployment
- `cd /var/www/`
- `git clone git@github.com:frontbastard/jabydoo.git [DOMAIN_NAME]`
- `chmod +x /nginx/deploy_nginx.sh`
- `sudo deploy.sh`

## Rosetta translations
- `django-admin makemessages --all`
- `python manage.py compilemessages`
- and go to `/rosetta`

## Resources
- https://remixicon.com/
- https://api.together.ai/
