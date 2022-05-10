package com.fiit.parkingstatus.ui.home;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewStub;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.fiit.parkingstatus.R;
import com.fiit.parkingstatus.databinding.FragmentHomeBinding;
import com.fiit.parkingstatus.ui.plotview.PlotViewFragment;
import com.fiit.parkingstatus.ui.plotview.ViewUpdates;
import com.fiit.parkingstatus.utils.FirebaseUtils;

import java.util.ArrayList;
import java.util.Locale;

public class HomeFragment extends Fragment implements ViewUpdates {

    private HomeViewModel homeViewModel;
    private FragmentHomeBinding binding;
    private TextView noFavText;
    private ConstraintLayout plotStatusTopBar;
    private ConstraintLayout plotStatus;

    private ViewStub vs;
    private com.google.android.material.button.MaterialButton favBtn;
    private String plotN;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        homeViewModel =
                new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();
        vs = root.findViewById(R.id.plotLayout);
        noFavText = root.findViewById(R.id.noFavText);
        plotStatusTopBar = root.findViewById(R.id.plotStatusTopBar);
        plotStatus = root.findViewById(R.id.plotStatus);
        favBtn = root.findViewById(R.id.addToFavBtn);

        SharedPreferences sp = getActivity().getSharedPreferences("FavPlot", Context.MODE_PRIVATE);
        plotN = sp.getString("FavPlot", " ");

        favBtn.setIconTintResource(R.color.yellow);
        if(plotN != " ") {
            String packageName = getContext().getPackageName();
            int resId = getResources().getIdentifier(plotN + "_plot_layout", "layout", packageName);
            vs.setLayoutResource(resId);
            vs.inflate();
        }

        favBtn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    SharedPreferences sp = getActivity().getSharedPreferences("FavPlot", Context.MODE_PRIVATE);
                    SharedPreferences.Editor editor = sp.edit();

                    editor.remove("FavPlot");
                    favBtn.setIconTintResource(R.color.white);
                    editor.commit();
                    plotStatusTopBar.setVisibility(View.INVISIBLE);
                    plotStatus.setVisibility(View.INVISIBLE);
                    noFavText.setVisibility(View.VISIBLE);
                }
            }
        );


        homeViewModel.getText().observe(getViewLifecycleOwner(), new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {

            }
        });
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    @Override
    public void onResume() {
        FirebaseUtils.startPlotStatusListener(plotN,this::updateUI);
        SharedPreferences sp = getActivity().getSharedPreferences("FavPlot", Context.MODE_PRIVATE);
        plotN = sp.getString("FavPlot", " ");

        if(plotN != " ") {

//            String packageName = getContext().getPackageName();
//            int resId = getResources().getIdentifier(plotN + "_plot_layout", "layout", packageName);
//            vs.setLayoutResource(resId);
//            vs.inflate();

            noFavText.setVisibility(View.INVISIBLE);
            plotStatusTopBar.setVisibility(View.VISIBLE);
            plotStatus.setVisibility(View.VISIBLE);

        }
        super.onResume();
    }

    @Override
    public void updateUI(ArrayList<Integer> id) {
        int x = 1;
        int parkSum = 0;
        for(int i : id){
            int resId = getResources().getIdentifier("plot" + x + "indicator", "id", getContext().getPackageName());
            ImageView indicator = this.getView().findViewById(resId);
            if(indicator == null)
                return;
            if(i == 1) {
                indicator.setImageResource(R.drawable.ic_car);
            }
            else{
                indicator.setImageResource(R.drawable.ic_parking);
            }
            x ++;
            parkSum += i;
        }

        TextView numberOfFreeSpaces = this.getView().findViewById(R.id.emptySpotsNum);
        numberOfFreeSpaces.setText(Integer.toString(id.size() - parkSum));
    }
}