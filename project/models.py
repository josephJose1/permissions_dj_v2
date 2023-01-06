from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse

#signals
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from django.db.models.signals import post_save

class Project(models.Model):

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("project:project_detail", args=[self.slug])

    #add new custom permission from here
    class Meta:
        permissions = [
            ("can_add_new_project", "can add new project"),
            ("dg_view_project", "OLP can view project")
            ]

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Project)
def set_permission(sender, instance, **kwargs):
    assign_perm(
        "dg_view_project", instance.user, instance)             