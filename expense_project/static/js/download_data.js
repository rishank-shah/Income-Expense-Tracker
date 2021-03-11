const today = document.getElementById('download_by_today')
const week = document.getElementById('download_by_week')
const month = document.getElementById('download_by_month')
const year = document.getElementById('download_by_year')
const name_for_download = document.getElementById('name_for_download')
const download_as_excel_expense =  document.getElementById('download_as_excel_expense')
const download_as_csv_expense =  document.getElementById('download_as_csv_expense')
const download_as_excel_income =  document.getElementById('download_as_excel_income')
const download_as_csv_income =  document.getElementById('download_as_csv_income')

today.addEventListener('click',()=>{
    name_for_download.style.display = 'block';
    name_for_download.innerText = `(Selected : Today )`
    link = download_as_excel_expense.href.split('download-excel')
    download_as_excel_expense.href = link[0] + 'download-excel/today'
    link = download_as_csv_expense.href.split('download-csv')
    download_as_csv_expense.href = link[0] + 'download-csv/today'
    link = download_as_excel_income.href.split('download-excel')
    download_as_excel_income.href = link[0] + 'download-excel/today'
    link = download_as_csv_income.href.split('download-csv')
    download_as_csv_income.href = link[0] + 'download-csv/today'
})
week.addEventListener('click',()=>{
    name_for_download.style.display = 'block';
    name_for_download.innerText = `(Selected : Week )`
    link = download_as_excel_expense.href.split('download-excel')
    download_as_excel_expense.href = link[0] + 'download-excel/week'
    link = download_as_csv_expense.href.split('download-csv')
    download_as_csv_expense.href = link[0] + 'download-csv/week'
    link = download_as_excel_income.href.split('download-excel')
    download_as_excel_income.href = link[0] + 'download-excel/week'
    link = download_as_csv_income.href.split('download-csv')
    download_as_csv_income.href = link[0] + 'download-csv/week'
})
month.addEventListener('click',()=>{
    name_for_download.style.display = 'block';
    name_for_download.innerText = `(Selected : Month )`
    link = download_as_excel_expense.href.split('download-excel')
    download_as_excel_expense.href = link[0] + 'download-excel/month'
    link = download_as_csv_expense.href.split('download-csv')
    download_as_csv_expense.href = link[0] + 'download-csv/month'
    link = download_as_excel_income.href.split('download-excel')
    download_as_excel_income.href = link[0] + 'download-excel/month'
    link = download_as_csv_income.href.split('download-csv')
    download_as_csv_income.href = link[0] + 'download-csv/month'
})
year.addEventListener('click',()=>{
    name_for_download.style.display = 'block';
    name_for_download.innerText = `(Selected : Year )`
    link = download_as_excel_expense.href.split('download-excel')
    download_as_excel_expense.href = link[0] + 'download-excel/year'
    link = download_as_csv_expense.href.split('download-csv')
    download_as_csv_expense.href = link[0] + 'download-csv/year'
    link = download_as_excel_income.href.split('download-excel')
    download_as_excel_income.href = link[0] + 'download-excel/year'
    link = download_as_csv_income.href.split('download-csv')
    download_as_csv_income.href = link[0] + 'download-csv/year'
})