from django.contrib import admin
from .models import Client, Event, Contract


class ClientAdmin(admin.ModelAdmin):
    """
        A form for :
            creating new clients.
                Includes required fields:
                  'name',
                  'last_name',
                  'first_name',
                  'email',
            list/set users
                Includes fields:
                  'name',
                  'sales_user'
                  'client_confirmed',
            Filter users by:
                  'name',
                  'confirmed'
    """

    list_display = ('name', 'sales_user', 'confirmed')
    list_filter = ('sales_user', 'confirmed')

    search_fields = ("name",)
    ordering = ("name",)

    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Informations', {'fields': ('email', 'last_name', 'first_name', 'phone', 'mobile',)}),
        ('Status du client', {'fields': ('confirmed',)}),
        ("Contact de l'équipe Commercial", {'fields': ('sales_user',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'sales_user', 'email', 'last_name', 'first_name', 'phone', 'mobile', 'confirmed'),
        }),
    )


class ContractAdmin(admin.ModelAdmin):
    """
        A form for :
            creating new contract.
                Includes required fields:
                  'client',
                  'signed',
                  'amount',
                  'payment_due',
            list/set users
                Includes fields:
                  'Contract_name',
                  'client',
                  'amount',
                  'signed',
                  'payment_due'
            Filter users by:
                  'client',
                  'signed',
                  'payment_due'
    """

    list_display = ('contrat', 'client', 'signed', 'amount', 'payment_due')
    list_filter = ('client', 'signed', 'payment_due')

    @staticmethod
    def contrat(obj):
        return obj

    ordering = ("id",)

    fieldsets = (
        ('Informations', {'fields': ('amount', 'payment_due',)}),
        ('Status du contract', {'fields': ('signed',)}),
        ("Nom du client", {'fields': ('client',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('client', 'signed', 'amount', 'payment_due'),
        }),
    )


class EventAdmin(admin.ModelAdmin):
    """
        A form for :
            creating new Event.
                Includes required fields:
                  'contract',
                  'attendees',
                  'event_date',
                  'notes'
            list/set users
                Includes fields:
                  'client_name',
                  'amount',
                  'signed',
                  'payment_due'
            Filter users by:
                  'signed',
                  'amount',
                  'payment_due'
    """

    list_display = ('contract', 'event_date', 'attendees', 'completed', 'support_user')
    list_filter = ('completed', 'support_user', 'attendees')
    ordering = ("event_date",)

    fieldsets = (
        ('Informations', {'fields': ('contract', 'event_date', 'attendees')}),
        ("Status de l'événement", {'fields': ('completed',)}),
        ("Détail de l'événement", {'fields': ('notes',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('contract', 'client', 'event_date', 'attendees', 'completed', 'support_user', 'notes'),
        }),
    )

    @staticmethod
    def client(obj):
        return str(obj).split('-')[1]


admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)
