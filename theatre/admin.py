from django.contrib import admin

from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
    ordering = ("last_name",)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rows", "seats_in_row")


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("id", "play", "theatre_hall", "show_time")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "row", "seat", "performance", "reservation")