package ch.idsia.agents.controllers;

import ch.idsia.agents.Agent;
import ch.idsia.agents.behaviortrees.*;
import ch.idsia.benchmark.mario.engine.sprites.Mario;
import ch.idsia.benchmark.mario.environments.Environment;

public class BehaviorTreeMarioAIAgent extends BasicMarioAIAgent implements Agent {
	
	Blackboard blackboard = new Blackboard();
	boolean[] totalActions;
	
	Selector rootSelector;
	Sequence noObstacleMoveSequence;
	Sequence enemyAheadSequence;
	Sequence wallOrPipeAheadSequence;
	Sequence blockAheadSequence;
	Sequence incomingPitfallSequence;
	Sequence coinNearbySequence;
	JumpTask jumpTask;
	MoveForwardTask moveForwardTask;
	MoveBackwardTask moveBackwardTask;
	SpeedTask speedTask;
	IsObstacleAhead isObstacleAhead;
	IsEnemyAhead isEnemyAhead;
	IsObstacleWall isObstacleWall;
	IsObstacleBlock isObstacleBlock;
	IsIncomingPitfall isIncomingPitfall;
	IsCoinNearby isCoinNearby;
	
	public BehaviorTreeMarioAIAgent() {
		super("BehaviorTreeAIAgent");
		System.out.println("Creating new Agent");
		
		// Create new tasks in tree, may be reused
		
		rootSelector = new Selector(blackboard, this);
		noObstacleMoveSequence = new Sequence(blackboard, this);
		enemyAheadSequence = new Sequence(blackboard, this);
		wallOrPipeAheadSequence = new Sequence(blackboard, this);
		blockAheadSequence = new Sequence(blackboard, this);
		incomingPitfallSequence = new Sequence(blackboard, this);
		coinNearbySequence = new Sequence(blackboard, this);
		isObstacleAhead = new IsObstacleAhead(blackboard, this);
		jumpTask = new JumpTask(blackboard, this);
		moveForwardTask = new MoveForwardTask(blackboard, this);
		moveBackwardTask = new MoveBackwardTask(blackboard, this);
		speedTask = new SpeedTask(blackboard, this);
		isEnemyAhead = new IsEnemyAhead(blackboard, this);
		isObstacleWall = new IsObstacleWall(blackboard, this);
		isObstacleBlock = new IsObstacleBlock(blackboard, this);
		isIncomingPitfall = new IsIncomingPitfall(blackboard, this);
		isCoinNearby = new IsCoinNearby(blackboard, this);
		
		totalActions = new boolean[Environment.numberOfKeys];
		
		// BUILD TREE ~ Pack Sequences //
		
		enemyAheadSequence.getChildTasks().add(isEnemyAhead);
		enemyAheadSequence.getChildTasks().add(jumpTask);
		wallOrPipeAheadSequence.getChildTasks().add(isObstacleWall);
		wallOrPipeAheadSequence.getChildTasks().add(jumpTask);
		blockAheadSequence.getChildTasks().add(isObstacleBlock);
		blockAheadSequence.getChildTasks().add(speedTask);
		blockAheadSequence.getChildTasks().add(jumpTask);
		incomingPitfallSequence.getChildTasks().add(isIncomingPitfall);
		incomingPitfallSequence.getChildTasks().add(moveForwardTask);
		incomingPitfallSequence.getChildTasks().add(jumpTask);
		coinNearbySequence.getChildTasks().add(isCoinNearby);
		coinNearbySequence.getChildTasks().add(moveBackwardTask);
		coinNearbySequence.getChildTasks().add(jumpTask);
		
		// BUILD TREE ~ Pack Selector //
		
		rootSelector.getChildTasks().add(enemyAheadSequence);
		rootSelector.getChildTasks().add(coinNearbySequence);
		rootSelector.getChildTasks().add(incomingPitfallSequence);
		rootSelector.getChildTasks().add(wallOrPipeAheadSequence);
		rootSelector.getChildTasks().add(blockAheadSequence);
		rootSelector.getChildTasks().add(moveForwardTask);		
		
	}
	
	public boolean[] getAction()
	{   
		for(int i = 0; i < totalActions.length; i++) totalActions[i] = false;
		rootSelector.update(totalActions);
		return totalActions;
		
	}
	
	

}
