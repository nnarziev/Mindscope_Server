from django.db import models


class Feature(models.Model):
    uid = models.TextField()
    timestamp = models.BigIntegerField(default=0)
    day_num = models.IntegerField(default=0)
    ema_order = models.SmallIntegerField(default=0)
    label = models.SmallIntegerField(default=0)
    feature_set = models.TextField()
    updated_flag = models.BooleanField(default=False)

    class Meta:
        unique_together = (('uid', 'day_num', 'ema_order'),)
