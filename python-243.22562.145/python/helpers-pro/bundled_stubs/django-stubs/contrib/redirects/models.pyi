from django.db import models

class Redirect(models.Model):
    site: models.ForeignKey
    old_path: models.CharField
    new_path: models.CharField
