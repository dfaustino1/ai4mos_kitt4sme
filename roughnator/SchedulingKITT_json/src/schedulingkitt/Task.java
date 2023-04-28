/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package schedulingkitt;

/**
 *
 * @author Duarte
 */
public class Task implements Comparable<Task>{

    private String id;
    private Resource associatedResource;
    private String associatedProduct;
    private double cycleTime;
    private double executionTime;
    private int quantity;
    private double deadline;
    private double startTime;  //Date in the future
    private double endTime;    //Date in the future
    private boolean taskAllocated = false;
    
    
    //Contructor
    public Task(String id, String associatedProduct, Resource associatedResource, double cycleTime, int quantity, double deadline) {
        this.id = id;
        this.associatedProduct = associatedProduct;
        this.associatedResource = associatedResource;
        this.executionTime = cycleTime*quantity;
        this.deadline = deadline;
        this.startTime = -1;
        this.endTime = -1;
    }

    public String getId() {
        return id;
    }
    
    public String getAssociatedProduct() {
        return associatedProduct;
    }
    
    public Resource getAssociatedResource() {
        return associatedResource;
    }
    
    public double getExecutionTime() {
        return executionTime;
    }
    
    public double getDeadline() {
        return deadline;
    }

    public double getStartTime() {
        return startTime;
    }

    public void setStartTime(double startTime) {
        this.startTime = startTime;
    }

    public double getEndTime() {
        return endTime;
    }

    public void setEndTime(double endTime) {
        this.endTime = endTime;
    }
    
    public boolean isTaskAllocated(){
        return taskAllocated;
    }
    
    public void setTaskAllocated(boolean allocated){
        this.taskAllocated = allocated;
    }
    
    @Override
    public int compareTo(Task t){
        if(getStartTime() == -1 || t.getStartTime() == -1){
            return 0;
        }
        return (int)(this.getStartTime()-t.getStartTime());
    }
}
