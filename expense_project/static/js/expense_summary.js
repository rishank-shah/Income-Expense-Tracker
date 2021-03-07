const dough = document.getElementById('dough')
const pie = document.getElementById('pie')
const bar = document.getElementById('bar')
const polarArea = document.getElementById('polarArea')
const today = document.getElementById('today')
const week = document.getElementById('week')
const month = document.getElementById('month')
const year = document.getElementById('year')
let myChart;
let data,labels,type,label_title;

dough.addEventListener('click',()=>{
    myChart.destroy()
    renderChart(data,labels,'doughnut',label_title)
})

pie.addEventListener('click',()=>{
    myChart.destroy()
    renderChart(data,labels,'pie',label_title)
})

bar.addEventListener('click',()=>{
    myChart.destroy()
    renderChart(data,labels,'bar',label_title)
})

polarArea.addEventListener('click',()=>{
    myChart.destroy()
    renderChart(data,labels,'polarArea',label_title)
})

today.addEventListener('click',()=>{
    myChart.destroy()
    getChartData('bar','today')
})

week.addEventListener('click',()=>{
    myChart.destroy()
    getChartData('bar','week')
})

month.addEventListener('click',()=>{
    myChart.destroy()
    getChartData('bar','month')
})

year.addEventListener('click',()=>{
    myChart.destroy()
    getChartData('bar','year')
})

const renderChart = (data,labels,type,label_title)=>{
    var ctx = document.getElementById('myChart').getContext('2d');
    myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label_title,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: label_title,
            },
        }
    });
}

const getChartData = (type,filter_by) =>{
    fetch(`/expense/expense-summary-data?filter=${filter_by}`)
        .then(res=>res.json())
        .then(results=>{
            const category_data = results.expense_category_data;
            label_title = results.label_title
            const [labels_fetch,data_fetch] = [Object.keys(category_data),Object.values(category_data)]
            labels = labels_fetch
            data = data_fetch
            renderChart(data_fetch,labels_fetch,type,label_title)
        })
}

document.onload = getChartData('pie','today')