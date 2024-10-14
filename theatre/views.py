from django.db.models import F, Count
from rest_framework import viewsets

from theatre.models import (
    Play,
    Actor,
    Genre,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
)
from theatre.pagination import OrderPagination
from theatre.serializers import (
    PlaySerializer,
    ActorSerializer,
    GenreSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer, PlayListSerializer, PlayRetrieveSerializer, PerformanceListSerializer,
    PerformanceRetrieveSerializer, ReservationListSerializer
)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("genres", "actors")

        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        elif self.action == "retrieve":
            return PlayRetrieveSerializer

        return PlaySerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()

    def get_queryset(self):
        queryset = self.queryset.select_related("play", "theatre_hall")

        if self.action == "list":
            queryset = (
                queryset
                .prefetch_related("tickets")
                .annotate(
                    tickets_available=(
                        F("theatre_hall__rows") *
                        F("theatre_hall__seats_in_row") -
                        Count("tickets")
                    )
                )
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        elif self.action == "retrieve":
            return PerformanceRetrieveSerializer

        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.prefetch_related("tickets__performance__play", "tickets__performance__theatre_hall")
    serializer_class = ReservationSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
