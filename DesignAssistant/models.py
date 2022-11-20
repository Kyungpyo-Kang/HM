from django.db import models
import os, random, sys, time, datetime
os.environ['TZ'] = 'Asia/Seoul'


class History(models.Model):
    id = models.IntegerField(primary_key=True)
    content_image = models.ImageField(upload_to='history_images/content')
    style_image = models.ImageField(upload_to='history_images/style')
    output_image = models.ImageField(upload_to='history_images/output')
    preserve_color = models.BooleanField(default = True)
    nature_pattern = models.BooleanField(default = True)
    alpha = models.FloatField(default = 1)
    upload_time = models.DateTimeField(default = datetime.datetime.now())

    def delete_files(self):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.content_image.path))
        os.remove(os.path.join(settings.MEDIA_ROOT, self.style_image.path))
        os.remove(os.path.join(settings.MEDIA_ROOT, self.output_image.path))

    def delete(self, *args, **kwargs):
        super(History, self).delete(*args, **kwargs)
        