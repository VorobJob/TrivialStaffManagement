from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    ref_code = models.UUIDField(verbose_name="Реферальный код")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        app_label = "item"


class Subordination(models.Model):
    # заменить models.CASCADE на models.SET_NULL?
    # заменить models.CASCADE на начальника начальника при удалении models.SET()?
    subordinate = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Подчиненный",
                                    related_name="subordination_subordinate")
    boss = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Босс", related_name="subordination_boss")

    def __str__(self):
        return f"{self.subordinate.username} - {self.boss.username}"

    class Meta:
        db_table = "subordinations"
        app_label = "item"
