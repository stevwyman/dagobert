from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class PingCount(models.Model):
    """
    Model to store a single, cumulative count of pings.
    There should only ever be one instance of this model.
    """
    count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ping Counter"
        verbose_name_plural = "Ping Counters"

    def __str__(self):
        return f"Total Pings: {self.count}"

    @classmethod
    def get_singleton(cls):
        """
        Retrieves the single PingCount instance, creating it if it doesn't exist.
        """
        obj, created = cls.objects.get_or_create(pk=1, defaults={'count': 0})
        return obj

    def increment_and_save(self):
        """
        Increments the count by one and saves the object safely.
        """
        # We use F() to ensure the database update is atomic, preventing race conditions
        # if multiple requests try to increment the count at the same time.
        from django.db.models import F
        PingCount.objects.filter(pk=self.pk).update(count=F('count') + 1)
        # Re-fetch the updated object to reflect the change in this instance
        self.refresh_from_db()
        return self.count