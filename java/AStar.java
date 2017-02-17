package s3.ai;


import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import javafx.collections.transformation.SortedList;
import s3.base.S3;
import s3.entities.S3PhysicalEntity;
import s3.entities.WOGrass;
import s3.util.Pair;


public class AStar {
	
	public double a_star_startx;
	public double a_star_starty;
	
	public double a_star_goalx;
	public double a_star_goaly;
	
	public int mapWidth = 0;
	public int mapHeight = 0;
	
	S3PhysicalEntity thisEntity;
	S3 thisGame;
	
	int gameCount = 1;
	
	/** The set of nodes that we do not yet consider fully searched */
	ArrayList <CellHeuristics> open = new ArrayList <CellHeuristics>();
	/** The set of nodes that have been searched through */
	ArrayList <CellHeuristics> closed = new ArrayList <CellHeuristics>();
	
	Set<Pair<Double, Double>> closedSetCoords = new HashSet<>(); // was not used
	List<Pair<Double, Double>> finalPath = new ArrayList<Pair<Double, Double>>();
	
	int mapOccupancyList[][]; // Store 1 if grass, 0 otherwise

	
	public static int pathDistance(double start_x, double start_y, double goal_x, double goal_y, S3PhysicalEntity i_entity, S3 the_game) {
		AStar a = new AStar(start_x,start_y,goal_x,goal_y,i_entity,the_game);
		List<Pair<Double, Double>> path = a.computePath();
		if (path!=null) return path.size();
		return -1;
	}

	public AStar(double start_x, double start_y, double goal_x, double goal_y, S3PhysicalEntity i_entity, S3 the_game) {
		a_star_startx = start_x;
		a_star_starty = start_y;
		a_star_goalx = goal_x;
		a_star_goaly = goal_y;
		thisEntity = i_entity;
		thisGame = the_game;
		
		mapWidth = the_game.getMap().getWidth();
		mapHeight = the_game.getMap().getHeight();
		
		mapOccupancyList = new int[mapWidth][mapHeight];
		
		System.out.println("START \n");
		for (int h = 0; h < mapOccupancyList.length; h++ ){
			for (int v = 0; v < mapOccupancyList[h].length; v++){
				mapOccupancyList[h][v] = 0;	
			}
		}
	}

	public List<Pair<Double, Double>> computePath() {
        
		if (!(thisGame.getEntity((int) a_star_goalx, (int) a_star_goaly) instanceof WOGrass)){  // if destination is blocked
			return null; 
		}
		
		closed.clear();
		open.clear();
		
		int rootLevel = 0;
		
		CellHeuristics startingCell = new CellHeuristics(rootLevel, a_star_startx, a_star_starty, null);
		startingCell.set_h_n(heuristicFunc(startingCell)); 
		
		open.add(startingCell);
		
		while(!open.isEmpty()){
			System.out.println("\nGame Counter: " + gameCount + "\n");
			int targetIndex = getLowestF(open);
			
			CellHeuristics thisCell = open.remove(targetIndex);
			
			if (isGoal(thisCell)){
				System.out.println("Found Goal!");
				returnPathToStart(thisCell);
				return finalPath;
			}
			else {
				System.out.println("No goal found yet!~~~~~~~~~~");
			}
			closed.add(thisCell);
			//mapOccupancyList[(int) thisCell.getLocy()][(int) thisCell.getLocx()] = 1;	

			ArrayList <CellHeuristics> theseChildren = generateChildren(thisCell);
			ArrayList <CellHeuristics> newChildren = removeDuplicates(theseChildren);
			for (int i = 0; i < newChildren.size(); i++){
				open.add(newChildren.get(i));
			}
			gameCount++;
		}
		
		return null;
	}
	
	public double heuristicFunc(CellHeuristics cell){
		
		// Calculate distance based on x and y using start and goal
		double newX = Math.abs(a_star_goalx - cell.getLocx());
		double newY = Math.abs(a_star_goaly - cell.getLocy());
		double distanceFromStart = newX + newY;
		
		return distanceFromStart;
	}
	
	public ArrayList <CellHeuristics> generateChildren(CellHeuristics parentCell){
		
		int parent_x = (int) parentCell.getLocx();
		int parent_y = (int) parentCell.getLocy();
		int cur_x;
		int cur_y;
		
		ArrayList <CellHeuristics> children = new ArrayList <CellHeuristics>();
		
		
		// check north
		cur_x = parent_x;
		cur_y = parent_y - 1;
		if (inBounds(cur_x, cur_y)) {
			if (thisGame.getEntity(cur_x, cur_y) instanceof WOGrass){
				CellHeuristics northCell = new CellHeuristics(parentCell.get_g_n() + 1, cur_x, cur_y, parentCell);
				northCell.set_h_n(heuristicFunc(northCell));
				northCell.computeF();
				children.add(northCell);
			}
		}
		// check south
		cur_x = parent_x;
		cur_y = parent_y + 1;
		if (inBounds(cur_x, cur_y)) {
			if (thisGame.getEntity(cur_x, cur_y) instanceof WOGrass){
				CellHeuristics southCell = new CellHeuristics(parentCell.get_g_n() + 1, cur_x, cur_y, parentCell);
				southCell.set_h_n(heuristicFunc(southCell));
				southCell.computeF();
				children.add(southCell);
			}
		}
		// check east
		cur_x = parent_x + 1;
		cur_y = parent_y;
		if (inBounds(cur_x, cur_y)) {
			if (thisGame.getEntity(cur_x, cur_y) instanceof WOGrass){
				CellHeuristics eastCell = new CellHeuristics(parentCell.get_g_n() + 1, cur_x, cur_y, parentCell);
				eastCell.set_h_n(heuristicFunc(eastCell));
				eastCell.computeF();
				children.add(eastCell);
			}
		}
		// check west
		cur_x = parent_x - 1;
		cur_y = parent_y;
		if (inBounds(cur_x, cur_y)) {
			if (thisGame.getEntity(cur_x, cur_y) instanceof WOGrass){
				CellHeuristics westCell = new CellHeuristics(parentCell.get_g_n() + 1, cur_x, cur_y, parentCell);
				westCell.set_h_n(heuristicFunc(westCell));
				westCell.computeF();
				children.add(westCell);
			}
		}
		
		return children;
		
	}
	
	public boolean inBounds(int x, int y){
		if ( x < 0 || x > mapWidth || y < 0 || y > mapHeight ){
			return false;
		}
		else {
			return true;
		}
	}
	
	public int getLowestF(ArrayList <CellHeuristics> list){
		int index = 0;
		int currentLowest = 1000;
		
		for (int i = 0; i < list.size(); i++){
			CellHeuristics c = list.get(i);
			if (c.get_f_n() < currentLowest){
				currentLowest = (int) c.get_f_n();
				index = i;
			}
		}
		return index;
	}
	
	public boolean isGoal(CellHeuristics cell){
		if ((cell.getLocx() == a_star_goalx) && (cell.getLocy() == a_star_goaly)){
			System.out.println("Got to the goal!");
			return true;
		}
		else {
			return false;
		}
	}
	
	public void returnPathToStart(CellHeuristics cell){
		System.out.println("Calculating path to start");
		while (cell.hasParent()){
			Pair <Double, Double> step = new Pair<Double, Double>(cell.getLocx(), cell.getLocy());
			System.out.println("(" + step.m_a + ", " + step.m_b + ")");
			finalPath.add(step);
			cell = cell.parent;
		}
		Collections.reverse(finalPath);
	}
	
	
	
	ArrayList <CellHeuristics> removeDuplicates(ArrayList <CellHeuristics> uncheckedChildren){
		Set <CellHeuristics> combinedList = new HashSet <CellHeuristics>(open);
		combinedList.addAll(closed);
		ArrayList <CellHeuristics> copyList = new ArrayList <CellHeuristics>(uncheckedChildren);
		
		for (CellHeuristics j : uncheckedChildren){
			for (CellHeuristics c : combinedList){
				if (j.getLocx() == c.getLocx() && j.getLocy() == c.getLocy()){
					copyList.remove(j); 
				}
			}
		}
		return copyList;
	}
	

}
