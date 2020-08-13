//const fetch = require('node-fetch');
async function main()
{
    //get past 5 times at intervals currTime-24hr, currTime-28hr etc.
    let pastTimes = getPastTimes();


    //user zipcode -> lat-long
    let zipcodeInput = document.getElementById("zipcode").value.trim().substring(0,5);
    let latLongArr = await getLatLong(zipcodeInput);
    let lat = latLongArr[0];
    let long = latLongArr[1];
    console.log(latLongArr);



    //do openweather API calls to load the past 5 days of data in 3 hr increments into a JSON
    //format:  https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={YOUR API KEY} 
    let weatherApiKey = 'ef49a66f02393c65eb96e511aa8a7898'; //harish's api key

    let allTemperatures = [];
    for (let i = 0; i < pastTimes.length; i++)
    {
        let time = pastTimes[i];
        let url = `https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=${lat}&lon=${long}&dt=${time}&appid=${weatherApiKey}`;

        let tempsFromThatDay = await performOpenWeatherAPICall(url);
        allTemperatures = allTemperatures.concat(tempsFromThatDay);
    }

    //console.log(allTemperatures.length) //length is 120, thats good because 24 hrs * 5 days



    //load the data into a LocalStorage object to use later in python
    localStorage.setItem("temps",allTemperatures);
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

//returns an array (really a promise) of [lat, long]
async function getLatLong(zip)
{
    //format: https://www.zipcodeapi.com/rest/<api_key>/info.<format>/<zip_code>/<units>
    
    if (!(zip.length == 5 && /^[0-9]+$/.test(zip)))
    {
        alert("Zipcode is not formatted correctly. Make sure it only has 5 digits and matches US Zipcode format.")
        return;
    }

    let applicationApiKey = 'hKzocZfFBzwpJU0NImyynukV7g7RnN3aH8tX2WWc6woz2VJy8ecyYJCr1aQtb0FJ'
    let jsClientKey = 'js-eV2aEpVYlSwidSXUswp6Hvo94QGoBervP9GDDJAG3xowo6hLvrfLzecizuvcsUxs'

    let url = `https://www.zipcodeapi.com/rest/${applicationApiKey}/info.json/${zip}/degrees`

    
    const response = await window.fetch('https://cors-anywhere.herokuapp.com/' + url);
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

async function performOpenWeatherAPICall(url)
{
    const response = await window.fetch('https://cors-anywhere.herokuapp.com/' + url);
    const json   = await response.json();

    //select the 'hourly' section
    const hourly = json["hourly"];

    //return an array of only the temperatures from every hour
    let temperatures = [];
    for (let i = 0; i < hourly.length; i++)
    {
        let currKelvinTemp = hourly[i]["temp"];
        let currFarenTemp = (9/5) * currKelvinTemp - 459.67;

        temperatures.push(currFarenTemp);
    }

    return temperatures;
}

//only for testing purposes
//main()

/*
maybe needed code for handling async methods onClick
element.addEventListener('click', async (e) => {put code here});
*/