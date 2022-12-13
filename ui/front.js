"use strict";

let loaded = false

//Api handling

//Normal get functiom
async function getAPI(url) {
  const result = await fetch(`http://127.0.0.1:3000/${url}`, {
    method: "GET",
    credentials: "include",
  });
  return result.json();
}

//Post function
async function postAPI(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(`http://127.0.0.1:3000/${url}`, {
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

function doFly(icao){
  flyImage()
  .then(a=>{
    getAPI(`user/?a=setLocation&val=${a}`)
  })
}

//On cockpit load
//Define event listeners when maps has finished loading to avoid errors
function addHandlers(){
  const cockpit = document.querySelector('.cockpit')
  cockpit.addEventListener('load', a=>{

    const tomtom = cockpit.contentDocument.querySelector('svg g#Tomtom')
    const svg = cockpit.contentDocument.querySelector('g')
    
    //svg.querySelector('g').addEventListener('mouseover', a=> console.log('touch'))

    const Center_console = svg.querySelector('#Center_Console')
    const Fuel_Gauge = svg.querySelector('#Fuel_Gauge')

    Center_console.addEventListener('click', a=>{
      closeAll()
      getPlayer()
      .then((data)=>{
        currLoc = data.location.icao
        airportMenu(data)
      })
    })
    
    //Map button
    tomtom.addEventListener('click', a=>{
      closeAll()
      openMap()
    })

  })
}
//last menu
let lastMenu

//Open last menu
//For back button
function openLast(last){
  closeAll()
  if(last=='map') return openMap()
  last[1].nodeName=='span'?openDialog(last[0]):openDialog(last[0], last[1])
}

function openDialog(element, close=document.createElement('span'), back=false){
  lastMenu = [element, close]
  const dialog = document.querySelector('#menu')
  dialog.appendChild(element)
  if(close.nodeName == 'SPAN'){
    close.innerHTML += '&#x2715'
    dialog.prepend(close)
  }
  if(!dialog.open){
    dialog.showModal()
  }
  close.addEventListener('click', a=>{
    dialog.innerHTML = ''
    dialog.close()
    if(back)
      openLast(lastMenu)
  })
  
}

function closeAll(){
  const map = document.querySelector('#dialogMap')
  const menu = document.querySelector('#menu')
  if(map.open) map.close()
  if(menu.open){
    menu.close()
    menu.innerHTML = ''
  }
}

function openMap(){
  getPlayer()
  .then((data)=>currLoc=data.location.icao)
  const dialog = document.querySelector('#dialogMap')
  if(!dialog.open){
    dialog.showModal()
    map.invalidateSize()
  }
  
  dialog.querySelector('span').addEventListener('click', a=>{
    dialog.close()
  })
}

function flyMenu(icao){
  
  let player, fUsage, airport

  const div = document.createElement('div')
  const header = document.createElement('h1')
  const p1 = document.createElement('p')
  const p2 = document.createElement('p')
  const btnDiv = document.createElement('div')
  const btn1 = document.createElement('button')
  const btn2 = document.createElement('button')
  const alert = document.createElement('p')

  btnDiv.appendChild(btn1)
  btnDiv.appendChild(btn2)

  btn1.innerHTML += 'Fly'
  btn2.innerHTML += 'Cancel'


  //Promise helvetti
  //Voi tehä nätimmin, muttä tää on nyt tällai. Seuraavis menuis on nätimpi
  getAPI(`airport/${icao}`)
  .then((data)=>{ 
    airport = data.content
    header.innerHTML+=`Fly to ${data.content.name}?`
    getPlayer()
    .then((data)=>{
      player = data
      p2.innerHTML += `Fuel level: ${Math.round(+data.fuel)} l <br>`
      getAPI(`/airport/${icao}?a=dist&val=${data.location.icao}`)
      .then((data)=>{
        fUsage = data.content
        p2.innerHTML += `Fuel usage: ${Math.round(+data.content)} l`
      })
    })
  })
  
  btn1.addEventListener('click', a=> {
    if(fUsage > player.fuel) alert.innerHTML = 'Not enought fuel!'
    else doFly(airport.icao)
  })
  div.appendChild(header)
  div.appendChild(p1)
  div.appendChild(p2)
  div.appendChild(btnDiv)
  div.appendChild(alert)
  openDialog(div, btn2)
}

function airportMenu(user){

  const div = document.createElement('div')
  const header = document.createElement('h1')
  const info = document.createElement('div')
  info.id = 'left'
  const quest = document.createElement('div')
  const btnDiv = document.createElement('div')
  const btn1 = document.createElement('button')
  const btn2 = document.createElement('button')
  const alert = document.createElement('p')

  header.innerHTML = `Welcome to the ${user.location.name}, ${user.name}!`
  for(let i=0; i<5; i++){
    const row = document.createElement('p')
    switch(i){
      case 1:
        row.innerHTML = `Money: ${user.money} €`
        break;
      case 2:
        row.innerHTML = `Fuel: ${user.fuel}/${user.plane.max_fuel} l`
        break;
      case 3:
        row.innerHTML = `Plane: ${user.plane.name}`
        break;
      case 4:
        row.innerHTML = `Plane health: ${user.health}/${user.plane.max_health}`
        break;
    }
    row.innerHTML += '<br>'
    info.appendChild(row)
  }

  if(user.quests){
    for(i of user.quests){
      const q = document.createElement('div')
      const p = document.createElement('p')
      p.innerHTML = `<bold>${i.title}</bold> <br>`
      p.innerHTML += `${i.desc} <br>`
      p.innerHTML += `Destination ${i.dest.name} [${i.dest.icao}]<br>`
      p.innerHTML += `Reward ${i.reward} €<br>`
    }
  }

  div.appendChild(header)
  div.appendChild(info)
  div.appendChild(quest)

  openDialog(div)
}

//Get objects that are used many times
async function getPlayer(){
  return await getAPI(`user`)
  .then((data)=>{
    if(data.content=='not logged') return 'loggedout'
    return data.content
  })
}

