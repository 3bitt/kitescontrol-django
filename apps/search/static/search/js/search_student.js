const search_button = document.querySelector('.search-button');
const reset_button = document.querySelector('.reset_button');
const student_search_form = document.forms.namedItem('student-search-form');
const student_search_results = document.querySelector('.student-search-results');

const search_name = document.getElementById('name');
const search_mobile = document.getElementById('mobile');
const search_weight_gt = document.getElementById('weight_gt');
const search_weight_le = document.getElementById('weight_le');
const search_kite_trip = document.getElementById('kite_trip');
const search_own_car = document.getElementById('own_car');
const search_available_from = document.getElementById('available_from');
const search_available_to = document.getElementById('available_to');


reset_button.addEventListener('click', (e) => {
  student_search_form.reset()
})

search_button.addEventListener('click', (e) => {
  e.preventDefault();
  getData();
});


function getData(){
  axios.get(
    'student/', {
      params: {
        name: search_name.value,
        mobile: search_mobile.value,
        weight_gt: search_weight_gt.value,
        weight_le: search_weight_le.value,
        kite_trip: search_kite_trip.checked ? 'True' : 'False',
        own_car: search_own_car.checked ? 'True' : 'False',
        available_from: search_available_from.value,
        available_to: search_available_to.value,
      }
    }).then(response => {
      student_search_results.innerHTML = response.data
  });
}