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
            'q': $('#carSearch').val()
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
