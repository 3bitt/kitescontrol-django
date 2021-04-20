const lesson_search_master = document.querySelector('.lesson-search');
const lesson_search_form = document.forms.namedItem('lesson-search-form');
const lesson_search_results = document.querySelector('.lesson-search-results');

const lesson_student = document.getElementById('lesson_student');
const lesson_instructor = document.getElementById('lesson_instructor');
const lesson_date_from = document.getElementById('date_from');
const lesson_date_to = document.getElementById('date_to');
const lesson_is_single = document.getElementById('is_single');
const lesson_is_group = document.getElementById('is_group');

// JS Event delegation - event listener is applied to parent element
// Only when specific button is clicked action is fired

lesson_search_master.addEventListener('click', (e) => {
  if (e.target && e.target.classList.contains('lesson-reset-button')) {
    console.log("reset btn fired");
    lesson_search_form.reset();
  } else if (e.target && e.target.classList.contains('lesson-search-button')){
    console.log("search btn fired");
    e.preventDefault();
    getLessonData();
  } else if (e.target && e.target.classList.contains('lesson-pagination')){
    e.preventDefault();
    console.log("next page btn fired");

    console.log(e.target.id);
    getLessonData(e.target.id)
  }
})


function getLessonData(page=1) {
  axios.get(
    `lesson/`, {
    params: {
      page: page,
      lesson_student: lesson_student.value,
      lesson_instructor: lesson_instructor.value,
      lesson_date_from: lesson_date_from.value,
      lesson_date_to: lesson_date_to.value,
      lesson_is_single: lesson_is_single.checked ? 'True' : 'False',
      lesson_is_group: lesson_is_group.checked ? 'True' : 'False',
    }
  }).then(response => {
    lesson_search_results.innerHTML = response.data
  });
}