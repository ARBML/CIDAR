function getNextElment() {
    var url = "/api/data";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return JSON.parse(xmlHttp.responseText);
}
getNext()

function getNext() {
    element = getNextElment()
    document.getElementById('inst').value = element['instruction'];
    document.getElementById('inp').value = element['input'];
    document.getElementById('out').value = element['output'];
    document.getElementById('idx').value = element['index'];
    document.getElementById('inst_en').value = element['instruction_en'];
    document.getElementById('inp_en').value = element['input_en'];
    document.getElementById('out_en').value = element['output_en'];
}