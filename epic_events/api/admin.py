from django.contrib import admin
from .models import Client, Event, Contract


class ClientAdmin(admin.ModelAdmin):
    """
        Manage Client Admin Django
    """

    list_display = ('name', 'sales_user', 'confirmed')
    list_editable = ('confirmed',)
    list_filter = ('sales_user', 'confirmed')

    search_fields = ('name', 'sales_user_id__username')
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
        Manage Contract Admin Django
    """

    list_display = ('numero_contrats', 'client', 'sales_user_username', 'signed', 'amount', 'payment_due')
    list_editable = ('signed',)
    list_filter = ('client__name', 'signed', 'payment_due')

    @staticmethod
    def numero_contrats(contract):
        return contract

    search_fields = ('id', 'client__name', 'client__sales_user_id__username', 'amount', 'payment_due')
    ordering = ('id',)

    fieldsets = (
        ('Informations', {'fields': ('amount', 'payment_due')}),
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
        Manage Event Admin Django
    """

    list_display = ('numero_contrats', 'event_date', 'societe', 'attendees', 'ended', 'support_user', )
    list_editable = ('ended',)
    list_filter = ('ended', 'support_user', 'event_date')

    search_fields = ('event_date', 'attendees', 'support_user__username', 'contract__client__name', 'contract__id')
    ordering = ('event_date',)

    fieldsets = (
        ('Informations', {'fields': ('contract', 'event_date', 'attendees', 'support_user')}),
        ("Status de l'événement", {'fields': ('ended',)}),
        ("Détail de l'événement", {'fields': ('notes',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('contract', 'event_date', 'attendees', 'ended', 'support_user', 'notes'),
        }),
    )

    @staticmethod
    def numero_contrats(event):
        return event

    @staticmethod
    def societe(event):
        return event.contract.client


admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)
