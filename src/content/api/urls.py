from django.urls import path
from content.api.views import(
	api_detail_content_view,
	api_update_content_view,
	api_delete_content_view,
	api_create_content_view,
	api_is_author_of_content,
	ApiContentListView,
	api_content_of_user_view
)

app_name = 'content'

urlpatterns = [
	path('<slug>/', api_detail_content_view, name="detail"),
	path('<slug>/update', api_update_content_view, name="update"),
	path('<slug>/delete', api_delete_content_view, name="delete"),
	path('create', api_create_content_view, name="create"),
	path('list', ApiContentListView.as_view(), name="list"),
	path('list_content_of_user',api_content_of_user_view , name="list_content_of_user"),
	path('<slug>/is_author', api_is_author_of_content, name="is_author"),
]