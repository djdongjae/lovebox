from django.db import models

class Form(models.Model):
    import uuid
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sex = models.CharField(max_length=20)
    mbti = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    fashion_style = models.CharField(max_length=20)
    hobby = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    food = models.CharField(max_length=20)
    character = models.CharField(max_length=20)
    laugh_cause = models.CharField(max_length=20)
    reaction_to_new_experience = models.CharField(max_length=20)
    music_style = models.CharField(max_length=20)
    weather = models.CharField(max_length=20)
    sns_style = models.CharField(max_length=20)
    travel = models.CharField(max_length=20)
    movie_genre = models.CharField(max_length=20)
    cat_or_dog = models.CharField(max_length=20)
    value = models.CharField(max_length=20)
