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
public class Product {
    
    private String id;
    // Holds our tasks
    private ArrayList tasksList = new ArrayList<Task>();
    private int startTime;  //Date in the future
    private int endTime;    //Date in the future
    
    public Product(String id) {
        this.id = id;
    }
    
    public Product(String id, ArrayList tasksList) {
        this.id = id;
        this.tasksList = tasksList;
    }
    
    public String getId() {
        return id;
    }

    public ArrayList getTasksList() {
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
    
}
