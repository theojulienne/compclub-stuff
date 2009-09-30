module ipexample;

import std.string;
import std.stdio;

import icypixels.all;

import icylict.opengl;
import icylict.openglu;
import icylict.SDL.SDL;

class IPExample {
    GLWindow win;
    
    Texture tex;
    
    this( ) {
        win = new GLWindow( 1024, 768 );
        win.title = "IcyPixels Example";
        
        win.onMouseMoveEvent += &handleMouseMove;
		win.onMouseDownEvent += &handleMouseDown;
		win.onKeyDownEvent += &handleKeyDown;
		win.onKeyUpEvent += &handleKeyUp;
		win.onRedraw += &handleRedraw;
		
		tex = TextureCache.loadTexture( "images/test.png", false );
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
	    
	    Primitives.renderSprite( tex.width, tex.height, tex );
	    
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
