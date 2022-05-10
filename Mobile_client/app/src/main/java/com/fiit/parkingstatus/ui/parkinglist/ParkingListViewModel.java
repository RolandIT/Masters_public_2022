package com.fiit.parkingstatus.ui.parkinglist;

import androidx.lifecycle.ViewModel;

import java.util.List;

public class ParkingListViewModel extends ViewModel {
    public List<String> getLis_of_parking_lots() {
        return lis_of_parking_lots;
    }

    public void setLis_of_parking_lots(List<String> lis_of_parking_lots) {
        this.lis_of_parking_lots = lis_of_parking_lots;
    }

    // TODO: Implement the ViewModel
    private List<String> lis_of_parking_lots;
}