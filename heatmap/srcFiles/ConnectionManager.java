package edu.ysu.itrace;

import java.io.*;
import java.net.*;
import java.util.*;
import javax.swing.JWindow;
import org.eclipse.e4.core.services.events.IEventBroker;
import org.eclipse.ui.PlatformUI;
import edu.ysu.itrace.GazeCursorWindow;
import org.eclipse.swt.graphics.Point;
import edu.ysu.itrace.solvers.XMLGazeExportSolver;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.drafts.Draft_6455;
import org.java_websocket.handshake.ServerHandshake;

public class ConnectionManager {
	
	private Socket socket;
	private BufferedReader reader;
	private Timer timer;
	private IEventBroker eventBroker;
	private JWindow gazeCursorWindow = new GazeCursorWindow();
	private boolean gazeCursorDisplay = false;
	private int counter = 0;
	private int totalX = 0;
	private int totalY = 0;
	public String dirLocation = "";
	private XMLGazeExportSolver xmlSolver; 
	
	ConnectionManager(){
		xmlSolver = new XMLGazeExportSolver();
		timer = new Timer();
		eventBroker = PlatformUI.getWorkbench().getService(IEventBroker.class);
		try{
			WebSocketClient mWs = new WebSocketClient( new URI( "ws://localhost:8008" ), new Draft_6455() )
			{
                @Override
                public void onMessage( String message ) {
					if(message == null) {
						return;
					}
					String[] dataSplit = message.split(",");
					
					if (dataSplit[0].equalsIgnoreCase("session")) {
						String tmp = dataSplit[1];
						dirLocation = tmp;
						return;
					}
					
					if(dataSplit[2].toLowerCase().contains("nan") || dataSplit[3].toLowerCase().contains("nan")) {
						dataSplit[2] = "-1";
						dataSplit[3] = "-1";
					}
					
					try {
						double x = Double.parseDouble(dataSplit[2]);
						double y = Double.parseDouble(dataSplit[3]);
						
						if (Double.isNaN(x) || Double.isNaN(y)) {
							x = -1;
							y = -1;
						} 
						
						long timestamp = Long.parseLong(dataSplit[1]);
						Gaze gaze = new Gaze(x,x,y,y,0,0,0,0,timestamp, dirLocation);
						
						if (gazeCursorDisplay == true) {
							if (x < 0 || y < 0) return;
							counter++;
							totalX += x;
							totalY += y;
							if(counter == 10) {
								int avgX = totalX/10;
								int avgY = totalY/10;
								totalX = 0;
								totalY = 0;
								counter = 0;
								gazeCursorWindow.setLocation(avgX, avgY);
							}
						}
						eventBroker.post("iTrace/newgaze", gaze);
					}
					catch(Exception e) {
						e.printStackTrace();
					}
                }

                @Override
                public void onOpen( ServerHandshake handshake ) {
                    System.out.println( "opened connection" );
                }

                @Override
                public void onClose( int code, String reason, boolean remote ) {
                    System.out.println( "closed connection" );
                }

                @Override
                public void onError( Exception ex ) {
                    ex.printStackTrace();
                }

            };
            mWs.connect();
		}catch(URISyntaxException ex){
			ex.printStackTrace();
		}
	}
	
	public void showGazeCursor(boolean display) {
		gazeCursorWindow.setVisible(display);	
		gazeCursorDisplay = display;	
	}
	
	void endSocketConnection() {
		try {
			socket.close();
		}
		catch(Exception e) {
			e.printStackTrace();
		}
	}
}
