var apigClient = apigClientFactory.newClient();
var user = sessionStorage.getItem('user');

const getRcommendation = async () => {
    try {
        let user = sessionStorage.getItem('user');
        if (!user) return;
        console.log(`user is ${user}`);
        let params = {
            'user': user
        };
        let body = {};
        let additionalParams = {};
    
        let response = await apigClient.recommendationGet(params, body, additionalParams);
        console.log(`Recommendation fetch successfully:`);
        console.log(response);
        return response.data;
    } catch (err) {
        // alert('Warning: failed to fetch Recommendation!');
        console.log(`failed to fetch Recommendation: ${err}`);
    }
};


const handleGetRecommendation = async () => {
    console.log(`handleGetRecommendation called`)
    var cars = [
        {
            "brand": 'Audi',
            "model": 's5',
            "year":	'2020',
            "miles": 500,
            "owner": 'ez2347@columbia.edu'
        },
        {
            "brand": 'Volkswagen',
            "model": 'Passat',
            "year":	'2010',
            "miles": 200000,
            "owner": 'sy3079@columbia.edu'
        },
        {
            "brand": 'Volkswagen',
            "model": 'Golf',
            "year":	'2014',
            "miles": 30000,
            "owner": 'john231@gmail.com'
        },
        {
            "brand": 'Volkswagen',
            "model": 'Jetta',
            "year":	'2017',
            "miles": 74623,
            "owner": 'simingzhang@gmail.com'
        },
        {
            "brand": 'Audi',
            "model": 'Q7',
            "year":	'2019',
            "miles": 2315,
            "owner": 'ezhao19990516@gmail.com'
        },
        {
            "brand": 'Porsche',
            "model": '911',
            "year":	'2023',
            "miles": 100,
            "owner": 'sy3079@columbia.edu'
        },
        {
            "brand": 'Porsche',
            "model": 'Cayenne',
            "year":	'2022',
            "miles": 650,
            "owner": 'sy3079@columbia.edu'
        },
        {
            "brand": 'Benz',
            "model": 'C300',
            "year":	'2010',
            "miles": 23658,
            "owner": 'ez2347@columbia.edu'
        },
        {
            "brand": 'Benz',
            "model": 'S63',
            "year":	'2018',
            "miles": 5532,
            "owner": 'ez2347@columbia.edu'
        },
        {
            "brand": 'Honda',
            "model": 'Civic',
            "year":	'2017',
            "miles": 6740,
            "owner": 'Mary26782@gmail.com'
        },
        {
            "brand": 'Honda',
            "model": 'Accord',
            "year":	'2021',
            "miles": 5861,
            "owner": 'sy3079@columbia.edu'
        }

    ];
    if (!user) {
        // TODO: shuffle
        /* Randomize array in-place using Durstenfeld shuffle algorithm */
        function shuffleArray(array) {
            for (var i = array.length - 1; i > 0; i--) {
                var j = Math.floor(Math.random() * (i + 1));
                var temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }

        shuffleArray(cars);
        cars = cars.slice(0, 5);
    } else {
        try {
            cars = await getRcommendation();
        } catch (err) {

        }
    }
    console.log(cars)
    const $tbody = $('#recommendation-tbody');
    // remove all existing rows
    $("#recommendation-tbody tr").remove();
    // Iterate through the data array
    $.each(cars, function (index, item) {
      const $tr = $('<tr>');
      $('<th>').text(index + 1).appendTo($tr);
      $('<td>').text(item.brand).appendTo($tr);
      $('<td>').text(item.model).appendTo($tr);
      $('<td>').text(item.year).appendTo($tr);
      $('<td>').text(item.miles).appendTo($tr);
      $('<td>').text(item.owner).appendTo($tr);
  
      // Append the table row to the tbody
      $tr.appendTo($tbody);
    });
};
