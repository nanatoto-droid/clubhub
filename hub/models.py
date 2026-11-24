from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=[
            ('tech', 'Technology'),
            ('arts', 'Arts & Culture'),
            ('academic', 'Academic'),
            ('sports', 'Sports'),
            ('community', 'Community'),
            ('business', 'Business'),
        ],
        default='community',
    )
    description = models.TextField()
    image = models.ImageField(upload_to='clubs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} — {self.club.name}"

    class Meta:
        ordering = ['date']


class JoinRequest(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='join_requests',
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )

    def __str__(self):
        return f"{self.name} → {self.club.name}"

    class Meta:
        ordering = ['-submitted_at']