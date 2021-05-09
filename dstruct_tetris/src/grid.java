// grid class

public class grid
{
	public static final int EMPTY = 0;
	
	// instance variables
	// any c=current
	tetris parent;
	private int cX = 0;
	private int cY = 0;
	private tetromino cT;
	private int[][] playGrid;
	
	// constructor
	public grid(tetris s) {
		parent = s;
		playGrid = new int[10][20];
		for (int i=0;i<10;i++) {
			for (int j=0;j<20;j++) {
				playGrid[i][j] = EMPTY;
			}
		}
	}
	
	// instance methods
	
	// calls for instance variables
	public int getGrid(int x, int y) { return playGrid[x][y]; }
	public int[][] getGridAll() { return playGrid; }
	public int[][] getTCO() { return cT.getCO(); }
	public int getX() { return cX; }
	public int getY() { return cY; }
	public int getT() { return cT.getType(); }
		
	// generates new tetro of random type
	public void newT() {
		int t = getRandomInt(0,6);
		cT = new tetromino(t);
		cX = 3;
		cY = 0;
		parent.color = t;
		int[][] temp = cT.getCO();
		for (int i=0;i<4;i++)
		{
			if (playGrid[cX+temp[i][0]][cY+temp[i][1]] != EMPTY) {
				parent.stop();
			}
		}
	}
	
	// generates random number in range min-max
	public static int getRandomInt(int min, int max) {
		return min + (int)(Math.random() * ((max - min) + 1));
	}

	// tries to move tetro to right 1 unit
	// on failure, does nothing
	public void tryRight() {
		int[][] temp = cT.getCO();
		for (int i=0;i<4;i++) {
			if (cX + temp[i][0]+1 > 9) return;
			if (playGrid[cX+temp[i][0]+1][cY+temp[i][1]] != EMPTY) return;
		}
		cX += 1;
	}
	
	// tries to move tetro to left 1 unit
	// on failure, does nothing
	public void tryLeft() {
		int[][] temp = cT.getCO();
		for (int i=0;i<4;i++)
		{
			if (cX + temp[i][0]-1 < 0) return;
			if (playGrid[cX+temp[i][0]-1][cY+temp[i][1]] != EMPTY) return;
		}
		cX += -1;
	}
	
	// tries to move tetro down 1 unit
	// on failure, sets gridspaces to color ids,
	// generates new tetro
	public void tryDrop()
	{
		if (!parent.isGo) return;
		int[][] temp = cT.getCO();
		for (int i=0;i<4;i++)
		{
			if (cY+temp[i][1] == 19 ||
					(playGrid[cX+temp[i][0]][cY+temp[i][1]+1] != EMPTY))
			{
				for (int j=0;j<4;j++)
				{
					playGrid[cX+temp[j][0]][cY+temp[j][1]] = cT.getType()+1;
				}
				checkAllRows();
				newT();
				return;
			}
		}
		cY += 1;
	}
	
	// tries to rotate tetro right 90
	// on failure, does nothing (no kick implemented)
	public void tryRotateR() {
		cT.rotateR();
		int[][] temp = cT.getCO();
		for (int i=0;i<4;i++) {
			try {
				if (cX+temp[i][0]<1 || cX+temp[i][0]>10) {
					cT.rotateL();
					return;
				}
				if (playGrid[cX+temp[i][0]-1][cY+temp[i][1]] != 0) {
					cT.rotateL();
					return;
				}
			} catch(ArrayIndexOutOfBoundsException e) {
				cT.rotateL();
				return;
			}
		}
	}
	
	// tries to rotate tetro left 90
	// on failure, does nothing (no kick implemented)
	public void tryRotateL() {
		cT.rotateL();
		int[][] temp = cT.getCO();
		for (int i=0;i<4;i++) {
			try {
				if (cX+temp[i][0]<1 || cX+temp[i][0]>10) {
					cT.rotateR();
					return;
				}
				if (playGrid[cX+temp[i][0]-1][cY+temp[i][1]] != 0) {
					cT.rotateR();
					return;
				}
			} catch(ArrayIndexOutOfBoundsException e) {
				cT.rotateR();
				return;
			}
		}
	}
	
	// checks all rows for rowFilled
	public void checkAllRows() {
		for (int r=0;r<20;r++) {
			rowFilled(r);
		}
	}
	
	// checks to see if a row i is filled
	// if true, calls clearRow
	public void rowFilled(int i)
	{
		int[][] temp = playGrid;
		for (int j=0;j<10;j++)
		{
			if (temp[j][i]==0) return;
		}
		clearRow(i);
	}
	
	// clears row, drops down all values above
	public void clearRow(int i)
	{
		for (int j=0;j<10;j++)
		{
			for (int r=i;r>1;r--)
			{
				playGrid[j][r] = playGrid[j][r-1];
			}
		}
		parent.score += 10;
		checkAllRows();
	}
	
	// prints grid
	// note: xy coords printed yx
	public void printGrid()
	{
		for (int i=0;i<10;i++)
		{
			for (int j=0;j<20;j++)
			{
				parent.pint(playGrid[i][j]);
			}
			parent.p("");
		}
	}
}
