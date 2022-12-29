from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Item(models.Model):
    class TypeChoices(models.TextChoices):
        HEAD = "머리",
        TOP = "상의",
        BOTTOM = "하의",
        SHOE = "신발",
        WEAPON = "무기"


    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(choices=TypeChoices.choices, max_length=2)
    # level = models.IntegerField(default=1, validators=[
    #     MinValueValidator(1),
    #     MaxValueValidator(999)
    # ])

    def __str__(self):
        return self.name


class Shop(models.Model):
  item = models.ForeignKey("Item", models.CASCADE)
  pay = models.IntegerField(default=0)
  quantity = models.IntegerField(null=True, blank=True) # 생략 가능. 생략하면 무제한 판매 

  def __str__(self):
    return self.item.name


class Character(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey("core.user", models.CASCADE)
  level = models.IntegerField(default=1, validators=[
        MinValueValidator(1),
        MaxValueValidator(999)
    ])
  # hp = models.
  exp = models.IntegerField()

  def __str__(self):
    return self.user.username
