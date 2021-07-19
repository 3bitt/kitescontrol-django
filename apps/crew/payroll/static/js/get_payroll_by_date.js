const trigger_calc_btn = document.getElementById('trig_payroll_calc');
const payroll_req_url = document.getElementById('payroll-by-date-form').action;
const result_dump_target = document.querySelector('.instructor_payrolls');


trigger_calc_btn.addEventListener('click', getPayroll)

function getPayroll(clickEvent){

  clickEvent.preventDefault()
  var date_from_input = document.getElementById('date_from').value;
  var date_to_input = document.getElementById('date_to').value;

  if (date_from_input && date_to_input){
    fetchData(date_from_input, date_to_input)
  } else {
    return
  }
}

function fetchData(dateFrom, dateTo) {
  axios.get(payroll_req_url, {
    params: {
      dateFrom: dateFrom,
      dateTo: dateTo,
    }
  }).then(response => {
      removeAllChildNodes(result_dump_target);
      result_dump_target.innerHTML = response.data
    });
}

function removeAllChildNodes(parent){
  while (parent.firstChild){
    parent.removeChild(parent.firstChild);
  }
}

