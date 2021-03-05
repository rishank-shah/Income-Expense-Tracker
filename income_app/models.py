from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime

class IncomeSource(models.Model):
	user = models.ForeignKey(to = User,on_delete=models.CASCADE)
	source = models.CharField(max_length = 256)
	created_at = models.DateTimeField(default=localtime)

	def __str__(self):
		return str(self.user) + self.source

	class Meta:
		verbose_name_plural = 'Income Sources'

class Income(models.Model):
	user = models.ForeignKey(to = User,on_delete=models.CASCADE)
	amount = models.FloatField()
	date = models.DateField(default = localtime)
	description = models.TextField()
	source = models.ForeignKey(to=IncomeSource,on_delete=models.CASCADE)
	created_at = models.DateTimeField(default=localtime)

	def __str__(self):
		return str(self.source) + str(self.date )+ str(self.amount)

	class Meta:
		ordering:['-date']