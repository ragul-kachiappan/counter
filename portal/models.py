from django.db import models
from django.core.validators import MinValueValidator


class Cube(models.Model):
    name = models.CharField(max_length=200)
    number_of_trees = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.number_of_trees} trees)"

    class Meta:
        ordering = ['-created_at']


class Tree(models.Model):
    STATUS_CHOICES = [
        (0, 'Nil'),
        (1, 'TODO'),
        (2, 'INPROGRESS'),
        (3, 'DOUBT'),
        (4, 'DONE'),
    ]
    
    tree_id = models.PositiveIntegerField()  # Incremental within each cube (001, 002, etc.)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    cube = models.ForeignKey(Cube, on_delete=models.CASCADE, related_name='trees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def representative_name(self):
        return f"Tree {self.tree_id:03d}"

    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def __str__(self):
        return f"{self.representative_name} - {self.status_display}"

    class Meta:
        ordering = ['tree_id']
        unique_together = ['cube', 'tree_id']
