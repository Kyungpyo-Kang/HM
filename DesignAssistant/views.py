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
from django.conf import settings

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

    alpha = float(request.POST['weight'])

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
    
    content_image = [i.content_image.path for i in history]
    style_image = [i.style_image.path for i in history]
    output_image = [i.output_image.path for i in history]

    history.delete()


    try:
        for i,j,k in content_image, style_image, output_image:
            os.remove(os.path.join(settings.MEDIA_ROOT, i))
            os.remove(os.path.join(settings.MEDIA_ROOT, j))
            os.remove(os.path.join(settings.MEDIA_ROOT, k))
            
    except:
        pass
    
    
    return redirect('history')



###### Static Images Section ######
def get_images(request):

    pattern_category = ['black_white_patterns','figure_patterns','fractal_patterns',
    'geometric_patterns','hexagon_patterns','line_patterns','patterns']

    nature_category = ['animal_images','animal_skin_images','bee_images','bird_images','butterfly_images',
    'crystal_images','dragonfly_images','eyes_images','flower_images','nature_images','reptile_images',
    'spider_images','tree_images','wave_images']

    is_pattern = 0

    try:
        pattern_cate_idx = int(request.POST['pattern_image'])
        is_pattern = 1
    except:
        nature_cate_idx = int(request.POST['nature_image'])


    if is_pattern:
        path_mid = pattern_category[pattern_cate_idx-1]
        path = './DesignAssistant/static/img/pattern_images_by_keywords/'+path_mid+'/'
        path_last = 'pattern_images_by_keywords/'+path_mid+'/'
    else:
        path_mid = nature_category[nature_cate_idx-1]
        path = './DesignAssistant/static/img/nature_images_by_keywords/'+path_mid+'/'
        path_last = 'nature_images_by_keywords/'+path_mid+'/'

    images = getImages(path)
    file_names = [i.split('/')[-1] for i in images]
    real_images = ['../static/img/'+path_last+i for i in file_names]
    
    real_images = random.sample(real_images, 30)

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


