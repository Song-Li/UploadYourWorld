//DOM
const doc = document.querySelector.bind(document);

//APP
let App = {};
App.init = function () {
  //Init
  function handleFileSelect(evt) {
    const files = evt.target.files; // FileList object
    if (files == undefined) {
      files = {"FILE": ""};
    }
    //files template
    let template = `${Object.keys(files).
    map(file => `<div class="file file--${file}">
     <div class="name"><span>${files[file].name}</span></div>
     <div class="progress active"></div>
     <div class="done">
	<a href="" target="_blank">
      <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 1000 1000">
		<g><path id="path" d="M500,10C229.4,10,10,229.4,10,500c0,270.6,219.4,490,490,490c270.6,0,490-219.4,490-490C990,229.4,770.6,10,500,10z M500,967.7C241.7,967.7,32.3,758.3,32.3,500C32.3,241.7,241.7,32.3,500,32.3c258.3,0,467.7,209.4,467.7,467.7C967.7,758.3,758.3,967.7,500,967.7z M748.4,325L448,623.1L301.6,477.9c-4.4-4.3-11.4-4.3-15.8,0c-4.4,4.3-4.4,11.3,0,15.6l151.2,150c0.5,1.3,1.4,2.6,2.5,3.7c4.4,4.3,11.4,4.3,15.8,0l308.9-306.5c4.4-4.3,4.4-11.3,0-15.6C759.8,320.7,752.7,320.7,748.4,325z"</g>
		</svg>
						</a>
     </div>
    </div>`).
    join("")}`;

    if(evt.target.id == "inputFile"){
      file_to_figures();
      doc("#dropFile").classList.add("hidden");
      doc("#fileFooter").classList.add("hasFiles");
      setTimeout(() => {
        doc("#listFiles").innerHTML = template;
      }, 1000);
    } else {
      figures_to_file();
      doc("#dropImg").classList.add("hidden");
      doc("#imgFooter").classList.add("hasFiles");
      setTimeout(() => {
        doc("#listImgs").innerHTML = template;
      }, 1000);
    }


    Object.keys(files).forEach(file => {
      let load = 2000 + file * 2000; // fake load
      setTimeout(() => {
        doc(`.file--${file}`).querySelector(".progress").classList.remove("active");
        doc(`.file--${file}`).querySelector(".done").classList.add("anim");
      }, load);
    });
  }

  // trigger input
  doc("#triggerUploadFile").addEventListener("click", evt => {
    evt.preventDefault();
    doc("input[id='inputFile']").click();
  });

  doc("#triggerUploadImgs").addEventListener("click", evt => {
    evt.preventDefault();
    doc("input[id='inputImg']").click();
  });

  // drop events
  var counter1 = 0;
  doc("#dropImg").ondragleave = evt => {
    evt.stopPropagation();
    counter1--;
    if (counter1 == 0){
      doc("#dropImg").classList.remove("active");
    }
    evt.preventDefault();
  };
  doc("#dropImg").ondragenter = evt => {
    evt.stopPropagation();
    counter1++;
    doc("#dropImg").classList.add("active");
    evt.preventDefault();
  };
  doc("#dropImg").ondragover = evt => {
    evt.preventDefault();
  }
  doc("#dropImg").ondrop = evt => {
    evt.stopPropagation();
    doc("input[id='inputImg']").files = evt.dataTransfer.files;
    doc("#imgFooter").classList.add("hasFiles");
    doc("#dropImg").classList.remove("active");
    counter1 = 0;
    evt.preventDefault();
    figures_to_file();
  };

  var counter2 = 0;
  doc("#dropFile").ondragleave = evt => {
    evt.stopPropagation();
    counter2--;
    if (counter2 == 0){
      doc("#dropFile").classList.remove("active");
    }
    evt.preventDefault();
  };
  doc("#dropFile").ondragover = evt => {
    evt.preventDefault();
  }
  doc("#dropFile").ondragenter = evt => {
    evt.stopPropagation();
    counter2++;
    doc("#dropFile").classList.add("active");
    evt.preventDefault();
  };
  doc("#dropFile").ondrop = evt => {
    evt.stopPropagation();
    doc("input[id='inputFile']").files = evt.dataTransfer.files;
    doc("#fileFooter").classList.add("hasFiles");
    doc("#dropFile").classList.remove("active");
    counter2 = 0;
    evt.preventDefault();
    file_to_figures()
  };

  //upload more
  doc("#downloadImgs").addEventListener("click", () => {
    doc("#listFiles").innerHTML = "";
    doc("#fileFooter").classList.remove("hasFiles");
    doc("#downloadImgs").classList.remove("active");
    setTimeout(() => {
      doc("#dropFile").classList.remove("hidden");
    }, 500);
  });

  doc("#downloadFile").addEventListener("click", () => {
    doc("#listImgs").innerHTML = "";
    doc("#imgFooter").classList.remove("hasFiles");
    doc("#downloadFile").classList.remove("active");
    setTimeout(() => {
      doc("#dropImg").classList.remove("hidden");
    }, 500);
  });

  // input change
  doc("input[id='inputFile']").addEventListener("change", handleFileSelect);
  doc("input[id='inputImg']").addEventListener("change", handleFileSelect);
}();


function file_to_figures() {
  console.log("ENTER")
  console.log($("#uploadfile")[0]);
  var form_data = new FormData($("#uploadfile")[0]);
  $.ajax({
    url: '/upload',
    type: 'POST',
    contentType: false,
    cache: false,
    processData: false,
    data: form_data,
    success: (data) => {
      if(data !== "success") return;
      doc("#downloadImgs").classList.add("active");
    }
  });
  return false;
}

function figures_to_file() {
  console.log("ENTER")
  var form_data = new FormData($('#uploadimg')[0]);
  $.ajax({
    url: '/backtofile',
    type: 'POST',
    contentType: false,
    cache: false,
    processData: false,
    data: form_data,
    success: (data) => {
      if(data !== "success") return;
      doc("#downloadFile").classList.add("active");
    }
  });
  return false;
}

function showFilename(obj) {
  let name = obj.value.split("\\").pop();
  document.getElementById("show-filename").textContent = name;
}
