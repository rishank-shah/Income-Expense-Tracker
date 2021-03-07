const line = document.getElementById('line')
const pie = document.getElementById('pie')
let myChart1;
let myChart2;

line.addEventListener('click',()=>{
    myChart1.destroy()
    myChart2.destroy()
    getChartData('line')
})

pie.addEventListener('click',()=>{
    myChart1.destroy()
    myChart2.destroy()
    getChartData('pie')
})

const renderExpenseChart = (data,labels,type)=>{
    var ctx = document.getElementById('myChart').getContext('2d');
    myChart1 = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'This month\'s expenses',
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
                text: "Expenses per category in this month",
            },
        }
    });
}

const renderIncomeChart = (data,labels,type)=>{
    var ctx = document.getElementById('myChart2').getContext('2d');
    myChart2 = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'This month\'s incomes',
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
                text: "Incomes per source in this month",
            },
        }
    });
}

const getChartData = (type) =>{
    fetch('/expense/expense-summary-data')
        .then(res=>res.json())
        .then(results=>{
            const category_data = results.expense_category_data;
            const [labels,data] = [Object.keys(category_data),Object.values(category_data)]
            renderExpenseChart(data,labels,type)
        })
    fetch('/income/income-summary-data')
        .then(res=>res.json())
        .then(results=>{
            const source_data = results.income_source_data;
            const [labels,data] = [Object.keys(source_data),Object.values(source_data)]
            renderIncomeChart(data,labels,type)
        })
}

document.onload = getChartData('line')