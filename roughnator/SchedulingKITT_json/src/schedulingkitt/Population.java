/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package schedulingkitt;

import java.util.ArrayList;
import java.util.HashMap;
import java.lang.String;
import schedulingkitt.Resource;

/**
 *
 * @author Duarte
 */
public class Population {
    
    //Holds a populations of schedules
    Schedule[] schedules;
    HashMap<String, Resource> resourcesList;
    
    // Construct a population
    public Population (int populationSize, boolean initialise, HashMap<String, Resource> resourcesList){
        schedules = new Schedule[populationSize];
        this.resourcesList = resourcesList;
        
        // If we need to initialise a population of schedules do so
        if(initialise){
            // Loop and create individuals
            for (int i = 0; i < populationSize(); i++){
                Schedule newSchedule = new Schedule(this.resourcesList);
                newSchedule.generateIndividual();
                saveSchedule(i, newSchedule);
            }
        }
    }
    
    // Saves a schedule
    public void saveSchedule(int index, Schedule schedule) {
        schedules[index] = schedule;
    }
    
    // Gets a schedule from population
    public Schedule getSchedule(int index){
        return schedules[index];
    }
    
    // Gets the best schedule in the population
    public Schedule getFittest(){
        Schedule fittest = schedules[0];

        // Loop through individuals to find fittest
        for (int i = 1; i < populationSize(); i++){
            if(fittest.getFitness() <= getSchedule(i).getFitness()){
                fittest = getSchedule(i);
            }
        }
        return fittest;
    }
    
    //Sort by fittest
    public ArrayList<Schedule> sortFittest(){
        ArrayList<Schedule> fittestArray = new ArrayList<Schedule>();
        fittestArray.add(0, schedules[0]);
        
        // Loop through individuals to find fittest
        for (int i = 1; i < populationSize(); i++){
            for(int j = 0; j < fittestArray.size(); j++){
                if(fittestArray.get(j).getFitness() <= getSchedule(i).getFitness()){
                    fittestArray.add(j, getSchedule(i));
                    break;
                }        
                fittestArray.add(getSchedule(i));
            }
        }
        return fittestArray;
        
    }
    
    // Gets population size
    public int populationSize(){
        return schedules.length;
    }
}
