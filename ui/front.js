"use strict";

//Api handling

//Normal get functiom
async function getAPI(url) {
  const result = await fetch(url, {
    method: "GET",
    credentials: "include",
  });
  return result.json();
}

//Post function
async function postAPI(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: JSON.stringify(data),
  });
  return response.json();
}

async function sleep(tSeconds) {
  return new Promise((resolve) => setTimeout(resolve, tSeconds * 100));
}

async function flyImage() {
  let image = document.getElementById("window-image");

  image.src = "/ui/images/hangarOpening.jpg";
  await sleep(5);
  image.src = "/ui/images/hangarOpen.jpg";
  await sleep(5);
  image.src = "/ui/images/runway.jpg";
  await sleep(10);
  image.src = "/ui/images/sky.jpg";
  await sleep(10);
  image.src = "/ui/images/decent.jpg";
  await sleep(10);
  image.src = "/ui/images/hangarOut.jpg";
  await sleep(10);
  image.src = "/ui/images/hangar.jpg";
}
//On cockpit load
const cockpit = document.querySelector('.cockpit')
cockpit.addEventListener('load', a=>{

  const tomtom = cockpit.contentDocument.querySelector('svg g#Tomtom')
  const svg = cockpit.contentDocument.querySelector('g')
  
  //svg.querySelector('g').addEventListener('mouseover', a=> console.log('touch'))

  const Center_console = svg.querySelector('#Center_Console')

  Center_console.addEventListener('click', a=>{
    console.log('airport')
  })

})

function openDialog(element){
  const dialog = document.querySelector('#menu')
  dialog.appendChild(element)
  dialog.showModal()
  
  dialog.querySelector('span').addEventListener('click', a=>{
    dialog.close()
  })
  
}

function openMap(){
  const dialog = document.querySelector('#dialogMap')
  dialog.showModal()
  
  dialog.querySelector('span').addEventListener('click', a=>{
    dialog.close()
  })
}