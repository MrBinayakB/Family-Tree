
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.trees.models import Trees
from .serializers import TreeSerializer
#from .filters import TaskFilter, UserFilter
from django.db.models import Q

@api_view(['GET','POST'])
def tree_list(request, format=None):
    if request.method == 'GET':
        trees = Trees.objects.all()

        filterset = TreeSerializer(request.GET, queryset=tasks)
        if filterset.is_valid():
            tasks = filterset.qs
        
        search = request.GET.get('search')
        if search:
            tasks = trees.filter(Q(completed__icontains=search | Q(groupby__icontains=search)))
        
        serializer = TreeSerializer(trees, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def tree_detail(request, pk, format=None):

    try:
        trees = Trees.objects.get(pk=pk)
    except Trees.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TreeSerializer(trees)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TreeSerializer(trees, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        trees.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)