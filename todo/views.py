from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from datetime import datetime
from django.core import serializers


from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Todo


class TodoListView(ListView):
    model = Todo
    template_name = "home.html"
    context_object_name = "todos"

    def get_queryset(self):
        qs = super().get_queryset()
        # contents of qs: <QuerySet [<Todo: Buy SD Card>, <Todo: Clean Hair>, <Todo: Algongggggg34ed>, <Todo: fadfadf>, <Todo: Go to college>]>
        sort_by = self.request.GET.get("sort")
        # print(self.request) #output <WSGIRequest: GET '/?sort=due'>
        # print(self.request.GET) #output <QueryDict: {'sort': ['due']}>

        if sort_by == "due":
            qs = qs.order_by("due")
            # print(qs)#<QuerySet [<Todo: fadfadf>, <Todo: Buy SD Card>, <Todo: Go to college>, <Todo: Clean Hair>, <Todo: Algongggggg34ed>]>
        return qs

    def get(self, request, *args, **kwargs):
        if request.is_ajax():

            self.object_list = self.get_queryset()
            context = self.get_context_data()
            # print(context)
            # {'paginator': None, 'page_obj': None, 'is_paginated': False, 'object_list': <QuerySet [<Todo: fadfadf>, <Todo: Buy SD Card>, <Todo: Go to college>, <Todo: Clean Hair>, <Todo: Algongggggg34ed>]>, 'todos': <QuerySet [<Todo: fadfadf>, <Todo: Buy SD Card>, <Todo: Go to college>, <Todo: Clean Hair>, <Todo: Algongggggg34ed>]>, 'view': <todo.views.TodoListView object at 0x1068fb0d0>}
            # print(render(request, self.template_name, context)) #output <HttpResponse status_code=200, "text/html; charset=utf-8">    [23/Apr/2023 03:18:37] "GET /?sort=due HTTP/1.1" 200 18694

            # return render(request, self.template_name, context) #これだと返されるものがhtmlの内容だった(dataに入るみたいな)
            todos = serializers.serialize("json", context[self.context_object_name])
            # print(todos)
            # [{"model": "todo.todo", "pk": 2, "fields": {"body": "Buy SD Card", "due": "2023-08-16", "status": "not-started"}}, {"model": "todo.todo", "pk": 26, "fields": {"body": "Go to college", "due": "2023-08-30", "status": "in-progress"}}, {"model": "todo.todo", "pk": 16, "fields": {"body": "Clean Hair", "due": "2023-08-31", "status": "not-started"}}, {"model": "todo.todo", "pk": 18, "fields": {"body": "Algongggggg34ed", "due": "2023-09-20", "status": "not-started"}}]

            return JsonResponse({"success": True, "todos": todos})

        else:
            return super().get(request, *args, **kwargs)


class TodoCreateView(CreateView):
    model = Todo
    template_name = "todo_new.html"
    fields = ["body", "status", "due"]


# ajaxでやっているため下は現在不要

# class TodoUpdateView(UpdateView):
#     model = Todo
#     template_name = "todo_edit.html"
#     fields = ["body", "due"]


# class TodoDeleteView(DeleteView):
#     model = Todo
#     template_name = "todo_delete.html"
# Only delete needs this. The other is affected by get_absolute_url in model.py. what is the difference between reverse()
# success_url = reverse_lazy("home")


@csrf_exempt
def delete_todo(request):
    if request.method == "POST":
        todo_id = request.POST["todo_id"]
        try:
            todo = Todo.objects.get(pk=todo_id)
            todo.delete()
            return JsonResponse({"success": True})
        except Todo.DoesNotExist:
            return JsonResponse({"success": False})


@csrf_protect
def edit_todo(request):

    if request.method == "POST":
        todo_id = request.POST["todo_id"]
        # todo_id = request.POST.get('todo_id') this is same(to get info from dictionary using key)
        todo_body = request.POST["todo_body"]
        todo_status = request.POST["todo_status"]
        todo_due_b4conv = request.POST["todo_due"]
        todo_due = datetime.strptime(todo_due_b4conv, "%Y-%m-%d").strftime("%Y-%m-%d")

        # if "." in todo_due_b4conv:
        #     todo_due = datetime.strptime(todo_due_b4conv, "%b. %d, %Y").strftime(
        #         "%Y-%m-%d"
        #     )
        # else:
        #     todo_due = datetime.strptime(todo_due_b4conv, "%B %d, %Y").strftime(
        #         "%Y-%m-%d"
        #     )

        # todo_due = datetime.strptime(request.POST["todo_due"], "%b. %d, %Y").strftime(
        #     "%Y-%m-%d"
        # )

        try:
            todo = Todo.objects.get(pk=todo_id)
            todo.body = todo_body
            todo.status = todo_status
            todo.due = todo_due
            todo.save()
            return JsonResponse({"success": True})

        except Todo.DoesNotExist:
            return JsonResponse({"success": False})


# success_url 属性は、ビューが操作を正常に完了した後にユーザーを特定の URL にリダイレクトするために使用されます。たとえば、Todo オブジェクトを作成または更新した後は、ユーザーをすべての Todo オブジェクトのリストにリダイレクトするのが理にかなっていますが、Todo オブジェクトを削除した後は、ユーザーをホームページにリダイレクトするのが理にかなっている場合があります。
# TodoDeleteViewの場合、オブジェクトを削除した後、DeleteView はユーザーをどこにも自動的にリダイレクトしないため、success_url 属性が必要です。デフォルトでは、テンプレートをレンダリングして削除を確認しますが、どこにもリダイレクトしません。したがって、success_url 属性を指定して、オブジェクトが削除された後にユーザーをリダイレクトする場所を Django に伝える必要があります。
# 一方、TodoCreateView と TodoUpdateView は success_url 属性を必要としません。これは、デフォルトで、Todo モデルの get_absolute_url() メソッドによって決定される、新しく作成/更新されたオブジェクトの詳細ビューにユーザーをリダイレクトするためです。つまり、Todo オブジェクトを作成または更新した後、Django は get_absolute_url() メソッドに基づいて、ユーザーをリダイレクトする場所を自動的に認識します。したがって、これらのビューで success_url 属性を指定する必要はありません。 Todo モデルの get_absolute_url() メソッドは、Todo オブジェクトの詳細ビューの URL を決定するために使用されます。これは通常、単一の Todo オブジェクトに関する情報を表示するために使用されます。


# DeleteViewを使用してオブジェクトが削除された後は、get_absolute_url() を使用してリダイレクト URL を決定することはできません。その理由は、新しく作成/更新されたオブジェクトの詳細ビューに自動的にリダイレクトする CreateView および UpdateView とは異なり、DeleteView はオブジェクトの削除後にオブジェクトの詳細ビューまたはその他のビューに自動的にリダイレクトしないためです。
# したがって、DeleteView を使用してオブジェクトを削除した後にリダイレクト URL を指定するには、success_url 属性を使用する必要があります。これは、オブジェクトが削除された後にユーザーをリダイレクトする場所を Django に指示します。


# reverse() と reverse_lazy() は両方とも、URL を逆にするために使用される Django 関数です。これは、URL パターン名または URL パターン ビューを対応する URL に変換することを意味します。
# 2 つの関数の主な違いは、reverse() は積極的に評価される関数であるのに対し、reverse_lazy() は遅延的に評価される関数であることです。
# reverse() はすぐに評価され、反転された URL を文字列として返します。reverse_lazy() は、要求に応じて反転された URL を返すために使用できる遅延評価されたオブジェクトを返します。
# 実際には、これは、たとえば、ビュー、ミドルウェア、およびモデルで URL の反転をすぐに実行できる場合に、reverse() を使用する必要があることを意味します。一方、reverse_lazy() は、URL の設定など、URL の反転をすぐに実行できない場合に使用する必要があります。これは、その時点で Django が URL を解決するために必要なモジュールのロードを完了していない可能性があるためです。
# したがって、アプリケーションの最上位 (urls.py など) にインポートされたモジュール内の URL を反転する必要がある場合は、reverse_lazy() を使用する必要があります。それ以外の場合、リクエスト/レスポンス サイクル中に呼び出される関数またはメソッド内で URL を逆にする必要がある場合は、reverse() を使用できます。
