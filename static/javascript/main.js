
function getNextElment() {
    if (is_explore_page)
        var url = "/api/saved";
    else
        var url = "/api/data";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return JSON.parse(xmlHttp.responseText);
}

function getNext() {
    element = getNextElment()
    document.getElementById('instruction').value = element['instruction'];
    if ('input' in element)
        document.getElementById('input').value = element['input'];
    document.getElementById('output').value = element['output'];
    document.getElementById('instruction_en').value = element['instruction_en'];
    if ('input_en' in element)
        document.getElementById('input_en').value = element['input_en'];
    document.getElementById('output_en').value = element['output_en'];
    if (is_explore_page)
        document.getElementById('num_rem').innerHTML = 'Total: ' + element['num_rem'];
    else
        document.getElementById('num_rem').innerHTML = 'Remaining: ' + element['num_rem'];
    document.getElementById('index_input').value = element['index'];
    document.getElementById('index').innerHTML = 'index: ' + element['index'];
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

is_explore_page = window.location.pathname == '/explore'
if (is_explore_page) {
    $('#btnSubmit').hide();
}
changed = false
getNext()
