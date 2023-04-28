/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package schedulingkitt;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.TreeMap;

/**
 *
 * @author Duarte
 */
public class Schedule {
    
    // Holds tasks
    private ArrayList<Task> schedule = new ArrayList();
    
    // Holds resources
    private HashMap<String, Resource> resourcesList;
    
    //Cache
    private double fitness = 0;
    private double makespan = 0;
    
    // Constructs a blank schedule
    public Schedule(HashMap<String, Resource> resourcesList){
        for(int i = 0; i < ScheduleManager.numberOfTasks(); i++){
            schedule.add(null);
        }
        
        this.resourcesList = resourcesList;
    }
    
    public Schedule(ArrayList schedule){
        this.schedule = schedule;
    }
    
    // Creates a random individual
    public void generateIndividual(){
        // Loop through all our tasks and add them to our schedule
        for(int taskIndex = 0; taskIndex < ScheduleManager.numberOfTasks(); taskIndex++) {
            setTask(taskIndex, ScheduleManager.getTask(taskIndex));
        }
        // Randomly reorder the schedule
        Collections.shuffle(schedule);
        
        defineExecutionTimes();
    }
    
    // Gets a task from the schedule
    public Task getTask(int schedulePosition){
        return (Task) schedule.get(schedulePosition);
    }
    
    // Sets a task in a certain position within a schedule and reset values
    public void setTask(int schedulePosition, Task task){
        // Reset allocation state
        task.setTaskAllocated(false);
                
        schedule.set(schedulePosition, task);
        // If the schedules been altered we need to reset the fitness and makespan
        fitness = 0;
        makespan = 0;
    }
    
    // Gets the schedule fitness
    public double getFitness(){
        int penalty = 1;
        if(fitness == 0){
            for(int i = 0; i<scheduleSize(); i++){
                // If the task finishes after deadline, give a penalty
                if(getTask(i).getDeadline() != -1){
                    if(getTask(i).getEndTime() > getTask(i).getDeadline()){
                        penalty = penalty*2;
                    }
                }
            }
            
            fitness = 1/((double)getMakespan()*penalty);
        }
        return fitness;
    }
    
    // Gets the total makespan of the schedule
    public double getMakespan(){
        
        Resource myResource;
        int k = 0;
        
        double scheduleMakespan = 0;
        // Loop through our schedule's resources            
        //Find the maximum makespan between stations
        Iterator it = resourcesList.entrySet().iterator();
        while (it.hasNext()) {
            HashMap.Entry<String, Resource> pair = (HashMap.Entry) it.next();
            myResource = pair.getValue();
            scheduleMakespan = myResource.getMakespan();

            if (k == 0) {
                makespan = scheduleMakespan;
                k++;
            } else {
                makespan = Math.max(makespan, scheduleMakespan);
            }
        }
        
        return makespan;
    }
    
    /**
     * FEITO PARA PERCORRER O CROMOSSOMA E DEFINIR OS TEMPOS DE EXECUÇÃO DE 
     * CADA TAREFA E MAKESPAN DAS ESTAÇÕES
     */
    public void defineExecutionTimes(){
        
        Resource myResource;
        Task currentTask = null;
        double executionTime = 0;
        String resourceId = null;
        
        // Reset resources' makespan
        Iterator it = resourcesList.entrySet().iterator();
        while (it.hasNext()) {
            HashMap.Entry<String, Resource> pair = (HashMap.Entry) it.next();
            myResource = pair.getValue();
            myResource.setMakespan(0);
        }
        
        //AVISO: TALVEZ DAR RESET DE TASKALLOCATED ANTES DO FOR EM VEZ DE DAR ANTES DE ENTRAR NA FUNÇÃO
        //RESPOSTA: NÃO, PORQUE QUANDO SE GERA UM NOVO INDIVÍDUO A TASKALLOCATED ESTÁ A FALSE, LOGO SÓ É NECESSÁRIO PARA QUANDO JÁ HÁ INDIVIDUOS CRIADOS
        for(int i = 0; i<schedule.size(); i++){ 
            currentTask = schedule.get(i);
            executionTime = currentTask.getExecutionTime();
            resourceId = currentTask.getAssociatedResource().getId();
            
            //If task already allocated ignore and go to next task, PROVAVELMENTE DESNECESSARIO
            if(currentTask.isTaskAllocated()){
                continue;
            }
            
            //Get resource of the current task
            Resource resource = resourcesList.get(resourceId);
            //Get taks list of that resource
            ArrayList<Task> tasksList = resource.getTasksList();
            //Sort tasks list by StartTime, so it will start comparing from lowest time and doesn't overlap tasks
            Collections.sort(tasksList);
            
            //Set start and end times. Also serves to reset values
            currentTask.setStartTime(0);
            currentTask.setEndTime(currentTask.getStartTime() + executionTime);

            //If there is more than one task allocated to that station, check
            //conflicts with other tasks
            if(tasksList.size() > 1){
                //Check tasks conflicts within resource - CheckStationConflicts
                for(int j = 0; j < tasksList.size(); j++){
                    Task t = tasksList.get(j);
                    //Ignore if it is the same task or if the task is not allocated yet
                    if(!t.equals(currentTask) && t.isTaskAllocated()){
                        //If there is overlapping between tasks in the same station, except itself
                        if ((t.getEndTime() > currentTask.getStartTime() && t.getEndTime() <= currentTask.getEndTime())
                                || (t.getStartTime() >= currentTask.getStartTime() && t.getStartTime() < currentTask.getEndTime())
                                || (t.getStartTime() <= currentTask.getStartTime() && t.getEndTime() >= currentTask.getEndTime())) {
                            currentTask.setStartTime((t.getEndTime()));
                            currentTask.setEndTime(currentTask.getStartTime() + executionTime);
                        }
                    }
                }
            }
            
            //SET RESOURCE MAKESPAN
            if(resource.getMakespan() < currentTask.getEndTime()){
                resource.setMakespan(currentTask.getEndTime());
            }
            
            //Set task as allocated
            currentTask.setTaskAllocated(true);
        }
    }
    
    // Get number of tasks on our schedule
    public int scheduleSize(){
        return schedule.size();
    }
    
    // Check if the schedule contains a resource
    public boolean containsTask(Task task){
        return schedule.contains(task);
    }
    
    //Working on it...
    public void removeSchedule(int i){
        schedule.remove(i);
    }

    public HashMap<String, Resource> getResourcesList() {
        return resourcesList;
    }
            
    @Override
    public String toString(){
        String geneString = "|";
        for( int i = 0; i < scheduleSize(); i++){
            geneString += getTask(i).getId()+","+getTask(i).getAssociatedResource().getId()+","+getTask(i).getStartTime()+","+getTask(i).getEndTime()+"|";
        }
        return geneString;
    }
}
