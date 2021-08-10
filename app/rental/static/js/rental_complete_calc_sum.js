const rental_complete_buttons = document.querySelectorAll('.rental-complete-btn-js');

var CAN_CALCULATE = false;

rental_complete_buttons.forEach((item) => {

  item.addEventListener('click', (event) => {
    const modal_id = event.target.attributes['data-target'].value.substring(1);
    const complete_rent_modal = document.getElementById(modal_id);

    calcRentTimeAndValueOnModalInit(complete_rent_modal);
    watchDateInputChanges(complete_rent_modal);
  })

})

function calcRentTimeAndValueOnModalInit(modal) {
  const rental_start_date = modal.querySelector('.rental-start-date');
  const rental_end_date = modal.querySelector('.rental-end-date');
  const rent_items_quantities = modal.querySelectorAll('.rent-item-quantity');
  const rent_items_prices = modal.querySelectorAll('.rent-item-price');

  const total_rent_time = modal.querySelector('.total-rent-time');
  const total_rent_value = modal.querySelector('.total-rent-value');

  let start_date = new Date(rental_start_date.value);
  let end_date = new Date(rental_end_date.value);

  let rent_prices = Array.from(rent_items_prices).map(
    (item) => { return parseFloat(item.textContent) });
  let rent_quantities = Array.from(rent_items_quantities).map(
    (item) => { return parseFloat(item.textContent) });

  let rent_duration = calcRentDuration(start_date, end_date);
  let rent_value = calcRentValue(rent_prices, rent_quantities, rent_duration);

  total_rent_time.textContent = rent_duration + ' h';
  total_rent_value.textContent = rent_value + ' zł';

}

function calcRentDuration(start_date, end_date) {

  let result = ((end_date - start_date) / (1000 * 60) / 60);
  if (!isNaN(result)) {
    CAN_CALCULATE = true
    return result.toFixed(1)
  } else {
    CAN_CALCULATE = false
    return '---'
  }
}

function calcRentValue(pricesList, quantitiesList, rentDuration) {

  if (CAN_CALCULATE) {
    let sum = 0.0
    for (let i = 0; i < pricesList.length; i++) {
      sum += (pricesList[i] * quantitiesList[i] * rentDuration);
    }
    return sum.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })

  } else {
    return '---'
  }
}

function watchDateInputChanges(modal) {
  const date_inputs = modal.querySelectorAll('.modal-date-input')
  date_inputs.forEach((input) => {

    input.addEventListener('change', (event) => {
      event.preventDefault()
      calcRentTimeAndValueOnModalInit(modal)
    },true)
  })
}

