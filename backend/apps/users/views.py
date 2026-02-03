import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from apps.users.models import User
from .serializers import UserSerializer
#from .filters import TaskFilter, UserFilter
from django.db.models import Q

logger = logging.getLogger("apps.users")
@api_view(['GET','POST'])
def user_list(request, format=None):
    if request.method == 'GET':
        logger.info("GET /users/ requested")

        try:
            users = User.objects.all()
            logger.debug(f"Total users count: {users.count()}")

            search = request.GET.get('search')
            if search:
                logger.info(f"Searching users with keyword: {search}")
                users = users.filter( Q(username__icontains=search) | Q(email__icontains=search))

            serializer = UserSerializer(users, many=True)
            logger.info("User list fetched successfully")
            return Response(serializer.data)

        except Exception:
            logger.error("Error while fetching user list", exc_info=True)
            return Response(
                {"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        logger.info("POST /users/ requested")

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("New user created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Invalid user data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def users_detail(request, pk, format=None):
    
    logger.info(f"Request on /users/{pk}/ with method {request.method}")
    try:
        users = User.objects.get(pk=pk)
    except User.DoesNotExist:
        logger.warning(f"User with id={pk} not found")
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(users)
        logger.info(f"User {pk} fetched successfully")
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(users, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {pk} updated successfully")
            return Response(serializer.data)
        
        logger.warning(f"Update failed for user {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        users.delete()
        logger.info(f"User {pk} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)