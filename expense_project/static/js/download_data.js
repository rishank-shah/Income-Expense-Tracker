const today = document.getElementById('download_by_today')
const week = document.getElementById('download_by_week')
const month = document.getElementById('download_by_month')
const year = document.getElementById('download_by_year')
const name_for_download = document.getElementById('name_for_download')
const download_as_excel_expense =  document.getElementById('download_as_excel_expense')

today.addEventListener('click',()=>{
    name_for_download.style.display = 'block';
    name_for_download.innerText = `(Selected : Today )`
    link = download_as_excel_expense.href.split('download-excel')
    download_as_excel_expense.href = link[0] + 'download-excel/today'
})
week.addEventListener('click',()=>{
    name_for_download.style.display = 'block';
    name_for_download.innerText = `(Selected : Week )`
    link = download_as_excel_expense.href.split('download-excel')
    download_as_excel_expense.href = link[0] + 'download-excel/week'
})
month.addEventListener('click',()=>{
    name_for_download.style.display = 'block';
    name_for_download.innerText = `(Selected : Month )`
    link = download_as_excel_expense.href.split('download-excel')
    download_as_excel_expense.href = link[0] + 'download-excel/month'
})
year.addEventListener('click',()=>{
    name_for_download.style.display = 'block';
    name_for_download.innerText = `(Selected : Year )`
    link = download_as_excel_expense.href.split('download-excel')
    download_as_excel_expense.href = link[0] + 'download-excel/year'
})