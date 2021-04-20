const trigger_calc_btn = document.getElementById('trig_payroll_calc')
const payroll_req_url = document.getElementById('payroll-by-date-form').action
const result_dump_target = document.querySelector('.instructor_payrolls')


trigger_calc_btn.addEventListener('click', getPayroll)

function getPayroll(clickEvent){

  clickEvent.preventDefault()
  const dateFrom = document.getElementsByName('dateFrom')[0].value
  const dateTo = document.getElementsByName('dateTo')[0].value

  if (!dateFrom && !dateTo){
    return
  }

  search_params = new URLSearchParams({
    dateFrom: dateFrom,
    dateTo: dateTo,
  })

  fetch(payroll_req_url +'?'+ search_params, {
    method: 'GET',
    headers: {
      "X-Requested-With": "XMLHttpRequest"
    },
  }).then(function(response) {
    return response.json()
  }).then(function(data) {
    removeAllChildNodes(result_dump_target)
    result_dump_target.innerHTML = data.content
  }).catch((error) => {
  })

}

function removeAllChildNodes(parent){
  while (parent.firstChild){
    parent.removeChild(parent.firstChild);
  }
}

