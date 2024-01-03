from django.shortcuts import render
from .models import task
# Create your views here.

def add_task(request):
    if request.method == 'POST':
        party_id_ = request.POST['firmname']
        title_ = request.POST['title']
        content_ = request.POST['content']
        total_payment_ = request.POST['total_payment']

        new_task = task.objects.create(
            party_id_id=party_id_,
            title =title_,
            content = content_,
            total_payment = total_payment_,
        )
        new_task.save()
        print("Task added")
        return redirect('task_view')
    


    return render(request, 'tasks.html')
