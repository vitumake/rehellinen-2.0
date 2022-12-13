'use strict'

//Normal get functiom
async function getAPI(url){
const result = await fetch(url, {
    method: 'GET',
    credentials: 'include'
  })
  return result.json()
}

//Post function
async function postAPI(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)
  })
  return response.json()
}