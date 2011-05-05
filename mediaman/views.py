from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q, Count

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

from mimesis.models import MediaUpload, MediaAssociation
from taggit.models import Tag
from mediaman.forms import MetadataForm


MEDIA_LIST_LIMIT = 20


def media_selector(request):
    tags = request.GET.get('tags')
    for_model = request.GET.get('model')
    attached_ids = request.GET.get('media')
    
    media_list = MediaUpload.objects.filter(media_type='image')
    if for_model:
        (app_label, model_name) = for_model.split('.')
        ct = ContentType.objects.get(app_label=app_label, model=model_name)
        media_list = media_list.filter(mediaassociation__content_type=ct)
    media_list = media_list.annotate(attachments=Count('mediaassociation'))
    
    attached_media = []
    if attached_ids:
        attached_ids_list = [int(aid) for aid in attached_ids.split(',')]
        attached_dict = MediaUpload.objects.in_bulk(attached_ids_list)
        attached_media = [attached_dict[aid] for aid in attached_ids_list]
    
    return render_to_response('mediaman/media-selector.html', {
        'for_model': for_model,
        'attached_to': 'this',
        'media_type': 'image',
        'media_list': media_list[:MEDIA_LIST_LIMIT],
        'attached_media': attached_media
    }, context_instance=RequestContext(request))


def media_selector_search(request):
    for_model = request.GET.get('model')
    media_type = request.GET.get('mediatype')
    attached_to = request.GET.get('attachedto')
    search_text = request.GET.get('searchtext')
    
    media_list = MediaUpload.objects.all()
    if media_type:
        media_list = media_list.filter(media_type=media_type)
    if for_model and attached_to == 'this':
        (app_label, model_name) = for_model.split('.')
        ct = ContentType.objects.get(app_label=app_label, model=model_name)
        media_list = media_list.filter(mediaassociation__content_type=ct)
    if search_text:
        media_list = media_list.filter(caption__icontains=search_text)
        #Q(tags__name__in=search_text.split())
   
    media_list = media_list.annotate(attachments=Count('mediaassociation'))
    
    return render_to_response(
        'mediaman/list.html',
        {'media_list': media_list[:MEDIA_LIST_LIMIT]},
        RequestContext(request)
    )


@login_required
def media_selector_upload(request):
    if request.FILES:
        media = request.FILES['media']
        media_upload = MediaUpload.objects.create(
            media = media,
            creator = request.user,
            media_type = 'image',
            media_subtype = 'jpeg'
        )
        return render_to_response(
            'mediaman/list-item.html',
            {'media_item': media_upload},
            RequestContext(request)
        )
    media_list = MediaUpload.objects.filter(creator=request.user) \
        .order_by('-created').annotate(attachments=Count('mediaassociation'))
    return render_to_response(
        'mediaman/upload.html',
        {'media_list': media_list[:MEDIA_LIST_LIMIT]},
        context_instance=RequestContext(request)
    )


def media_selector_preview(request, media_id):
    media_item = get_object_or_404(MediaUpload, pk=media_id)
    return render_to_response('mediaman/preview.html', {
        'media_item': media_item
    }, context_instance=RequestContext(request))


@login_required
def media_selector_edit(request, media_id):
    media_item = get_object_or_404(MediaUpload, pk=media_id)
    if media_item.mediaassociation_set.count():
        return HttpResponseBadRequest('Media has already been attached.')
    if request.method == 'POST':
        form = MetadataForm(request.POST, instance=media_item, prefix='mediaman')
        if form.is_valid():
            media_item = form.save()
            return render_to_response('mediaman/list-item.html', {
                'media_item': media_item
            }, context_instance=RequestContext(request))
    else:
        form = MetadataForm(instance=media_item, prefix='mediaman')
    return render_to_response('mediaman/edit.html', {
        'media_item': media_item,
        'form': form
    }, context_instance=RequestContext(request))


def check_tags(request):
    tag_list = request.GET.get('tags')
    if not tag_list:
        return HttpResponse('')
    found_list = Tag.objects.filter(name__in=tag_list.split()).values_list('name', flat=True)
    return HttpResponse(' '.join(found_list), content_type='text/plain')
