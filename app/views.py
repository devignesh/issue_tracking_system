from django.shortcuts import render
from django.db import models
from django.views import generic, View

# App imports.
from app.models.models import User


# Create your views here
def home(request):
    user = User.objects.get(pk=1)
    print(user.full_name)
    print(user)
    return render(request, 'home.html')


def user(request):
    return render(request, 'user.html')


def projects(request):
    return render(request, 'project.html')


def issues(request):
    return render(request, 'issue.html')


def comments(request):
    return render(request, 'comments.html')


def error_404(request):
        data = {}
        return render(request,'error_404.html', data)

def error_500(request):
        data = {}
        return render(request,'error_500.html', data)

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post_login(request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = User.objects.get(email=username, password=password)
        if not user:
            return HttpResponse(serialize_object(user, True), content_type='application/json')
        return HttpResponse('UNAUTHORIZED', status=401)

class IssueView(View):

    def get(self, request):
        """
        get all the issues
        """
        issue_list = Issue.objects.order_by('-created_at')
        return HttpResponse(serialize_object(issue_list, False), content_type='application/json')
    
    def post(self, request):
        """
        create issue
        """
        if request.content_type == 'application/json':
            body_unicode = request.body.decode('utf-8')
            issue_req = json.loads(body_unicode)
            issue = Issue()
            issue.title = issue_req["title"]
            issue.description = issue_req["description"]
            issue.author = request.user
            issue.assignee_id = issue_req["assignee_id"]
            issue.status = issue_req["status"]
            try:
                issue.save()
            except IntegrityError as e:
                return HttpResponse(e.message, status=500)
            return HttpResponse(serialize_object(issue, True), content_type='application/json')

        return HttpResponse('post issue')


class IssueDetailsView(View):

    def get(self, request, **kwargs):
        issue_id = self.kwargs['issue_id']
        # issue = get_object_or_404(Issue, pk=issue_id)
        try:
            issue = Issue.objects.get(pk=issue_id)
        except (KeyError, Issue.DoesNotExist):
            return HttpResponse('Issue Not found', status=404)

        return HttpResponse(serialize_object(issue, True), content_type='application/json')
    
    def patch(self, request, issue_id):
        issue_id = self.kwargs['issue_id']
        return HttpResponse('patch issue, %d'.format(issue_id))

    def delete(self, request, issue_id):
        issue_id = self.kwargs['issue_id']
        try:
            issue = Issue.objects.get(pk=issue_id)
        except (KeyError, Issue.DoesNotExist):
            return HttpResponse('Issue Not found', status=404)
        # delete
        try:
            issue.delete()
        except IntegrityError as e:
            return HttpResponse(e.message, status=500)

        return HttpResponse('No Content', status=204)

