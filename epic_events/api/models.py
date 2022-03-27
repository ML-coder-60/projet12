from django.db import models
from django.core.validators import RegexValidator
from authentication.models import User


class Client(models.Model):

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    name = models.CharField(
        max_length=250,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Societé'
    )

    sales_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={
            "team": "Commercial",
            "is_active": True
        },
        verbose_name="Contact commercial"
    )
    email = models.EmailField(
        max_length=320,
        blank=False,
        unique=True,
        null=False,
        verbose_name='Adresse électronique'
    )
    last_name = models.CharField(max_length=25, blank=False, null=False, verbose_name='Nom')
    first_name = models.CharField(max_length=25, blank=False, null=False, verbose_name='Prénom')
    phone = models.CharField(
        validators=[phone_regex],
        max_length=20,
        blank=True,
        verbose_name='Numéro de téléphone'
    )
    mobile = models.CharField(
        validators=[phone_regex],
        max_length=20,
        blank=True,
        verbose_name='Numéro de téléphone portable'
    )
    confirmed = models.BooleanField(blank=False, null=False, verbose_name='Client confirmé')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')

    def __str__(self):
        return f'{self.name}'

    def sales_user_username(self):
        return f'{self.sales_user.username}'


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
        related_name='contract',
        verbose_name='Societé'
    )

    signed = models.BooleanField(blank=False, null=False, verbose_name="Le contrat est signée")
    amount = models.FloatField(blank=False, null=False, verbose_name="Montant de la prestation")
    payment_due = models.DateField(blank=False, null=False, verbose_name="Date de facturation")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')

    def __str__(self):
        return f'{self.id}'

    def client_name(self):
        return f'{self.client.name}'

    def sales_user_id(self):
        return f'{self.client.sales_user_id}'

    def sales_user_username(self):
        return f'{self.client.sales_user}'

    sales_user_username.short_description = "Contact Commercial"


class Event(models.Model):
    contract = models.OneToOneField(
        to=Contract,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='event',
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
    attendees = models.PositiveIntegerField(blank=True, null=True, verbose_name="Nombre de participants")
    event_date = models.DateField(blank=True, null=True, verbose_name="Date de l'événement")
    notes = models.TextField(blank=True, null=True, verbose_name='Description', max_length=2048)
    ended = models.BooleanField(default=False, verbose_name='Evenement terminé')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')

    def __str__(self):
        return f"{self.contract}"

    def client_name(self):
        return f"{self.contract.client.name}"

    def client_id(self):
        return f"{self.contract.client_id}"

    def support_user_username(self):
        return f"{self.support_user.username}"
