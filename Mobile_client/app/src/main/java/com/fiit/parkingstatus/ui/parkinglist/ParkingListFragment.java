package com.fiit.parkingstatus.ui.parkinglist;

import androidx.lifecycle.ViewModelProvider;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.fiit.parkingstatus.R;
import com.fiit.parkingstatus.utils.FirebaseUtils;
import com.fiit.parkingstatus.utils.PlotsListAdapter;

import java.util.ArrayList;

public class ParkingListFragment extends Fragment implements ListUpdates{

    private ParkingListViewModel mViewModel;
    private RecyclerView recyclerView;
    private RecyclerView.LayoutManager layoutManager;
    private RecyclerView.Adapter mAdapter;

    public static ParkingListFragment newInstance() {
        return new ParkingListFragment();
    }

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        final View rootView = inflater.inflate(R.layout.parking_list_fragment, container, false);
        recyclerView = rootView.findViewById(R.id.plotListRecycler);
        recyclerView.setHasFixedSize(true);

        layoutManager = new LinearLayoutManager(rootView.getContext());
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.setItemAnimator(new DefaultItemAnimator());
        FirebaseUtils.getAvailableParkingLots(this::updateUI);
        return rootView;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        mViewModel = new ViewModelProvider(this).get(ParkingListViewModel.class);
        // TODO: Use the ViewModel
    }

    @Override
    public void updateUI(ArrayList<String> data) {
        mAdapter = new PlotsListAdapter(data);
        recyclerView.setAdapter(mAdapter);
    }
}