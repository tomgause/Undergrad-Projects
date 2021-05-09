// tetris class

import java.awt.*; // abstract window toolkit
import java.awt.event.*; // event handling

public class tetris extends Canvas implements Runnable, KeyListener
{ 
	private static final long serialVersionUID = 1L;
	
	private static final Color[] tetroColors =
    {
    	new Color(137,207,240),Color.blue,
    	Color.orange, Color.yellow,
    	new Color(57,255,20),new Color(127,0,255),
        Color.red, Color.black // black for null tetro
    };
	
	// instance variables
	public boolean isGo = false;
	grid grid;
	public int color;
	int key;
	public int score = 0;
	applet parent;
	Thread t;
	
	// constructor
	public tetris(applet p)
	{
		setBackground(Color.black);
        Dimension screensize = new Dimension(300,600);
        setSize(screensize);
        addKeyListener(this);
        parent = p;
        grid = new grid(this);
        isGo = true;
        grid.newT();
        repaint();
    }
	
	// instance methods
	
	// thread methods
	
	public void run() {
        int cnt = 0;
        Thread currentThread = Thread.currentThread();
        while (currentThread == t && t!=null) {
    	   grid.tryDrop();
           cnt = (cnt+1) % 10;
           try {
               Thread.sleep(500);
           } catch (InterruptedException e) {};
           repaint();
       }
   }
	
	public void start() {
       t = new Thread(this);
       t.start();
    }

	public void stop() {
       t = null;
    }
	
	// KeyListener methods
	
	public void keyPressed(KeyEvent e)
	{
		int KEY = e.getKeyCode();
		key = KEY;
	}
	public void keyReleased(KeyEvent e) { }
	public void keyTyped(KeyEvent e)
	{
		if (!isGo) return; // do nothing if game paused
		if (key == KeyEvent.VK_A) { // left arrow pressed, tryLeft
			grid.tryLeft();
		}
		else if (key == KeyEvent.VK_D) { // right arrow pressed, tryRight
			grid.tryRight();
		}
		else if (key == KeyEvent.VK_S) { // down arrow pressed, tryDrop
			grid.tryDrop();
		}
		else if (key == KeyEvent.VK_L) { // l pressed, tryRotateR
			grid.tryRotateR();
		}
		else if (key == KeyEvent.VK_K) { // k pressed, tryRotateL
			grid.tryRotateL();
		}
		color = grid.getT();
		repaint();
	}
	
	// other methods
	
	// This method is called by Java when the window is changed (e.g.,
    // uncovered or resized), or when "repaint()" is called.
	public synchronized void paint(Graphics g)
	{
		if (t==null) {
			parent.title.setText("YOU LOSE!");
			isGo = false;
			stop();
			return;
		}
		drawRest(g);
		drawTetro(g);
	}
	
	// draws active tetro
	public void drawTetro(Graphics g)
	{
		g.setColor(tetroColors[color]);
		int[][] tCO = grid.getTCO();
		for (int i=0;i<4;i++)
		{
			int x = tCO[i][0];
			int y = tCO[i][1];
			g.fillRect((x+grid.getX())*30,(y+grid.getY())*30,30,30);
		}
	}
	
	// draws static tetros
	public void drawRest(Graphics g)
	{
		int[][] allG = grid.getGridAll();
		for (int i=0;i<10;i++)
		{
			for (int j=0;j<20;j++)
			{
				int var = allG[i][j];
				if (var != 0)
				{
					g.setColor(tetroColors[var-1]);
					g.fillRect(i*30,j*30,30,30);
				}
			}
		}
		g.setFont(new Font("Americantypewriter", Font.BOLD, 20));
		g.setColor(Color.white);
		g.drawString(" Score = " + Integer.toString(score),0,20);
	}
	
	// quick print
	public void p(String s)
	{
		System.out.println(s);
	}
	
	// quick print for integers
	public void pint(int i)
	{
		System.out.print(Integer.toString(i) + " ");
	}
}