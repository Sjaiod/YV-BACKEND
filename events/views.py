from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Event
from .serializers import EventSerializer
from django.db.models import Q
from rest_framework.permissions import AllowAny

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # Overriding the create method to handle event creation
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Fetch all events, ordered by creation (latest first)
    @action(detail=False, methods=['get'], url_path='latest')
    def getAllEvents(self, request):
        events = Event.objects.all().order_by('-id')  # Ordering by latest
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Search for events by name
    @action(detail=False, methods=['get'], url_path='search')
    def searchEvent(self, request):
        query = request.query_params.get('name', '')
        if query:
            events = Event.objects.filter(Q(name__icontains=query))
            serializer = self.get_serializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)
