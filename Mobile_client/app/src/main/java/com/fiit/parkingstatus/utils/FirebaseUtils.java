package com.fiit.parkingstatus.utils;

import android.provider.ContactsContract;
import android.util.Log;
import android.view.View;

import androidx.annotation.NonNull;

import com.fiit.parkingstatus.ui.parkinglist.ListUpdates;
import com.fiit.parkingstatus.ui.plotview.ViewUpdates;
import com.google.firebase.FirebaseApp;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class FirebaseUtils {
    private static DatabaseReference mDatabase;
    private static ValueEventListener statusListener;
    private static DatabaseReference plotRef;
    private static boolean isInitialized = false;

    public static void init(){
        if(!isInitialized)
            FirebaseDatabase.getInstance().setPersistenceEnabled(true);
            isInitialized = true;
            mDatabase = FirebaseDatabase.getInstance().getReference("parking");
    }

    public static void getAvailableParkingLots(final ListUpdates view){
        final ArrayList<String> result = new ArrayList<>();
        DatabaseReference listRef = mDatabase.child("/plotList");
        listRef.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                if(dataSnapshot.getValue() != null) {
                    for(DataSnapshot child : dataSnapshot.getChildren()){
                        result.add(child.getKey());
                    }
                    view.updateUI(result);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }

    public static void startPlotStatusListener(String plot, final ViewUpdates view){
        plotRef = mDatabase.child("/" + plot);
        statusListener = new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                ArrayList<Integer> pStatus = new ArrayList<>();
                for(DataSnapshot child : snapshot.getChildren()){
                    pStatus.add((Integer) ((Long)child.getValue()).intValue());
                }
                view.updateUI(pStatus);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        };
        plotRef.addValueEventListener(statusListener);
    }

    public static void removeListeners(){
        plotRef.removeEventListener(statusListener);
    }
}
