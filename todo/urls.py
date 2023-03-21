from django.urls import path
from .views import (
    TodoListView,
    TodoCreateView,
    # TodoUpdateView,
    # TodoDeleteView,
    delete_todo,
    edit_todo,
)

# from . import views


urlpatterns = [
    path("todo/new/", TodoCreateView.as_view(), name="todo_new"),
    # path("todo/<int:pk>/edit", TodoUpdateView.as_view(), name="todo_edit"),
    # path("todo/<int:pk>/edit", views.TodoUpdateView, name="todo_edit"),
    # the above writing somehow did not work
    # path("todo/<int:pk>/delete", TodoDeleteView.as_view(), name="todo_delete"), ajaxにするためにこれは削除した
    path("delete-todo/", delete_todo, name="delete_todo"),
    path("edit-todo/", edit_todo, name="edit_todo"),
    path("", TodoListView.as_view(), name="home"),
]
