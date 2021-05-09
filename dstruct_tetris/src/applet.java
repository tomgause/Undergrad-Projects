// Tom Gause and Will Stutt
// applet.java
// May 13, 2019

import java.awt.*;        // abstract window toolkit
import java.awt.event.*;  // event handling
import java.applet.*;     // Applet classes

public class applet extends Applet implements ActionListener
{
	private static final long serialVersionUID = 1L;
	
	// instance variables
	tetris canvas;
	Panel UI;
	Label title = new Label("TETRIS");
	
	// instead of constructor
	public void init()
	{
		setFont(new Font("AmericanTypewriter", Font.BOLD, 28));
        
		canvas = new tetris(this);
        
		title.setBackground(Color.blue);
		title.setForeground(Color.white);
		title.setAlignment(Label.CENTER);
        
        Panel BUTTONS = new Panel();
        BUTTONS.setFont(new Font("AmericanTypewriter", Font.PLAIN, 24));
        BUTTONS.add(CButton("Pause",Color.red,Color.blue));
        
        Panel TEXT = new Panel();
        TEXT.setForeground(Color.white);
        TEXT.setFont(new Font("AmericanTypewriter", Font.PLAIN, 17));
        TEXT.add(new Label("controls: move => asd, rotate => kl"));
        
        UI = new Panel();
        UI.setBackground(Color.blue);
        UI.setLayout(new GridLayout(2,1));
        UI.add(BUTTONS);
        UI.add(TEXT);
        
        setLayout(new BorderLayout());
        add(title, "North");
        add(canvas, "Center");
        add(UI, "South");
        
        canvas.start();
	}
	
	// instance methods
	
	// helper function to create colored buttons
	protected Button CButton(String s, Color fg, Color bg)
	{
        Button b = new Button(s);
        b.setBackground(bg);
        b.setForeground(fg);
        b.addActionListener(this);
        return b;
    }
	
	public void actionPerformed(ActionEvent evt)
	{
		String label = ((Button)evt.getSource()).getLabel();
        if (label.equals("Pause")) {
        	canvas.isGo = !canvas.isGo;
        }
	}
}