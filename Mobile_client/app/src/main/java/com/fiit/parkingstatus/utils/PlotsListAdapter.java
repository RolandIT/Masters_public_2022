package com.fiit.parkingstatus.utils;

import android.annotation.SuppressLint;

import android.app.Activity;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.navigation.NavController;
import androidx.navigation.NavOptions;
import androidx.navigation.Navigation;
import androidx.recyclerview.widget.RecyclerView;
import com.fiit.parkingstatus.R;


import java.util.List;

public class PlotsListAdapter extends RecyclerView.Adapter<PlotsListAdapter.ViewHolder> {
    private List<String> mDataset;



    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView plotName;


        public ViewHolder(View v) {
            super(v);
            this.plotName = (TextView) itemView.findViewById(R.id.plotName);
        }
    }

    public PlotsListAdapter(List<String> dataset) {
        mDataset = dataset;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent,
                                         int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.plots_cards_layout, parent, false);

        ViewHolder mViewHolder = new ViewHolder(view);
        return mViewHolder;
    }

    // Replace the contents of a view (invoked by the layout manager)
    @Override
    public void onBindViewHolder(ViewHolder holder, @SuppressLint("RecyclerView") final int position) {
        TextView plotName = holder.plotName;

        plotName.setText(mDataset.get(position));
        holder.itemView.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                Activity act = (Activity) v.getContext();
                Intent intent = act.getIntent();
                intent.putExtra("plot",mDataset.get(position));
                NavController controller = Navigation.findNavController(v);
                controller.navigateUp();
                controller.navigate(R.id.nav_plot_view,
                        null,
                        new NavOptions.Builder()
                                .setEnterAnim(android.R.animator.fade_in)
                                .setExitAnim(android.R.animator.fade_out)
                                .build());
            }
        });
    }

    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mDataset.size();
    }
}
