async function main()
{
    //get past 5 times at intervals currTime-24hr, currTime-28hr etc.
    let pastTimes = getPastTimes();


    //user zipcode -> lat-long
    let zipcodeInput = "78613";//document.getElementById("zipcode").value().trim().substring(0,5);
    let latLongArr = await getLatLong(zipcodeInput);
    //console.log(latLongArr);



    //do openweather API calls to load the past 5 days of data in 3 hr increments into a JSON
    //format:  https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={YOUR API KEY} 
    let weatherApiKey = 'ef49a66f02393c65eb96e511aa8a7898'; //harish's api key




    //load the JSON into a local file

    //call the python script to execute on the JSON

    //the python script will work on the JSON and predict predictions in another JSON
}

//returns an array of UNIX times for the past 5 days
function getPastTimes()
{
    //get current UNIX time
    let currTime = Math.round((new Date()).getTime() / 1000)
    let dayInSeconds = 24*60*60 //24 hrs * 60 min * 60 sec
    let pastTimes = []

    //get past 5 days from now in UNIX times
    for (let i = 1; i <= 5; i++)
    {
        pastTimes.push(currTime - dayInSeconds*i)
    }

    return pastTimes;
}

async function getAPIResponse(url)
{
    fetch(url)
        .then(response => {
            return response.json()
        })
}

//returns an array (really a promise) of [lat, long]
async function getLatLong(zip)
{
    //format: https://www.zipcodeapi.com/rest/<api_key>/info.<format>/<zip_code>/<units>
    
    if (!(zip.length == 5 && /^[0-9]+$/.test(zip)))
    {
        alert("Zipcode is not formatted correctly. Make sure it only has 5 digits and matches US Zipcode format.")
    }

    let applicationApiKey = 'hKzocZfFBzwpJU0NImyynukV7g7RnN3aH8tX2WWc6woz2VJy8ecyYJCr1aQtb0FJ'
    //let jsClientKey = 'js-eV2aEpVYlSwidSXUswp6Hvo94QGoBervP9GDDJAG3xowo6hLvrfLzecizuvcsUxs'

    let url = `https://www.zipcodeapi.com/rest/${applicationApiKey}/info.json/${zip}/degrees`

    
    const response = await fetch(url);
    const json = await response.json();

    const arr = [json["lat"], json["lng"]];
    return arr;

    /*
    return fetch(url)
        .then(res => res.json())
        .then((response) => {
            let return_arr = [response['lat'], response['lng']]
            return return_arr
        })
        .catch(err => { throw err });
    */
}

const fetch = require('node-fetch')
main()

/*
maybe needed code for handling async methods onClick
element.addEventListener('click', async (e) => {put code here});
*/