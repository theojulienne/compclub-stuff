module ipexample;

import std.string;
import std.stdio;
import std.math;

import icypixels.all;

import icylict.opengl;
import icylict.openglu;
import icylict.SDL.SDL;

class IPExample {
    GLWindow win;
    
    Texture tex;
    
    StopWatch timer;
    
    this( ) {
        win = new GLWindow( 1024, 768 );
        win.title = "IcyPixels Example";
        
        win.onMouseMoveEvent += &handleMouseMove;
		win.onMouseDownEvent += &handleMouseDown;
		win.onKeyDownEvent += &handleKeyDown;
		win.onKeyUpEvent += &handleKeyUp;
		win.onRedraw += &handleRedraw;
		
		tex = TextureCache.loadTexture( "images/test.png", false );
		
		timer.start;
    }
    
    void handleMouseMove( GLWindow window, Event event ) {
        MouseMoveEvent mouseEvent = cast(MouseMoveEvent)event;
		Vector2D mouseScreen = Vector2D( mouseEvent.mouseX, mouseEvent.mouseY );
	}
	
	void handleMouseDown( GLWindow window, Event event ) {
        MouseDownEvent mouseEvent = cast(MouseDownEvent)event;
		Vector2D mouseScreen = Vector2D( mouseEvent.mouseX, mouseEvent.mouseY );
	}
	
	void handleKeyDown( GLWindow window, Event event ) {
        KeyDownEvent keyEvent = cast(KeyDownEvent)event;
		int keyCode = keyEvent.keyCode;
	}
	
	void handleKeyUp( GLWindow window, Event event ) {
        KeyUpEvent keyEvent = cast(KeyUpEvent)event;
		int keyCode = keyEvent.keyCode;
	}
	
	void handleRedraw( GLWindow window, Event event ) {
	    win.setOrthographicProjection( );
	    
	    glLoadIdentity( );
	    
	    double t = cast(double)timer.microsec / 1000000;
	    
	    t *= 2;
	    
	    //double x = sin(t) * 100;
	    //double y = cos(t) * 100;
	    for ( int i = 0; i < 100; i++ ) {
	        double z = sin(t);
	        
	        double x = i / 10;
	        double y = i % 10;
	        
	        x += sin( t ) * 0.5;
	        y += cos( t ) * 0.5;
	        
	        glLoadIdentity( );
	        glTranslatef( window.width/10 * x, window.height/10 * y, 0 );
	        glRotatef( cos(t*cast(double)i/100)*50, 0.0f, 0.0f, 1.0f );
	        glScalef( z, z, z );
	        glColor4f( abs(sin(t)), abs(cos(t)), abs(tan(t)), 1.0f );
	        //glTranslatef( 100+x, 100+y, 0 );
	        Primitives.renderSprite( tex.width, tex.height, tex );
	    }
	    
	    win.resetPerspectiveProjection( );
	}
    
    void runGameLoop( ) {
		win.runLoop( );
	}
}

int main( string[] args ) {
    loadIcyPixelsDeps();
    
    IPExample example = new IPExample;
    example.runGameLoop( );
    
    return 0;
}
