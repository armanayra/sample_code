// Procedural Content Generation - CS 387
// by Arman Ayrapetyan
// MapBuilder Class for PCG Game, generates random tileset for game

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Random;


public class MapBuilder  {
	
	ArrayList<TwoDTile> arrangedTileSet = new ArrayList<TwoDTile>();
	ArrayList<TwoDTile> randomizedFinalTileSet = new ArrayList<TwoDTile>();
	Random randomGenerator = new Random();
	PrintWriter writer = new PrintWriter((new File("generatedMap.tmx")));
	int totalTiles = 14;
	
	public MapBuilder() throws FileNotFoundException {
		arrangedTileSet = authorTiles();
		init();
    	for ( TwoDTile tile : arrangedTileSet){
    		System.out.println(tile.tileName + " has classification " + tile.getClassification());
    	}
    	System.out.println("\nFirst tile in random set is " + randomizedFinalTileSet.get(0).tileName + "\n");
    	
    	for ( TwoDTile rands : randomizedFinalTileSet){
    		System.out.println(rands.tileName + " has classification " + rands.getClassification());
    	}
    	
	}
	
	public void init(){
		TwoDTile startingTile = arrangedTileSet.get(0);
		randomizedFinalTileSet.add(startingTile);
		
		generateRandomTiles(randomizedFinalTileSet);
		generateTMXFile();
		writer.close();
	}
	
	public void generateRandomTiles(ArrayList<TwoDTile> list){
		int randomIndex;
		boolean matchFound = false;
		
		while (randomizedFinalTileSet.size() < totalTiles){
			while(!matchFound){
				TwoDTile newRandomTile;
				randomIndex = randomGenerator.nextInt(arrangedTileSet.size());
				System.out.println("The random index is " + randomIndex);
				newRandomTile = arrangedTileSet.get(randomIndex);
				if (newRandomTile.getLeftNeighbor() == randomizedFinalTileSet.get(randomizedFinalTileSet.size()-1).getRightNeighbor()){
					randomizedFinalTileSet.add(newRandomTile);
					matchFound = true;
				}
			}
			matchFound = false;
		}
		
	}
	
	public void generateTMXFile(){
		int index = 0;
		int totalSquares = totalTiles * 64;
		int squaresInRow = totalTiles * 8;
		
		int rowIndex = 0;
		int columnIndex = 0;
		
		int mapIndex = 0;
		
		
		writer.println("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
		writer.println("<map version=\"1.0\" orientation=\"orthogonal\" renderorder=\"right-down\" width=\"" + squaresInRow + "\" height=\"8\" tilewidth=\"64\" tileheight=\"64\" nextobjectid=\"1\">");
		writer.println(" <properties>");
		writer.println("  <property name=\"name\" value=\"cave_a\"/>");
		writer.println(" </properties>");
		writer.println(" <tileset firstgid=\"1\" name=\"basic\" tilewidth=\"64\" tileheight=\"64\">");
		writer.println("  <image source=\"graphics2x-basic.png\" width=\"640\" height=\"1344\"/>");
		writer.println(" </tileset>");
		writer.println(" <layer name=\"Tile Layer 1\" width=\"" + squaresInRow + "\" height=\"8\">");
		writer.println("  <data>");
		
		while (index < totalSquares){
			writer.println("   <tile gid=\"57\"/>");
			index++;
		}
		
		writer.println("  </data>");
		writer.println(" </layer>");
		
		writer.println(" <layer name=\"Tile Layer 2\" width=\"" + squaresInRow + "\" height=\"8\">");
		writer.println("  <data>");
		
		int rowCeiling;
		for (int j = 0; j < 8; j++){
			for (TwoDTile tile : randomizedFinalTileSet){
				rowCeiling = rowIndex + 8;
				if (mapIndex > 3) mapIndex = 0;
				for (int i = rowIndex; i < rowCeiling; i++){
					int[] e = randomizedFinalTileSet.get(mapIndex).getTiles();
					if (e[i] == 1){
						writer.println("   <tile gid=\"11\"/>");
					}
					else if(e[i] == 0){
						writer.println("   <tile gid=\"0\"/>");
					}
				}
				
				mapIndex++;
			}
			rowIndex += 8;
		}
		
		
		writer.println("  </data>");
		writer.println(" </layer>");
		writer.println("</map>");
		
	
	}
	
	public ArrayList<TwoDTile> authorTiles(){
		ArrayList <TwoDTile> newTileMap = new ArrayList<TwoDTile>();
		
		// 1 in 1 out
		
		TwoDTile tile_a = new TwoDTile("tile_a", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 1, 1, 1, 1, 0, 0,
							1, 0, 1, 1, 1, 1, 0, 1,
							1, 0, 1, 1, 1, 1, 0, 1,
							1, 0, 1, 1, 1, 1, 0, 1,
							1, 0, 0, 0, 0, 0, 0, 1,
							1, 0, 0, 0, 0, 0, 0, 1,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		TwoDTile tile_b = new TwoDTile("tile_b", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 0, 1, 0, 1, 0, 0,
							1, 0, 1, 0, 0, 0, 0, 1,
							1, 0, 1, 0, 1, 0, 0, 1,
							1, 0, 1, 0, 1, 0, 1, 1,
							1, 0, 0, 0, 0, 0, 0, 1,
							1, 1, 0, 0, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		TwoDTile tile_c = new TwoDTile("tile_c", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 0, 0, 0, 0, 0, 0,
							1, 0, 0, 0, 0, 0, 0, 1,
							1, 1, 0, 0, 0, 0, 1, 1,
							1, 1, 1, 0, 0, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		// 1 in 2 out
		
		TwoDTile tile_d = new TwoDTile("tile_d", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 0, 1, 1, 1, 0, 0,
							1, 0, 0, 0, 0, 0, 0, 1,
							1, 0, 0, 0, 1, 0, 0, 1,
							1, 0, 1, 0, 1, 0, 1, 1,
							1, 0, 0, 0, 0, 0, 0, 1,
							1, 1, 0, 0, 1, 1, 0, 0,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		TwoDTile tile_e = new TwoDTile("tile_e", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 1, 1, 1, 1, 0, 0,
							1, 0, 1, 0, 1, 0, 0, 1,
							1, 0, 1, 0, 0, 0, 1, 1,
							1, 0, 1, 0, 1, 0, 1, 1,
							1, 0, 1, 0, 1, 0, 1, 1,
							1, 0, 0, 0, 1, 0, 0, 0,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		TwoDTile tile_f = new TwoDTile("tile_f", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 0, 0, 0, 0, 0, 0,
							1, 1, 1, 1, 0, 1, 0, 1,
							1, 0, 0, 0, 0, 1, 0, 1,
							1, 0, 1, 1, 1, 1, 0, 1,
							1, 0, 1, 0, 0, 1, 1, 1,
							1, 0, 0, 0, 0, 0, 0, 0,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		// 2 in 1 out
		
		TwoDTile tile_g = new TwoDTile("tile_g", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 0, 0, 0, 0, 0, 0,
							1, 0, 1, 0, 0, 1, 0, 1,
							1, 0, 0, 1, 1, 0, 0, 1,
							1, 0, 0, 1, 1, 0, 0, 1,
							1, 0, 1, 0, 0, 1, 0, 1,
							0, 0, 0, 0, 0, 0, 0, 1,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		TwoDTile tile_h = new TwoDTile("tile_h", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 1, 1, 1, 1, 0, 0,
							1, 0, 0, 1, 1, 1, 0, 1,
							1, 1, 0, 0, 1, 1, 0, 1,
							1, 1, 1, 0, 0, 1, 0, 1,
							1, 1, 1, 1, 0, 0, 0, 1,
							0, 0, 0, 0, 0, 0, 0, 1,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		TwoDTile tile_i = new TwoDTile("tile_i", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 1, 1, 1, 1, 0, 0,
							1, 0, 0, 1, 1, 1, 0, 1,
							1, 1, 0, 0, 1, 1, 0, 1,
							1, 1, 1, 0, 0, 1, 0, 1,
							1, 1, 1, 1, 0, 0, 0, 1,
							0, 0, 0, 0, 0, 0, 0, 1,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		// 2 in 2 out
		
		TwoDTile tile_j = new TwoDTile("tile_j", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 0, 0, 0, 0, 0, 0,
							1, 0, 0, 0, 0, 0, 0, 1,
							1, 0, 0, 1, 1, 0, 0, 1,
							1, 0, 0, 1, 1, 0, 0, 1,
							1, 0, 0, 0, 0, 0, 0, 1,
							0, 0, 0, 0, 0, 0, 0, 0,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		TwoDTile tile_k = new TwoDTile("tile_k", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 0, 0, 0, 0, 0, 0,
							1, 1, 1, 1, 0, 1, 1, 1,
							1, 0, 0, 1, 0, 1, 1, 1,
							1, 0, 0, 0, 0, 0, 0, 1,
							1, 0, 0, 1, 1, 1, 1, 1,
							0, 0, 0, 0, 0, 0, 0, 0,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		TwoDTile tile_l = new TwoDTile("tile_l", 64, 64, 
				new int []{ 1, 1, 1, 1, 1, 1, 1, 1,
							0, 0, 1, 0, 0, 0, 0, 0,
							1, 0, 1, 0, 1, 0, 1, 1,
							1, 0, 1, 0, 1, 0, 1, 1,
							1, 0, 0, 0, 1, 0, 0, 1,
							1, 0, 1, 0, 1, 0, 1, 1,
							0, 0, 1, 0, 1, 0, 0, 0,
							1, 1, 1, 1, 1, 1, 1, 1,
						}
				);
		
		newTileMap.add(tile_a);
		newTileMap.add(tile_b);
		newTileMap.add(tile_c);
		newTileMap.add(tile_d);
		newTileMap.add(tile_e);
		newTileMap.add(tile_f);
		newTileMap.add(tile_g);
		newTileMap.add(tile_h);
		newTileMap.add(tile_i);
		newTileMap.add(tile_j);
		newTileMap.add(tile_k);
		newTileMap.add(tile_l);

		return newTileMap;
		
	}
}
