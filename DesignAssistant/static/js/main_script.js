function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      var tmp_id = input.id;
      if (tmp_id == "content_image_upload") {
          document.getElementById('uploaded_content_img').src = e.target.result;
          sessionStorage.setItem('content_image', e.target.result); // 세션에 이미지 저장해 새로 로드되어도 업로드된 이미지가 유지되게 함
          document.getElementById('content_image_selected').value = "";
      } else {
          document.getElementById('uploaded_style_img').src = e.target.result;
          sessionStorage.setItem('style_image', e.target.result); // 동일 용도
          document.getElementById('style_image_selected').value = "";
      }
      
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    document.getElementById('uploaded_img_id').src = "";
  }
};

// DB 이미지 선택하면 이미지가 변경되게 하는 메소드
// Content Image를 선택하고 Style Image를 선택하기 위해 DB를 새로 로드하면 새로고침되면서 선택한 Content Image가 사라지기 때문에 세션을 이용해 유지되게 함
function getSource(id) {
image_source = document.getElementById(id).src;

// DB 선택 창은 하나의 div를 공유하기 때문에 선택한 Image 섹션에 따라 출력되는 영역이 변하게 하기 위해 아래 두 변수 생성
is_content = sessionStorage.getItem('is_content');
is_style = sessionStorage.getItem('is_style');

if (is_content == "1") {

  sessionStorage.setItem('content_image', document.getElementById(id).src);
  document.getElementById("uploaded_content_img").src = image_source;
  document.getElementById("content_image_selected").value = image_source;
  document.getElementById("content_image_upload").value = null;

} else if (is_style == "1") {

  sessionStorage.setItem('style_image', document.getElementById(id).src);
  document.getElementById("uploaded_style_img").src = image_source;
  document.getElementById("style_image_selected").value = image_source;
  document.getElementById("style_image_upload").value = null;

}

};

// 체크박스 하나만 선택되게 하는 메소드
function checkOnlyOne(element) {
        
const checkboxes = document.getElementsByName("selected-item");

checkboxes.forEach((cb) => {
    cb.checked = false;
})

element.checked = true;
};

function isContent() {

sessionStorage.setItem('is_content', "1");
sessionStorage.setItem('is_style', "0");

};

function isStyle() {

sessionStorage.setItem('is_style', "1");
sessionStorage.setItem('is_content', "0");

};

function sessionClear() {
  sessionStorage.clear();
}

// 새로고침 시 선택 or 업로드한 이미지가 유지되도록 하는 메소드
window.onload = function() {

var content_null = sessionStorage.getItem('content_image') == null;
var style_null = sessionStorage.getItem('style_image') == null;

console.log(sessionStorage.getItem('content_image'));

if (content_null & style_null) {
  
  document.getElementById("uploaded_content_img").src = '../static/img/front/no_image.jpg';
  document.getElementById("uploaded_style_img").src = '../static/img/front/no_image.jpg';

  console.log(document.getElementById("content_image_selected").value);
  document.getElementById("content_image_selected").value = "";
  document.getElementById("style_image_selected").value = "";

} else if (!content_null & style_null) {

  document.getElementById("uploaded_content_img").src = sessionStorage.getItem('content_image');
  document.getElementById("uploaded_style_img").src = '../static/img/front/no_image.jpg';
  document.getElementById("content_image_selected").value = sessionStorage.getItem('content_image');
  document.getElementById("style_image_selected").value = "";

} else if (content_null & !style_null) {

  document.getElementById("uploaded_content_img").src = '../static/img/front/no_image.jpg';
  document.getElementById("uploaded_style_img").src = sessionStorage.getItem('style_image');
  document.getElementById("content_image_selected").value = "";
  document.getElementById("style_image_selected").value = sessionStorage.getItem('style_image');

} else {

  document.getElementById("uploaded_content_img").src = sessionStorage.getItem('content_image');
  document.getElementById("uploaded_style_img").src = sessionStorage.getItem('style_image');
  document.getElementById("content_image_selected").value = sessionStorage.getItem('content_image');
  document.getElementById("style_image_selected").value = sessionStorage.getItem('style_image');

}

};