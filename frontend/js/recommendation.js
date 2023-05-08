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
        }
    ];
    if (!user) {
        // TODO:
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
