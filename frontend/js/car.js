const apigClient = apigClientFactory.newClient();


const createCar = async (car) => {
    let params = {};
	let body = car;
    let additionalParams = {};

    try {
        let response = await apigClient.carsPost(params, body, additionalParams);
        console.log(`Car added successfully: ${response}`);
    } catch (err) {
        console.error(`failed to add car: ${err}`);
    }
};

const updateCar = async () => {

};

const deleteCar = async() => {

};


const uploadCarHandler = async () => {
    // TODO: add images
    createCar({
        'brand': $('#FormControlInput0').val(),
        'model': $('#FormControlInput1').val(),
        'year': $('#FormControlInput2').val(),
        'miles': $('#FormControlInput3').val(),
        'description': $('#FormControlInput4').val(),
    });
};

// export {createCar, updateCar, deleteCar};