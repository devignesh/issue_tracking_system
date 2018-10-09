from django.views import generic, View
from django.shortcuts import render
from django.http import (
    JsonResponse, 
    HttpResponse, 
    HttpResponseRedirect
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate, 
    login, 
    logout as django_logout
)
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator

# App imports.
from app.models import Commands, Issue, Project, User
from app.views import serialize_object


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        # if isinstance(obj, YourCustomType):
        #     return str(obj)
        return super().default(obj)


class IssueView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        """
        get all the issues
        """
        issue_list = Issue.objects.order_by('-created_at')
        open_issues = Issue.objects.filter(status='O').count()
        closed_issues = Issue.objects.filter(status='C').count()
        
        return render(request, 'issue.html', {
            'issue_list': issue_list,
            'open_issues': open_issues,
            'closed_issues': closed_issues,
            })

    
    @login_required(login_url='/login/')
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

