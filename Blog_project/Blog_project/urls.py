from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import (
    about,
    profile,
    # UserProfile,
    IndexView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    SearchView,
)

urlpatterns = [
    path('accounts/profile/', profile, name='profile'),
    # path('accounts/<pk>/profile/', UserProfile.as_view(), name='profile'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', IndexView.as_view(), name='index'),
    path('about/', about, name='about'),
    path('blog/', PostListView.as_view(), name='post-list'),
    path('search/', SearchView.as_view(), name='search'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)