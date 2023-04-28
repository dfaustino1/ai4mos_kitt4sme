/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package schedulingkitt;

import java.util.ArrayList;

/**
 *
 * @author Duarte
 */
public class Resource {

    private String id;
    // Holds our tasks
    private ArrayList<Task> tasksList = new ArrayList();
    private int startTime;  //Date in the future
    private int endTime;    //Date in the future
    private double makespan;
    
    public Resource(String id) {
        this.id = id;
    }

    public Resource(String id, ArrayList tasksList) {
        this.id = id;
        this.tasksList = tasksList;
    }

    public String getId() {
        return id;
    }

    public ArrayList<Task> getTasksList() {
        return tasksList;
    }

    public int getStartTime() {
        return startTime;
    }

    public void setStartTime(int startTime) {
        this.startTime = startTime;
    }

    public int getEndTime() {
        return endTime;
    }

    public void setEndTime(int endTime) {
        this.endTime = endTime;
    }

    public double getMakespan() {
        return makespan;
    }

    public void setMakespan(double makespan) {
        this.makespan = makespan;
    }
        
    
    @Override
    public String toString(){
        String geneString = "|";
        for( int i = 0; i < tasksList.size(); i++){
            geneString += tasksList.get(i).getId()+","+tasksList.get(i).getStartTime()+","+tasksList.get(i).getEndTime()+"|";
        }
        return geneString;
    }
}
