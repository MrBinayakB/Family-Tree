from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.relationship.models import Relation
from .serializers import RelationSerializer
#from .filters import RelationFilter
from django.db.models import Q

@api_view(['GET','POST'])
def relation_list(request, format=None):
    if request.method == 'GET':
        relations = Relation.objects.all()

        filterset = RelationSerializer(request.GET, queryset=relations)
        if filterset.is_valid():
            relations = filterset.qs
        
        search = request.GET.get('search')
        if search:
            relations = relations.filter(Q(completed__icontains=search | Q(groupby__icontains=search)))
        
        serializer = RelationSerializer(relations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = RelationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def relation_detail(request, pk, format=None):

    try:
        relations = Relation.objects.get(pk=pk)
    except Relation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RelationSerializer(relations)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = RelationSerializer(relations, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        relations.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
