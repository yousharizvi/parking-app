for (var i = 0; i < 10; i++) {
    db.parking.insert({ display_name: 'Parking ' + (i + 1), address: 'Address for parking ' + (i + 1) })
}

db.parking.find().toArray().forEach((parking) => {
    for (var i = 0; i < 100; i++) {
        db.parkingslot.insert({
            parking_id: parking._id,
            display_name: 'A'+ (i+1)
        })
    }
})