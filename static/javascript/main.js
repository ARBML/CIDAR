function getNextElment() {
    var url = "/api/data";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return JSON.parse(xmlHttp.responseText);
}
getNext()
changed = false

function getNext() {
    element = getNextElment()
    document.getElementById('inst').value = element['instruction'];
    document.getElementById('inp').value = element['input'];
    document.getElementById('out').value = element['output'];
    document.getElementById('idx').value = 'index: ' + element['index'];
    document.getElementById('inst_en').value = element['instruction_en'];
    document.getElementById('inp_en').value = element['input_en'];
    document.getElementById('out_en').value = element['output_en'];
    document.getElementById('num_rem').innerHTML = 'Remaining:' + element['num_rem'];
}

$(".edittable").on('change', function () {
    changed = true
});

function checkChanges() {
    if (!changed) {
        $('#exampleModal').modal('show');
    } else {
        submitForm()
    }
}

function submitForm() {
    document.getElementById('theForm').submit();
}