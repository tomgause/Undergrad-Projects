// tetromino class

public class tetromino
{
	
	// tetro integer assignments
	public static final int I = 0;
    public static final int J = 1;
    public static final int L = 2;
    public static final int O = 3;
    public static final int S = 4;
    public static final int T = 5;
    public static final int Z = 6;
	
    public static final int NORTH = 0;
    public static final int EAST = 1;
    public static final int SOUTH = 2;
    public static final int WEST = 3;
    
    // grid representations of all tetromino
    // rotations, 0-6
    private int[][][] tetroOrientationN =
    {
    	{ {0,1}, {1,1}, {2,1}, {3,1} },
    	{ {0,0}, {0,1}, {1,1}, {2,1} },
    	{ {2,0}, {0,1}, {1,1}, {2,1} },
    	{ {1,0}, {2,0}, {1,1}, {2,1} },
    	{ {1,0}, {2,0}, {0,1}, {1,1} },
    	{ {1,0}, {0,1}, {1,1}, {2,1} },
    	{ {0,0}, {1,0}, {1,1}, {2,1} },
    };
    private int[][][] tetroOrientationE =
    {
    	{ {2,0}, {2,1}, {2,2}, {2,3} },
    	{ {1,0}, {2,0}, {1,1}, {1,2} },
    	{ {1,0}, {1,1}, {1,2}, {2,2} },
    	{ {1,0}, {2,0}, {1,1}, {2,1} },
    	{ {1,0}, {1,1}, {2,1}, {2,2} },
    	{ {1,0}, {1,1}, {2,1}, {1,2} },
    	{ {2,0}, {1,1}, {2,1}, {1,2} },
    };
    private int[][][] tetroOrientationS =
    {
		{ {0,2}, {1,2}, {2,2}, {3,2} },
    	{ {0,1}, {1,1}, {2,1}, {2,2} },
    	{ {0,1}, {1,1}, {2,1}, {0,2} },
    	{ {1,0}, {2,0}, {1,1}, {2,1} },
    	{ {1,1}, {2,1}, {0,2}, {1,2} },
    	{ {0,1}, {1,1}, {2,1}, {1,2} },
    	{ {0,1}, {1,1}, {1,2}, {2,2} },
    };
    private int[][][] tetroOrientationW =
    {
		{ {1,0}, {1,1}, {1,2}, {1,3} },
    	{ {1,0}, {1,1}, {0,2}, {1,2} },
    	{ {0,0}, {1,0}, {1,1}, {1,2} },
    	{ {1,0}, {2,0}, {1,1}, {2,1} },
    	{ {0,0}, {0,1}, {1,1}, {1,2} },
    	{ {1,0}, {0,1}, {1,1}, {1,2} },
    	{ {1,0}, {0,1}, {1,1}, {0,2} },
    };
    
    // instance variables
    int type;
    //int x;
    //int y;
    int[][] CO; // current orientation
    int[][] NO; // north orientation
    int[][] EO; // east orientation
    int[][] SO; // south orientation
    int[][] WO; // west orientation
    
    // constructor
	public tetromino(int t)
	{
		type = t;
		NO = tetroOrientationN[t];
		EO = tetroOrientationE[t];
		SO = tetroOrientationS[t];
		WO = tetroOrientationW[t];
		CO = NO;
	}
	
	// instance methods
	
	//public void setX(int i) { x = i; }
	//public void setY(int i) { y = i; }
	//public int getX() { return x; }
	//public int getY() { return y; }
	public int[][] getCO() { return CO; }
	public int getType() { return type; }
	
	// rotates tetro 90 to right
	public void rotateR()
	{
		if (CO==NO) CO=EO;
		else if (CO==EO) CO=SO;
		else if (CO==SO) CO=WO;
		else if (CO==WO) CO=NO;
	}
	
	// rotates tetro 90 to left
	public void rotateL()
	{
		if (CO==NO) CO=WO;
		else if (CO==WO) CO=SO;
		else if (CO==SO) CO=EO;
		else if (CO==EO) CO=NO;
	}
}
