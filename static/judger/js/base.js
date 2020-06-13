function parseTitle(string) {
    var reg = /[A-Z][a-z]*/g;
    strings = string.match(reg);
    result = ""
    for (let i = 0; i < strings.length; i++) {
        if (i != strings.length - 1) result += strings[i].toLowerCase() + "-";
        else result += strings[i].toLowerCase();
    }
    return result;
}

var title = document.getElementsByTagName("title");
var section = title[0].text.trim().split(" - ")[1];
var navString = "nav-" + parseTitle(section);
var navLi = document.getElementsByClassName(navString);
navLi[0].className += " active";