from django.db import models
from django.utils.html import format_html


class User(models.Model):
    """
    Barclays users who have opted out of ubiquity
    """
    time_added_to_database = models.DateTimeField(auto_now_add=True, db_index=True, blank=False,
                                                  verbose_name=format_html(
                                                      "Opt out timestamp <br> Time added to database"))
    email = models.EmailField(max_length=100, blank=False)
    ubiquity_join_date = models.DateTimeField(blank=False)
    delete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email
