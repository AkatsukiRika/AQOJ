var codeArea = document.getElementById("code");
var language = document.getElementById("language");
var modeDict = {
    "cpp": "text/x-c++src",
    "java": "text/x-java",
    "python3": {
        name: "python",
        version: 3,
        singleLineStringErrors: false
    }
};

var editor = CodeMirror.fromTextArea(codeArea, {
    mode: "text/x-c++src",
    lineNumbers: true,
    indentUnit: 4,
    styleActiveLine: true,
    matchBrackets: true,
    lineWrapping: true,
    theme: "base16-light"
});
editor.setSize('height', '400px');

language.onclick = function() {
    editor.setOption("mode", modeDict[language.value]);
    console.log("mode", modeDict[language.value]);
};

var submitCode = function (problemId) {
    $.ajax({
        url: "/Submitted/" + problemId + "/",
        type: "post",
        dataType: "text",
        data: {
            code: $("#code").text(editor.getValue()).val(),
            language: $("#language").val(),
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        },
        success: function (data) {
            swal({
                title: "Aqours Online Judge",
                text: data,
                icon: "success",
            });
        },
        error: function () {
            swal({
                title: "Error",
                text: "Something went wrong......",
                icon: "error",
            });
        }
    });
};