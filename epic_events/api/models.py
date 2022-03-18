from django.db import models

# Create your models here.

from authentication.models import User


class Client(models.Model):

    name = models.CharField(max_length=250, unique=True, null=False, blank=False, verbose_name='Societé')

    sales_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='sales_user',
        limit_choices_to={
            "team": "Commercial",
            "is_active": True
        },
        verbose_name="Contact commercial",
        null=True,
        blank=True
    )
    email = models.EmailField(blank=False, unique=True, null=False, verbose_name='Adresse électronique')
    last_name = models.CharField(max_length=25, blank=False, verbose_name='Nom')
    first_name = models.CharField(max_length=25, blank=False, verbose_name='Prénom')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Numéro de téléphone')
    mobile = models.CharField(max_length=20, blank=True, verbose_name='Numéro de téléphone portable')
    confirmed = models.BooleanField(default=False, verbose_name='Client confirmé')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')

    def __str__(self):
        return self.name


class Contract(models.Model):

    class Meta:
        unique_together = (('client', 'id'),)

    id = models.AutoField(primary_key=True, verbose_name="Numéro de contract")

    client = models.ForeignKey(
        to=Client,
        on_delete=models.PROTECT,
        limit_choices_to={
            "confirmed": True
        },
        related_name='contracts',
        verbose_name='Societé'
    )

    signed = models.BooleanField(default=False, verbose_name="Le contrat est signée")
    amount = models.FloatField(null=True, verbose_name="Montant de la prestation")
    payment_due = models.DateField(null=True, verbose_name="Date de facturation")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')

    def __str__(self):
        return f"{self.id}"+"-"+f"{self.client.name}"


class Event(models.Model):
    contract = models.OneToOneField(
        to=Contract,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='contracts',
        limit_choices_to={
            "signed": True
        },
        verbose_name="Contrat"
    )

    support_user = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        limit_choices_to={
            "team": "Support",
            "is_active": True
        },
        verbose_name='Contact Support',
        null=True,
        blank=True
    )
    attendees = models.PositiveIntegerField(null=True, verbose_name="Nombre de participants")
    event_date = models.DateField(null=True, verbose_name="Date de l'événement")
    notes = models.TextField(blank=False, verbose_name='Description', max_length=2048)
    completed = models.BooleanField(default=False, verbose_name='Evenement terminé')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')

    def __str__(self):
        return f"{self.contract}"
