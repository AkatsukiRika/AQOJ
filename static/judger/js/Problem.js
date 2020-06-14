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

language.onclick = function() {
    editor.setOption("mode", modeDict[language.value]);
};