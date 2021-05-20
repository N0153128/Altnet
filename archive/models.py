from django.db import models


class Archive(models.Model):
    archive_title = models.CharField('Title', max_length=100)
    archive_text = models.TextField('Text', max_length=20000)
    archive_date = models.DateTimeField('Publish date', auto_now=True)
    archive_author = models.CharField('Author', max_length=100)
    CATEGORY = [('Tech', 'Literature', 'Gaming', 'Politics', 'Media', 'Garbage')]

    def __str__(self):
        return self.archive_title