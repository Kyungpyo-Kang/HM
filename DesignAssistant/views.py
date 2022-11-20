from django.shortcuts import render, redirect
from django.core.files.uploadhandler import InMemoryUploadedFile
from .models import History
from io import BytesIO
from pathlib import Path
from PIL import Image
import os, sys
import torch
import AdaIN
import random

def setseq(request):
    history_list = History.objects.all().order_by('id')
    seq = 1

    for history in history_list:

        if history.id != seq:
            History.objects.filter(id=history.id).update(id=seq)
        
        seq += 1

    return redirect('history')

def initseq(Model):
    num = Model.objects.count()

    if num == 0:
        seq = 1
    else:
        model = Model.objects.last()
        seq = model.id + 1
    
    return seq

# Create your views here.
def main_view(request):
    return render(request, 'index.html')


def transfer_view(request):
    return render(request, 'transfer.html')


def result_view(request):
    
    try:
        preserve_color = request.POST['color_checkbox']
    except:
        preserve_color = '0'
    try:
        is_nature = request.POST['image_type_checkbox']
    except:
        is_nature = '0'

    alpha = request.POST['weight']

    PATH = 'HM/model_made/'
    vgg_path = PATH + 'vgg_normalised.pth'
    decoder_model_nature_path = PATH + 'nature_7_pattern_30.tar'
    decoder_model_pattern_path = PATH + 'pattern_7_pattern_30.tar'

    
    # try except로 input 중 파일을 우선 받고 exception 발생하면 post로 전달받은 이미지 url 이용
    try : 
        content_image = request.FILES['content_image']
    except : 
        content_image = request.POST['content_selected']
    
    try : 
        style_image = request.FILES['style_image']
    except : 
        style_image = request.POST['style_selected']
    
    

    if int(is_nature):
        generated_result = AdaIN.main(vgg_path, decoder_model_nature_path, content_image, style_image, alpha=alpha, interpolation_weights=None, preserve_color = int(preserve_color))

    else:
        generated_result = AdaIN.main(vgg_path, decoder_model_pattern_path, content_image, style_image, alpha=alpha, interpolation_weights=None, preserve_color = int(preserve_color))

    output = generated_result['output_image']
    content_image = generated_result['content_image']
    style_image = generated_result['style_image']


    output_io = BytesIO()
    output.save(output_io, format='JPEG')

    content_io = BytesIO()
    content_image.save(content_io, format='JPEG')

    style_io = BytesIO()
    style_image.save(style_io, format='JPEG')


    final_output = InMemoryUploadedFile(file=output_io,
    field_name="ImageField",
    name='stylized.jpg',
    content_type='image/jpeg',
    size=sys.getsizeof(output_io),
    charset=None)

    final_content_image = InMemoryUploadedFile(file=content_io,
    field_name="ImageField",
    name='content.jpg',
    content_type='image/jpeg',
    size=sys.getsizeof(content_io),
    charset=None)

    final_style_image = InMemoryUploadedFile(file=style_io,
    field_name="ImageField",
    name='style.jpg',
    content_type='image/jpeg',
    size=sys.getsizeof(style_io),
    charset=None)
    
    
    history = History()
    history.id = initseq(History)
    history.content_image = final_content_image
    history.style_image = final_style_image
    history.output_image = final_output
    history.preserve_color = True if int(preserve_color) == 1 else False
    history.nature_pattern = True if int(is_nature) == 1 else False
    history.alpha = alpha
    history.save()
    
    result = History.objects.order_by('-pk')[0]
    
    
    return render(request, 'result.html', {'args':result})

def history_view(request):
    history = History.objects
    return render(request, 'history.html', {'history':history})


def delete_history(request):
    
    check_list = request.GET.getlist('chk')

    history = History.objects.filter(id__in=check_list)
    history.delete()
    
    return redirect('history')


def delete_history(request):
    
    check_list = request.GET.getlist('chk')

    history = History.objects.filter(id__in=check_list)
    history.delete()
    
    return redirect('history')

def delete_history(request):
    
    check_list = request.GET.getlist('chk')

    history = History.objects.filter(id__in=check_list)
    history.delete()
    
    return redirect('history')

###### Static Images Section ######
def get_images(request):

    is_pattern = 0
    print(request.POST)

    try:
        is_pattern = int(request.POST['pattern_image'])
    except:
        pass

    if is_pattern:
        path = './DesignAssistant/static/img/sample_pattern/'
        path_mid = 'sample_pattern/'
    else:
        path = './DesignAssistant/static/img/sample_nature/'
        path_mid = 'sample_nature/'

    images = getImages(path)
    file_names = [i.split('/')[-1] for i in images]
    real_images = ['../static/img/'+path_mid+i for i in file_names]
    
    info: dict = {
        'real_images' : real_images
    }
    

    return render(request, 'transfer.html', {'info' : info})

# 이미지 경로 불러오는 메소드
def getImages(path: str) : 
    image_list: list = os.listdir(path) # 입력된 path 내의 모든 '파일명' 호출 : 출력 예시) ['0.jpg', '1.jpg', ...]
    random_images: list = random.sample(image_list, 30) # 랜덤하게 30개만 추출
    image_path_list: list = getFullPath(path, random_images) # 파일명만 있기 때문에 getFullPath 메소드로 경로 생성
    return image_path_list

# 이미지 경로 생성 메소드
def getFullPath(path: str, image_list: list) : 
    fullPath: list = []

    for image in image_list : 
        temp_path = '%s%s' % (path, image) # 입력된 path에 파일명을 붙여 경로 생성 : 출력 예시) './DesignAssistant/static/img/pattern_images/0.jpg'
        fullPath.append(temp_path)

    return fullPath

###### Static Images Section End ######


