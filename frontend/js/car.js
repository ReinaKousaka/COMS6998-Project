const apigClient = apigClientFactory.newClient();


const createCar = async (car) => {
    let params = {};
	let body = car;
    let additionalParams = {};

    try {
        let response = await apigClient.carsPost(params, body, additionalParams);
        alert('Car added successfully!');
        console.log(`Car added successfully: ${response}`);
    } catch (err) {
        alert('Warning: failed to add car!');
        console.log(`failed to add car: ${err}`);
    }
};

const updateCar = async () => {

};

const deleteCar = async() => {

};

const getCar = async () => {
    try {
        let user = sessionStorage.getItem('user');
        if (!user) return;
        console.log(`user is ${user}`);
        let params = {
            'owner': user
        };
        let body = {};
        let additionalParams = {};
    
        let response = await apigClient.carsGet(params, body, additionalParams);
        alert('Car fetch successfully!');
        console.log(`Car fetch successfully:`);
        console.log(response);
        return response.data;
    } catch (err) {
        alert('Warning: failed to fetch car!');
        console.log(`failed to fetch car: ${err}`);
    }
};

const handleGetCarByUser = async () => {
    try {
        const cars = await getCar();

        const $tbody = $('#carmanage-tbody');
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

    } catch (err) {

    }
};

const uploadCarHandler = async () => {
    // TODO: add images
    console.log(`user is ${sessionStorage.getItem('user')}`)
    createCar({
        'brand': $('#FormControlInput0').val(),
        'model': $('#FormControlInput1').val(),
        'year': $('#FormControlInput2').val(),
        'miles': $('#FormControlInput3').val(),
        'description': $('#FormControlInput4').val(),
        'owner': sessionStorage.getItem('user')
    });
};

// get called in car-search.html
const searchCar = async () => {
    try {
        let params = {
            'q': $('#carSearch').val(),
            'user': sessionStorage.getItem('user')
        };
        let body = {};
        let additionalParams = {};

        let response = await apigClient.searchGet(params, body, additionalParams);
        console.log(response)
        if (response.data == 'No car found') {
            alert('No cars found');
            return;
        }

        const $tbody = $('#carsearch-tbody');
        // Iterate through the data array
        $.each(response.data, function (index, item) {
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

        alert('Car searched successfully!');
        console.log(`Car searched successfully: ${response}`);
    } catch (err) {
        alert('Warning: failed to search car!');
        console.log(`failed to search car: ${err}`);
    }
};
