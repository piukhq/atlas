from django.db import models


class User(models.Model):
    """
    Barclays users who have opted out of ubiquity
    """
    time_added_to_database = models.DateTimeField(auto_now_add=True, db_index=True, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    ubiquity_join_date = models.DateTimeField(blank=False)
    delete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email
