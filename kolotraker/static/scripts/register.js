let timer;
const delay = 2000;

const username_field = document.querySelector('#username_field');
const feedback_username = document.querySelector('.invalid_feedback-username');
const email_field = document.querySelector('#email_field');
const feedback_email = document.querySelector('.invalid_feedback-email');
const username_check = document.querySelector('.checking_user');
const password_toggle = document.querySelector('.show-password-toggle');
const password_field = document.querySelector('#password_field');
const submit = document.querySelector('.submit-btn');

username_field.addEventListener('keyup', (event) => {
  clearTimeout(timer);
  username_field.classList.remove('is-invalid');
  username_field.classList.remove('is-valid');
  feedback_username.style.display = 'none';
  timer = setTimeout(() => {
    const username_value = event.target.value;
    if (username_value.length > 0) {
      fetch('/authentication/validate-username', {
        body: JSON.stringify({ username: username_value }),
        method: 'POST',
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.username_error) {
            submit.disabled = true;
            username_field.classList.add('is-invalid');
            feedback_username.style.display = 'block';
            feedback_username.innerHTML = `<p>${data.username_error}</p>`;
          } else {
            submit.removeAttribute('disabled');
          }
          if (data.username_valid) {
            username_field.classList.add('is-valid');
          }
        });
    }
  }, delay);
});

email_field.addEventListener('keyup', (event) => {
  console.log('listening');
  email_field.classList.remove('is-invalid');
  email_field.classList.remove('is-valid');
  feedback_email.style.display = 'none';
  timer = setTimeout(() => {
    const email_value = event.target.value;
    if (email_value.length > 0) {
      fetch('/authentication/validate-email', {
        body: JSON.stringify({ email: email_value }),
        method: 'POST',
      })
        .then((res) => res.json())
        .then((data) => {
          console.log('data', data);
          if (data.email_error) {
            submit.disabled = true;
            email_field.classList.add('is-invalid');
            feedback_email.style.display = 'block';
            feedback_email.innerHTML = `<p>${data.email_error}</p>`;
          } else {
            submit.removeAttribute('disabled');
          }
          if (data.email_valid) {
            email_field.classList.add('is-valid');
          }
        });
    }
  }, delay);
});

const toggle_input = (event) => {
  if (password_toggle.textContent === 'SHOW') {
    password_toggle.textContent = 'HIDE';
    password_field.setAttribute('type', 'text');
  } else {
    password_toggle.textContent = 'SHOW';
    password_field.setAttribute('type', 'password');
  }
};
password_toggle.addEventListener('click', toggle_input);
