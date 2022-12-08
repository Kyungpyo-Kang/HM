##### 개발 환경 #####

Server: Ubuntu 1.18.0
Web framework: django
Web server: nginx

추가적인 라이브러리 정보는 requirements.txt파일을 참고해주세요.


##### GitHub clone 주소 #####
현차 자사 서버 배포전까지 해당 Git repository는 public으로 변경해둘 예정입니다.
Git clone 시 아래 url 사용하면 됩니다.

* Git push 용량 제한 상 Git에 올라간 프로젝트는 static 폴더에
front에 활용된 이미지 및 패턴_자연 샘플데이터만을 포함하고 있습니다.

* 서버 배포시 pattern_images.zip, nature_images.zip 파일은 scp로 전송했습니다.

https://github.com/Kyungpyo-Kang/HM.git



##### 서버 배포 시 변경해야 할 파일 목록 #####
실제 현차 자사 서버에 배포시 아래 파일들을 수정해주셔야 합니다.
(각각의 파일에 주석으로 표시해두었습니다)

/.config/nginx/HM.conf
/.config/uwsgi/HM.ini
/HM/settings.py

* uwsgi는 pip 패키지로 설치가 안되기 때문에 (버전문제) conda로 설치해주었습니다.
-> conda install -c conda-forge uwsgi


* uwsgi, nginx 설치 후 수정이 끝나면 서버에서 아래 명령어를 추가적으로 입력해주었습니다.
-> pip3 install nginx


sudo mkdir -p /var/log/uwsgi/HM

sudo chown -R ubuntu:ubuntu /var/log/uwsgi/HM/

# sudo [가상환경 uwsgi 경로] -i [프로젝트 HM.ini 경로]
sudo /home/ubuntu/anaconda3/envs/myvenv/bin/uwsgi -i /srv/HM/.config/uwsgi/HM.ini
sudo ln -f /srv/HM/.config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service
sudo cp -f /srv/HM/.config/nginx/HM.conf /etc/nginx/sites-available/HM.conf
sudo ln -sf /etc/nginx/sites-available/HM.conf /etc/nginx/sites-enabled/HM.conf


sudo rm /etc/nginx/sites-enabled/default

sudo systemctl daemon-reload
sudo systemctl enable uwsgi
sudo systemctl restart uwsgi nginx



##### 가비아 도메인 #####

주소: www.hyundaids.com
만료일: 2023-11-17

<네임서버>
1차 ns-2033.awsdns-62.co.uk
2차 ns-1393.awsdns-46.org
3차 ns-243.awsdns-30.com
4차 ns-950.awsdns-54.net
















