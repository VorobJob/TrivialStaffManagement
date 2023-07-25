from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ref_code = models.UUIDField(
        verbose_name="Реферальный код",
        default='00000000-0000-0000-0000-000000000001'
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        app_label = "item"


class Subordination(models.Model):
    subordinate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подчиненный",
        related_name="subordination_subordinate",
    )
    boss = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Босс",
        related_name="subordination_boss"
    )

    def __str__(self):
        return f"{self.subordinate} - {self.boss}"

    class Meta:
        db_table = "subordinations"
        app_label = "item"
