## Rosetta translations

`django-admin makemessages --all`
and go to `/rosetta`

## Autorun docker daemon

`sudo systemctl enable docker`

### Config

`sudo nano /etc/systemd/system/jabydoo.service`

```ini
[Unit]
Description = Jabydoo
After = docker.service
Requires = docker.service

[Service]
Restart = always
WorkingDirectory = /path/to/your/project
ExecStart = /usr/local/bin/docker-compose up
ExecStop = /usr/local/bin/docker-compose down
TimeoutStartSec = 0

[Install]
WantedBy = multi-user.target

```

### Run

`sudo systemctl daemon-reload`

`sudo systemctl enable myapp.service`

`sudo systemctl start myapp.service`

### Check

`sudo systemctl status myapp.service`


## Resources
- https://remixicon.com/
- https://api.together.ai/
