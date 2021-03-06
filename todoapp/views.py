import os

from django.core.files import File
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from .models import todoTask, fileModel
from .forms import fileForm
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
from django.db import models
import zipfile
import magic
import shutil



class ToDoView(View):

    def get(self, request):
        items = todoTask.objects.all()
        return render(request, 'todoList.html', {'allItems': items})


class SubmitTask(View):

    def post(self, request):
        newContent = request.POST['content']
        newTask = todoTask(content=newContent)
        newTask.save()
        return HttpResponseRedirect('/home/')


class RemoveTask(View):

    def post(self, request, item_id):
        delItem = todoTask.objects.get(id=item_id)
        delItem.delete()
        return HttpResponseRedirect('/home/')


class Upload(View):

    def post(self, request):

        form = fileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            inputFile = self.request.FILES['mediaFile']
            if (zipfile.is_zipfile(inputFile)):
                self.processZipFile(inputFile)
            else:
                form.save()
        
        files = fileModel.objects.all()
        return render(request, 'uploadPage.html', {'form': form, 'files': files})

    def get(self, request):

        files = fileModel.objects.all()
        return render(request, 'uploadPage.html', {'files': files})

    def processZipFile(self,inFile):

        with zipfile.ZipFile(inFile, 'r') as zipObj:

            zipObj.extractall('zipContents')
        
        for file in os.listdir('zipContents'):

            filename = os.fsdecode(file)
            
            if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png"):

                with open('./zipContents/'+filename,'rb') as f:
                    contents = File(f)
                    fileModel.objects.create(mediaFile = contents)

        shutil.rmtree('zipContents')
                





class RemoveFile(View):

    def post(self, request, item_id):
        delItem = fileModel.objects.get(id=item_id)
        delItem.delete()
        return HttpResponseRedirect('/upload/')

@receiver(models.signals.post_delete, sender=fileModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
     if instance.mediaFile:
          if os.path.isfile(instance.mediaFile.path):
               os.remove(instance.mediaFile.path)
