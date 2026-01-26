from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.people.models import People
from .serializers import PeopleSerializer
#from .filters import PeopleFilter
from django.db.models import Q

@api_view(['GET','POST'])
def people_list(request, format=None):
    if request.method == 'GET':
        peoples = People.objects.all()

        filterset = PeopleSerializer(request.GET, queryset=peoples)
        if filterset.is_valid():
            peoples = filterset.qs
        
        search = request.GET.get('search')
        if search:
            peoples = peoples.filter(Q(completed__icontains=search | Q(groupby__icontains=search)))
        
        serializer = PeopleSerializer(peoples, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def people_detail(request, pk, format=None):

    try:
        peoples = People.objects.get(pk=pk)
    except People.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PeopleSerializer(peoples)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PeopleSerializer(peoples, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        peoples.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
