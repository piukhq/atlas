from django.db import models


class User(models.Model):
    """
    Barclays users who have opted out of bink
    """
    time_added_to_database = models.DateTimeField(auto_now_add=True, db_index=True, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    opt_out_timestamp = models.DateTimeField(blank=False)
    delete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email
