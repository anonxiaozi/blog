from django.shortcuts import render, HttpResponse, Http404, redirect
from django.views import View
import json
import os
import uuid
from django.conf import settings
from .forms import EmailForm
from .models import Blog, Label
import markdown
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail

# Create your views here.


class IndexView(View):

    def get(self, request):
        search = request.GET.get('search')
        label = request.GET.get('label')
        if search:
            blog_list = Blog.objects.filter(
                    Q(title__contains=search) |
                    Q(summary__contains=search)
                ).order_by('-create_time')
        else:
            blog_list = Blog.objects.all().order_by('-create_time')
        if label:
            blog_list = blog_list.filter(label__name__contains=label).order_by('-create_time')
        labels = Label.objects.all()
        show_page_num = 5
        paginator = Paginator(blog_list, show_page_num)
        page = request.GET.get('page') or 1
        page = int(page)
        blog_range = paginator.get_page(page)
        page_range = paginator.page_range
        if show_page_num < paginator.num_pages:
            d, r = divmod(show_page_num, 2)
            end_num = (page + d) if (page + d) < paginator.num_pages else paginator.num_pages
            start_num = (end_num - show_page_num) if (end_num - show_page_num) > 0 else 0
            if (end_num - start_num) < show_page_num:
                end_num = start_num + show_page_num
            page_range = page_range[start_num: end_num]

        data = {
            'blogs': blog_range,
            'page_range': page_range,
            'labels': labels,
            'a_label': label,
        }
        if search:
            data['search_data'] = search
        return render(request, 'blog/index.html', data)


class AboutView(View):

    def get(self, request):
        return render(request, 'blog/about.html')


class ContactView(View):

    def get(self, request):
        return render(request, 'blog/contact.html')

    def post(self, request):
        data = EmailForm(request.POST)
        if data.is_valid():
            send_mail(
                'from blog site',
                '[ name: {name} | email: {email} | phone: {phone} ] say: \n\n\n{message}'.format(**data.cleaned_data),
                'bloke_anon@126.com',
                ['bloke_anon@126.com'],
                fail_silently=False,
            )
            result = {'status': 200}
            return HttpResponse(json.dumps(result))
        else:
            error_message = ''
            for key, value in data.errors.items():
                e = '{}: {}'.format(key, value.as_text())
                error_message += e
            result = {'status': 500, 'data': error_message}
            return HttpResponse(json.dumps(result))


class BlogView(View):

    def get(self, request, blog_id):
        blog = Blog.objects.filter(id=blog_id)
        if blog:
            blog = blog[0]
            blog.content = markdown.markdown(
                text=blog.content, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                 'markdown.extensions.toc',
                ])
            blog.background_img = blog.background_img
            return render(request, 'blog/post.html', {'blog': blog})
        else:
            raise Http404()


def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def check_f_suffix(f, check_list):
    f_suffix = os.path.splitext(f)[-1]
    if f_suffix in check_list:
        return True, f_suffix
    else:
        return False, f_suffix


class UploadImgView(View):

    def post(self, request):
        img = request.FILES.get('background_img', None)
        if img:
            accept_suffix = ['.jpg', '.png', '.jpeg']
            signal, f_suffix = check_f_suffix(img.name, accept_suffix)
            if not signal:
                return HttpResponse(json.dumps({'status': 500, 'message': 'Invalid file type.'}))
            background_img_path = os.path.join(settings.MEDIA_ROOT, 'background_img')
            check_dir(background_img_path)
            img_name = str(uuid.uuid1()) + f_suffix
            img_path = os.path.join(background_img_path, img_name)
            with open(img_path, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            return HttpResponse(json.dumps({'status': 200, 'url': settings.MEDIA_URL + 'background_img/' + img_name}))
        else:
            return HttpResponse(json.dumps({'status': 500, 'message': 'No file selected.'}))


class UploadDataView(View):

    def post(self, request):
        f = request.FILES.get('imgFile')
        if f:
            result = self.image_upload(f)
        else:
            result = {'error': 1, 'message': 'Invalid file.'}
        return HttpResponse(json.dumps(result), content_type="application/json")

    def image_upload(self, upload_file):
        accept_suffix = ['.jpg', '.png', '.jpeg']
        f_suffix = os.path.splitext(upload_file.name)[-1]
        if f_suffix not in accept_suffix:
            return {'error': 1, 'message': 'Invalid file type.'}
        f_name = str(uuid.uuid1()) + f_suffix
        store_name = os.path.join(settings.MEDIA_ROOT, f_name)
        with open(store_name, 'wb') as f:
            for chunk in upload_file.chunks():
                f.write(chunk)
        return {'error': 0, 'url': settings.MEDIA_URL + f_name}
