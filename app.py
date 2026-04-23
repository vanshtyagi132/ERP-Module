"""Render/Gunicorn compatibility entrypoint.

Allows legacy start commands like `gunicorn app:app` to run this Django project.
"""

from college_management_system.wsgi import application

app = application
