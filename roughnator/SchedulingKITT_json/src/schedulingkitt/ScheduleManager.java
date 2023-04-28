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
public class ScheduleManager {
    
    // Holds our tasks
    private static ArrayList tasksList = new ArrayList<Task>();
    
    // Adds a task
    public static void addTask(Task task) {
        tasksList.add(task);
    }
    
    // Get a task
    public static Task getTask (int index){
        return (Task) tasksList.get(index);
    }
    
    // Get the number of tasks
    public static int numberOfTasks(){
        return tasksList.size();
    }
}
