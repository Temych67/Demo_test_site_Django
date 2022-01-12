from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter


from data_app.models import DataModels
from data_app.api.serializers import DataPostSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_blog_view(request, slug):
    try:
        blog_post = DataModels.objects.get(slug=slug)
    except DataModels.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DataPostSerializer(blog_post)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_blog_view(request, slug):
    try:
        blog_post = DataModels.objects.get(slug=slug)
    except DataModels.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({'response': 'You don`t have permission to edit that.'})

    if request.method == 'PUT':
        serializer = DataPostSerializer(blog_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data[SUCCESS] = UPDATE_SUCCESS
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_blog_view(request, slug):
    try:
        blog_post = DataModels.objects.get(slug=slug)
    except DataModels.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({'response': 'You don`t have permission to delete that.'})

    if request.method == 'DELETE':
        operation = blog_post.delete()
        data = {}
        if operation:
            data[SUCCESS] = DELETE_SUCCESS
        return Response(data=data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_create_blog_view(request):
    User_Custom_Model = request.user

    blog_post = DataModels(author=User_Custom_Model)

    if request.method == 'POST':
        serializer = DataPostSerializer(blog_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiBlogListView(ListAPIView):
    queryset = DataModels.objects.all()
    serializer_class = DataPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'body', 'author__username')
