from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm


# Create your views here.
class TaskListView(ListView):
    model=Todo
    template_name = 'home.html'
    context_object_name = 'work'

class TaskDetailView(DetailView):
    model = Todo
    template_name = 'detail.html'
    context_object_name = 'task1'

class TaskUpdateView(UpdateView):
    model = Todo
    template_name = 'update.html'
    context_object_name = 'task2'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Todo
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

def index(request):
    work = Todo.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')

        task=Todo(name=name,priority=priority,date=date)
        task.save()
    return render(request,'home.html',{'work':work})

# def details(request):
    work=Todo.objects.all()
#     return render(request,"detail.html",{'work':work})

def delete(request,task_id):
    done=Todo.objects.get(id=task_id)
    if request.method=='POST':
        done.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    up=Todo.objects.get(id=id)
    f=TodoForm(request.POST or None, instance=up)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'up':up})