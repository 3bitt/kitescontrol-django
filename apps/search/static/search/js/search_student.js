const student_search_master = document.querySelector('.student-search');
const student_search_form = document.forms.namedItem('student-search-form');
const student_search_results = document.querySelector('.student-search-results');

const student_name = document.getElementById('name');
const student_mobile = document.getElementById('mobile');
const student_weight_gt = document.getElementById('weight_gt');
const student_weight_le = document.getElementById('weight_le');
const student_kite_trip = document.getElementById('kite_trip');
const student_own_car = document.getElementById('own_car');
const student_available_from = document.getElementById('available_from');
const student_available_to = document.getElementById('available_to');
const student_available_now = document.getElementById('available_now_flag');


student_search_master.addEventListener('click', (e) => {
  if (e.target && e.target.classList.contains('student-reset-button')) {
    student_search_form.reset();
  } else if (e.target && e.target.classList.contains('student-search-button')) {
    e.preventDefault();
    geStudenttData();
  } else if (e.target && e.target.classList.contains('student-pagination')) {
    e.preventDefault();
    geStudenttData(e.target.id)
  }
})

function geStudenttData(page=1){
  axios.get(
    'student/', {
      params: {
        page: page,
        name: student_name.value,
        mobile: student_mobile.value,
        weight_gt: student_weight_gt.value,
        weight_le: student_weight_le.value,
        kite_trip: student_kite_trip.checked ? 'True' : 'False',
        own_car: student_own_car.checked ? 'True' : 'False',
        available_from: student_available_from.value,
        available_to: student_available_to.value,
        student_available_now: student_available_now.checked ? 'True' : 'False'
      }
    }).then(response => {
      student_search_results.innerHTML = response.data
  });
}