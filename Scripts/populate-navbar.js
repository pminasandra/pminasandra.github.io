fetch('/navbar')
.then(response => response.text())
.then(data => {
  document.getElementById('navbar').innerHTML = data;
  const currentPage = window.location.pathname.split('/')[1];
  if (currentPage) {
    document.getElementById(currentPage).classList.add('currentlink');
  } else {
    document.getElementById('home').classList.add('currentlink');
  }
});
