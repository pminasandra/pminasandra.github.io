fetch('/footer')
.then(response => response.text())
.then(data => {
  document.querySelector('footer').innerHTML = data;
});
