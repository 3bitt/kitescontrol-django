const rental_search_master = document.querySelector('.rental-search');
const rental_search_form = document.forms.namedItem('rental-search-form');
const rental_search_results = document.querySelector('.rental-search-results');

const rental_student = document.getElementById('rental_student');
const rental_start_date = document.getElementById('start_date');
const rental_end_date = document.getElementById('end_date');
const rental_created_date = document.getElementById('created_date');
const rental_paid = document.getElementsByName('paid')
const rental_item = document.getElementById('rent_item');

// JS Event delegation - event listener is applied to parent element
// Only when specific button is clicked action is fired

rental_search_master.addEventListener('click', (e) => {
  if (e.target && e.target.classList.contains('rental-reset-button')) {
    rental_search_form.reset();
  } else if (e.target && e.target.classList.contains('rental-search-button')){
    e.preventDefault();
    paid = getRadioSelection(rental_paid)
    getRentalData(page=1, paid);
  } else if (e.target && e.target.classList.contains('rental-pagination')){
    e.preventDefault();
    getRentalData(e.target.id)
  }
})


function getRentalData(page=1, paid) {
  axios.get(
    `rental/`, {
    params: {
      page: page,
      rental_student: rental_student.value,
      rental_start_date: rental_start_date.value,
      rental_end_date: rental_end_date.value,
      rental_created_date: rental_created_date.value,
      rental_paid: paid,
      rental_item: rental_item.value
    }
  }).then(response => {
    rental_search_results.innerHTML = response.data
  });
}


function getRadioSelection(radios){
  for (const rb of radios){
    if (rb.checked){
      return rb.value
    }
  }
}