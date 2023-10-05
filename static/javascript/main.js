
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

function getContributionsBy(name) {
    $.ajax({
        type: 'POST',
        url: "/api/getCon",
        data: {'Reviewed by': name}, //How can I preview this?
        dataType: 'json',
        success: function(d){
            document.getElementById('num_cont').innerHTML = 'Number of Contributions: '+ d.num_cont;
        }
      });
}

function getContributionsNames() {
    var url = "/api/getConNames";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return JSON.parse(xmlHttp.responseText);
}

function setUpBarGraph(){
    // Initialize the echarts instance based on the prepared dom
    var myChart = echarts.init(document.getElementById('main'));
    var contributers = getContributionsNames()
    // Specify the configuration items and data for the chart
    var source = []
    for (var key in contributers){
        source.push([key, contributers[key]])
      }
    console.log(source)
    var option = {
        dataset: [
            {
             dimensions: ['name', 'contributers'],
              source: source
            },
            {
                transform: [
                    {
                      type: 'sort',
                      config: { dimension: 'contributers', order: 'desc' }
                    }
                  ]
                }
          ],
      title: {
        text: ''
      },
      tooltip: {},
      legend: {
        data: ['Contributers']
      },
      xAxis: {
        type: 'category'
      },
      yAxis: {},
      series: [
        {
          name: 'Contributers',
          type: 'bar',
          itemStyle: { 
            // HERE IS THE IMPORTANT PART
            color: "rgba(13,202,240,1)"
          },
          datasetIndex: 1
        }
      ]
    };

    myChart.setOption(option);
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
    document.getElementById('Reviewed by').value = curr_reviewer
    console.log("Current Reviewer", curr_reviewer)

    if (is_explore_page){
        setUpBarGraph();
    }
}

$(".edittable").on('change', function () {
    changed = true
});

$(".changed").on('change', function () {
    curr_reviewer = this.value
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
    num_cont += 1
    document.getElementById('num_rem').innerHTML = 'Number of Contributions: '+ num_cont;

}

is_explore_page = window.location.pathname == '/explore'
if (is_explore_page) {
    $('#btnSubmit').hide();
}

$(document).on('submit','#theForm',function(e)
    {
      e.preventDefault();
      $.ajax({
        type:'POST',
        url:'/api/submit',
        data:$('form').serialize(),
        success:function()
        {
            getNext();
            getContributionsBy(curr_reviewer)
            
        }
      })
    });

num_cont = 0
curr_reviewer = ""
changed = true
getNext()
