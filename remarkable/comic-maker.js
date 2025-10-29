const container = document.querySelector(".webcomic .content");
const prevbutton = document.querySelector(".prev");
const randbutton = document.querySelector(".rand");
const nextbutton = document.querySelector(".next");
const prevbutton2 = document.querySelector("#bottomprev");
const randbutton2 = document.querySelector("#bottomrand");
const nextbutton2 = document.querySelector("#bottomnext");
const webcomicImages = '/Assets/webcomic-content/';

const params = new URLSearchParams(window.location.search);
const rawoutput = params.get("num");
let desiredID = parseInt(rawoutput);

const maxComicID = 24;
let currentComicID;

if (isNaN(desiredID) || desiredID < 1 || desiredID > maxComicID) {
    currentComicID = maxComicID;
}
else {
    currentComicID = desiredID;
}

function getFolderID(id) {
    return String(id).padStart(4, "0");
}

function updateButtonStates() {
  prevbutton.disabled = currentComicID === 1;
  nextbutton.disabled = currentComicID === maxComicID;
  prevbutton2.disabled = currentComicID === 1;
  nextbutton2.disabled = currentComicID === maxComicID;
}


loadcomic(currentComicID);


function loadcomic(id) {

    let dirpath = webcomicImages + getFolderID(id);

    let filepath = dirpath + "/title.txt";
    console.log(filepath);
    let titleContainer = document.querySelector(".comictitle");
    fetch(filepath)
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        else {
          history.pushState(null, "", `?num=${id}`);
          updateButtonStates();
        }
        return response.text(); // get the plain text
      })
      .then(text => {
        titleContainer.innerHTML = text; // insert into the page
      })
      .catch(error => {
        titleContainer.innerHTML = `Failed to load title: ${error}`;
      });
    
    let altpath = dirpath + "/alt.txt";
    let comicImage = document.querySelector(".comic");
    fetch(altpath)
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text(); // get the plain text
      })
      .then(text => {
        comicImage.title = text; // insert into the page
        comicImage.src = `${dirpath}/image.png`
      })
      .catch(error => {
        comicImage.innerHTML = `Failed to load alt-text: ${error}`;
      });
}


function go_prev() {
    if (currentComicID === 1) {
        return;
    }
    currentComicID -= 1;
    loadcomic(currentComicID);
}

function get_random_num(min, max) {
    return Math.floor(Math.random() * max) + min;
}

function go_rand() {
    let des = get_random_num(1, maxComicID);
    while (des === currentComicID) {
      des = get_random_num(1, maxComicID);
    }
    currentComicID = des;
    loadcomic(currentComicID);
}

function go_next() {
    if (currentComicID === maxComicID) {
        return;
    }
    currentComicID += 1;
    loadcomic(currentComicID);
}

prevbutton.addEventListener("click", go_prev);
randbutton.addEventListener("click", go_rand);
nextbutton.addEventListener("click", go_next);
prevbutton2.addEventListener("click", go_prev);
randbutton2.addEventListener("click", go_rand);
nextbutton2.addEventListener("click", go_next);
