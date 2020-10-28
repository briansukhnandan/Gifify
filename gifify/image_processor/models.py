from django.db import models


class VideoFile(models.Model):
    docfile = models.FileField(upload_to='documents/', default='.mp4')
    optional_text = models.CharField(max_length=50, default='PLACEHOLDER', blank=True)
    starting_timestamp = models.IntegerField(blank=False, default=0)
    ending_timestamp = models.IntegerField(blank=False, default=10)
    grayscale_option = models.BooleanField(blank=True, default=False)
    pencil_sketched_option = models.BooleanField(blank=True, default=False)
    flipX_option = models.BooleanField(blank=True, default=False)
    flipY_option = models.BooleanField(blank=True, default=False)