from django.db import models


class User(models.Model):
    """
    Barclays users who have opted out of bink
    """
    email = models.EmailField(max_length=100)
    opt_out_timestamp = models.DateTimeField(blank=True)
    time_added_to_database = models.DateTimeField(auto_now_add=True, db_index=True, blank=False)
    delete = models.BooleanField(null=False)

    def __unicode__(self):
        return self.email
