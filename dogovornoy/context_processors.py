from .models import Task

def task_counter(request):
    context = {}
    if request.user.is_authenticated:
        new_tasks = Task.objects.filter(assigned_to=request.user, completed_at__isnull=True)
        new_tasks_count = new_tasks.count()
        context['new_tasks_count'] = new_tasks_count
        context['new_tasks_list'] = new_tasks
    return context


def add_user_profile(request):
    if request.user.is_authenticated:
        return {'user_profile': request.user.userprofile}
    return {}