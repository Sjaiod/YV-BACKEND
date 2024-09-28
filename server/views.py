from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated


class HOmepage(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        return render(request, '../templates/welcome.html')
