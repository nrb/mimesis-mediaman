from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404

from mimesis.models import MediaAssociation
from exampleapp.models import Something
from exampleapp.forms import SomethingForm


def list(request):
    # Querying each object individually.  Recommended when a view needs media
    # from only one model.
    obj_list = Something.objects.all()
    for obj in obj_list:
        obj.media = MediaAssociation.objects.for_model(obj)
    
    # current version of mimesis doesn't have this
    #obj_list = MediaAssociation.objects.attach_to(Something.objects.all())
         
    return render_to_response(
        'list.html',
        {'list': obj_list},
        context_instance=RequestContext(request)
    )


def edit(request, instance_id=None):
    instance = None
    if instance_id:
        instance = get_object_or_404(Something, id=instance_id)
    if request.method == 'POST':
        print request.POST
        form = SomethingForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            form.attach_mimesis_media()
            return redirect('exampleapp.views.list')
    else:
        form = SomethingForm(instance=instance)
    return render_to_response(
        'exampleform.html',
        {'form': form},
        context_instance=RequestContext(request)
    )
