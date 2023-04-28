/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package schedulingkitt;

import java.util.ArrayList;
import java.util.HashMap;

/**
 *
 * @author Duarte
 */
public class Algorithm {
    
    /* GA parameters */
    private static final double mutationRate = 0.1;    //0.015
    private static final double crossoverRate = 0.85;
    private static final int tournamentSize = 5;
    private static final boolean elitism = true;
    
    // Evolves a population over one generation
    public static Population evolvePopulation(Population pop, HashMap<String, Resource> resourcesList){
        Population newPopulation = new Population(pop.populationSize(), false, resourcesList);
        
        // Keep our best individual if elitism is enabled
        int elitismOffset = 0;
        /*
        if(elitism){
            newPopulation.saveSchedule(0, pop.getFittest());
            elitismOffset = 1;
        }
        */
        
        
        //I added this to set the crossover rate, instead of keep only the best individual from the previous generation
        //Sort fittest
        ArrayList<Schedule> sortedPop = pop.sortFittest();
        for(int i = 0; i< (pop.populationSize() - pop.populationSize()*crossoverRate); i++){                        
            newPopulation.saveSchedule(i, sortedPop.get(i));   
            elitismOffset++;
        }
        
        // Crossover population
        // Loop over the new population's size and create individuals from current population
        for(int i = elitismOffset; i < newPopulation.populationSize(); i++){
            // Select parents
            Schedule parent1 = tournamentSelection(pop, resourcesList);
            Schedule parent2 = tournamentSelection(pop, resourcesList);
            // Crossover parents
            Schedule child = crossover(parent1, parent2, resourcesList);
            //Reset tasks' allocated state
            for(int m=0; m<child.scheduleSize(); m++){
                child.getTask(m).setTaskAllocated(false);
            }
            //AVISO: Definir tempos de execução
            //Set start and end times for new individual
            child.defineExecutionTimes();
            //Set makespan and fitness
            child.getFitness();
            
            // Add child to new population
            newPopulation.saveSchedule(i, child);
        }
        
        // Mutate the new population a bit to add some new genetic material
        for (int i = elitismOffset; i < newPopulation.populationSize(); i++){
            if(mutate(newPopulation.getSchedule(i))){
                for(int m=0; m<newPopulation.getSchedule(i).scheduleSize(); m++){
                    newPopulation.getSchedule(i).getTask(m).setTaskAllocated(false);
                }
                newPopulation.getSchedule(i).defineExecutionTimes();
                newPopulation.getSchedule(i).getFitness();
            }
        }
        
        return newPopulation;
    }
    
    // Applies crossover to a set of parents and creates offspring
    public static Schedule crossover(Schedule parent1, Schedule parent2, HashMap<String, Resource> resourcesList){
        // Create new child schedule
        Schedule child = new Schedule(resourcesList);
        
        // Get start and end sub schedule positions for parent1's schedule
        int startPos = (int) (Math.random() * parent1.scheduleSize());
        int endPos = (int) (Math.random() * parent1.scheduleSize());
        
        // Loop and add the sub schedule from parent1 to our child
        for(int i = 0; i < child.scheduleSize(); i++){
            // If our start position is less than the end position
            if(startPos < endPos && i>startPos && i<endPos){
                child.setTask(i, parent1.getTask(i));
            } //If our start position is larger
            else if(startPos > endPos){
                if(!(i < startPos && i > endPos)){
                    child.setTask(i, parent1.getTask(i));
                }
            }
        }
        
        // Loop through parent2's tasks schedule
        for ( int i = 0; i < parent2.scheduleSize(); i++){
            // If child doesn't have the task add it
            if(!child.containsTask(parent2.getTask(i))){
                // Loop to find a spare position in the child's schedule
                for (int ii = 0; ii < child.scheduleSize(); ii++){
                    // Spare position found, add task
                    if(child.getTask(ii) == null){
                        child.setTask(ii, parent2.getTask(i));
                        break;
                    }
                }
            }
            
        }
        return child;
    }
    
    // Mutate a schedule using swap mutation
    private static boolean mutate(Schedule schedule){
        
        boolean mutationPerformed = false;
        
        // Loop through schedule tasks
        for(int schedulePos1=0; schedulePos1 < schedule.scheduleSize(); schedulePos1++){
            // Apply mutation rate
            if(Math.random() < mutationRate){
                // Get a second random position in the schedule
                int schedulePos2 = (int) (schedule.scheduleSize() * Math.random());
                
                // Get the tasks at a target position in schedule
                Task task1 = schedule.getTask(schedulePos1);
                Task task2 = schedule.getTask(schedulePos2);
                
                // Swap them around
                schedule.setTask(schedulePos2, task1);
                schedule.setTask(schedulePos1, task2);
                
                mutationPerformed = true;
            }
        }
        
        return mutationPerformed;
    }
    
    // Selects candidate schedule for crossover
    private static Schedule tournamentSelection(Population pop, HashMap<String, Resource> resourcesList){
        // Create a tournament population
        Population tournament = new Population(tournamentSize, false, resourcesList);
        // For each place in the tournament get a random candidate schedule and add it
        for (int i = 0; i < tournamentSize; i++){
            int randomId = (int) (Math.random()*pop.populationSize());
            tournament.saveSchedule(i, pop.getSchedule(randomId));
        }
        Schedule fittest = tournament.getFittest();
        return fittest;
    }
}
