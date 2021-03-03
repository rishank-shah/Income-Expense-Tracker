from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime

class Category(models.Model):
	user = models.ForeignKey(to = User,on_delete=models.CASCADE)
	name = models.CharField(max_length = 256)
	created_at = models.DateTimeField(default=localtime)

	def __str__(self):
		return str(self.user) + self.name

	class Meta:
		verbose_name_plural = 'Categories'

class Expense(models.Model):
	user = models.ForeignKey(to = User,on_delete=models.CASCADE)
	amount = models.FloatField()
	date = models.DateField(default = localtime)
	description = models.TextField()
	category = models.ForeignKey(to=Category,on_delete=models.CASCADE)

	def __str__(self):
		return str(self.category) + str(self.date )+ str(self.amount)

	class Meta:
		ordering:['-date']
