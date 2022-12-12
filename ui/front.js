'use strict'

async function queryAPI(url){
const result = await fetch(url, {
    method: 'GET',
    credentials: 'include'
  })
  .then((response) => response.json());
  return result
}