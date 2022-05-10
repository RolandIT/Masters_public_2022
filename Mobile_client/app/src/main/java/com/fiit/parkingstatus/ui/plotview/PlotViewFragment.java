package com.fiit.parkingstatus.ui.plotview;
import androidx.fragment.app.FragmentManager;
import androidx.lifecycle.ViewModelProvider;


import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewStub;
import android.widget.ImageView;
import android.widget.TextView;
import androidx.appcompat.widget.Toolbar;
import androidx.fragment.app.FragmentTransaction;

import com.fiit.parkingstatus.R;
import com.fiit.parkingstatus.utils.FirebaseUtils;
import java.util.ArrayList;
import java.util.Locale;

public class PlotViewFragment extends Fragment implements ViewUpdates {

    private PlotViewViewModel mViewModel;
    private ViewStub vs;
    private com.google.android.material.button.MaterialButton favBtn;
    private String plotN;

    public static PlotViewFragment newInstance() {
        return new PlotViewFragment();
    }

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.plot_view_fragment, container, false);
        vs = view.findViewById(R.id.plotLayout);
        Toolbar toolbar = getActivity().findViewById(R.id.toolbar);
        plotN = getActivity().getIntent().getSerializableExtra("plot").toString().toLowerCase(Locale.ROOT);

        toolbar.setTitle(plotN);

        String packageName = getContext().getPackageName();
        int resId = getResources().getIdentifier(plotN + "_plot_layout", "layout", packageName);
        vs.setLayoutResource(resId);
        vs.inflate();

        favBtn = view.findViewById(R.id.addToFavBtn);

        SharedPreferences sp = getActivity().getSharedPreferences("FavPlot", Context.MODE_PRIVATE);
        String s = sp.getString("FavPlot", "");
        if (s == "" || !s.equals(plotN)) {
            favBtn.setIconTintResource(R.color.white);
        }
        else{
            favBtn.setIconTintResource(R.color.yellow);
        }


        favBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SharedPreferences sp = getActivity().getSharedPreferences("FavPlot", Context.MODE_PRIVATE);
                SharedPreferences.Editor editor = sp.edit();
                String s = sp.getString("FavPlot", "");
                if(s == "" || !s.equals(plotN)){
                    editor.putString("FavPlot", plotN);
                    editor.commit();
                    favBtn.setIconTintResource(R.color.yellow);
                }
                else{
                    editor.remove("FavPlot");
                    favBtn.setIconTintResource(R.color.white);
                    editor.commit();
                }

            }
        });

        FirebaseUtils.startPlotStatusListener(plotN,this::updateUI);
        return view;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        mViewModel = new ViewModelProvider(this).get(PlotViewViewModel.class);
        // TODO: Use the ViewModel
    }

    @Override
    public void updateUI(ArrayList<Integer> id) {
        int x = 1;
        int parkSum = 0;
        for(int i : id){
            int resId = getResources().getIdentifier("plot" + x + "indicator", "id", getContext().getPackageName());
            ImageView indicator = this.getView().findViewById(resId);
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
    @Override
    public void onDestroy() {
        FirebaseUtils.removeListeners();
        super.onDestroy();
    }
}