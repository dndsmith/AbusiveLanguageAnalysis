let openTag = "<h2>";
let closeTag = "</h2>";


function changeIt() {  
  var textarea = document.getElementById("myTextarea");
  document.getElementById('test').innerHTML=openTag + textarea.value + closeTag;
}

function clicky(){ document.getElementById('mybutton').click();
}

window.onload = function() {
		var fileInput = document.getElementById('fileInput');
		var fileDisplayArea = document.getElementById('fileDisplayArea');

		fileInput.addEventListener('change', function(e) {
			var file = fileInput.files[0];
			var textType = /text.*/;

			if (file.type.match(textType)) {
				var reader = new FileReader();

				reader.onload = function(e) {
          document.getElementById('test').innerHTML=openTag + reader.result + closeTag;
				}
        

				reader.readAsText(file);	
			} else {
				fileDisplayArea.innerText = "File not supported!"
			}
		});
};
