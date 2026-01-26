
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.users.models import User
from .serializers import UserSerializer
#from .filters import TaskFilter, UserFilter
from django.db.models import Q

@api_view(['GET','POST'])
def user_list(request, format=None):
    if request.method == 'GET':
        users = User.objects.all()

        filterset = UserSerializer(request.GET, queryset=tasks)
        if filterset.is_valid():
            users = filterset.qs
        
        search = request.GET.get('search')
        if search:
            users = users.filter(Q(completed__icontains=search | Q(groupby__icontains=search)))
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def users_detail(request, pk, format=None):

    try:
        users = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(users)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(users, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)