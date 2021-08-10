const toogle_search_buttons = document.querySelectorAll('.toogle-search-button')
const student_search_view = document.querySelector('.student-search')
const lesson_search_view = document.querySelector('.lesson-search')
const rental_search_view = document.querySelector('.rental-search')


toogle_search_buttons.forEach((btn) => {
  btn.addEventListener('click', toogle_button)
})

function toogle_button(click_event) {
  toogle_search_buttons.forEach((btn) => {
    if (btn == click_event.target) {
      btn.classList.remove('btn-outline-primary')
      btn.classList.add('btn-primary')
      toogle_search_view(btn.textContent)
    } else {
      btn.classList.remove('btn-primary')
      btn.classList.add('btn-outline-primary')
    }
  })
}

function toogle_search_view(btn_text_content) {
  switch (btn_text_content) {
    case 'Kursant':
      lesson_search_view.classList.add('not-visible')
      rental_search_view.classList.add('not-visible')
      student_search_view.classList.remove('not-visible')
      break;
    case 'Lekcja':
      student_search_view.classList.add('not-visible')
      rental_search_view.classList.add('not-visible')
      lesson_search_view.classList.remove('not-visible')
      break;
    case 'Rental':
      student_search_view.classList.add('not-visible')
      lesson_search_view.classList.add('not-visible')
      rental_search_view.classList.remove('not-visible')
      break;
    default:
      break;
  }
}