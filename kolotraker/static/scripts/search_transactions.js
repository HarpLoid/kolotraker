let timer;
const delay = 500;
const search_field = document.querySelector('#search_field');
const search_output = document.querySelector('.search-output');
const no_result = document.querySelector('.noresult');
const transaction_table = document.querySelector('.transaction-table');
const pagination_container = document.querySelector('.pagination-container');
const search_tbody = document.querySelector('.search-body');

search_output.style.display = 'none';

search_field.addEventListener('keyup', (event) => {
  clearTimeout(timer);
  timer = setTimeout(() => {
    const needle = event.target.value;
    if (needle.trim().length > 0) {
      pagination_container.style.display = 'none';
      search_tbody.innerHTML = "";
      fetch('search-transaction', {
        body: JSON.stringify({ needle: needle }),
        method: 'POST',
      })
        .then((res) => res.json())
        .then((data) => {
          console.log('data', data);
          transaction_table.style.display = 'none';
          search_output.style.display = 'block';
          if (data.length === 0) {
            no_result.style.display = "block";
            search_output.style.display = "none";
          } else {
            no_result.style.display = "none";
            data.forEach((item) => {
              search_tbody.innerHTML += `
                <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>`;
            });
          }
        });
    } else {
      search_output.style.display = 'none';
      transaction_table.style.display = 'block';
      pagination_container.style.display = 'block';
    }
  }, delay);
});
