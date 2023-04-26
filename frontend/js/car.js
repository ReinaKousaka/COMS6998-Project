

const createCar = async (car) => {
    console.log(car);
};

const updateCar = async () => {

};

const deleteCar = async() => {

};


const uploadCarHandler = async () => {
    createCar({
        'brand': $('#FormControlInput0').val(),
        'model': $('#FormControlInput1').val(),
        'year': $('#FormControlInput2').val(),
        'miles': $('#FormControlInput3').val(),
        'description': $('#FormControlInput4').val(),
    });
};

// export {createCar, updateCar, deleteCar};