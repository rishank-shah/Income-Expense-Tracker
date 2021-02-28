from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def user_path(instance, filename):
    return 'profile_pic/{0}-{1}/{2}'.format(instance.user.username ,instance.user.id,filename)

class UserProfile(models.Model):
	user = models.OneToOneField(to = User,on_delete = models.CASCADE)
	currency = models.CharField(max_length = 255,blank=True,null=True)
	profile_pic = models.ImageField(blank=True,upload_to=user_path)

	def __str__(self):
		return str(self.user) + 's' + 'profile' 