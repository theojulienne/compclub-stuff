module ipexample;

import pixels;

import std.string;
import std.stdio;
import std.math;

import icypixels.all;

version (darwin) {
	public import derelict.sdl.sdl;
	public import derelict.opengl.gl;
	
	public import tango.time.StopWatch;
} else {
	import icylict.opengl;
	import icylict.openglu;
	import icylict.SDL.SDL;
}

struct Pixel {
    float x, y, z;
    float r, g, b, a;
}

extern (C) void exit( int );

class IPExample {
    GLWindow win;
    
    Texture tex;
    
    Pixel[] points;
    
    StopWatch timer;
    
    this( ) {
        win = new GLWindow( 1024, 768 );
        win.title = "3D Pixel Renderer";
        
        win.onMouseMoveEvent += &handleMouseMove;
		win.onMouseDownEvent += &handleMouseDown;
		win.onKeyDownEvent += &handleKeyDown;
		win.onKeyUpEvent += &handleKeyUp;
		win.onRedraw += &handleRedraw;
		
		/*
		points.length = 8*8*8;
		
		for ( int x = 0; x < 8; x++ ) {
		    for ( int y = 0; y < 8; y++ ) {
		        for ( int z = 0; z < 8; z++ ) {
		            int n = (((x*8)+y)*8)+z;
		            
		            assert( n < points.length );
		            
		            points[n].x = x;
		            points[n].y = y;
		            points[n].z = z;
		            points[n].r = x / 8.0;
		            points[n].g = y / 8.0;
		            points[n].b = z / 8.0;
		            points[n].a = 1.0;
		        }
		    }
		}
		*/
		
		points.length = awesomePixels.length;
		
		foreach( n, pixel; awesomePixels ) {
    		points[n].x = pixel[0];
		    points[n].y = pixel[1];
		    points[n].z = pixel[2];
		    points[n].r = 1;
		    points[n].g = 1;
		    points[n].b = 1;
		    points[n].a = 1.0;
		}
		
		
		tex = TextureCache.loadTexture( "images/sprite.png", false );
		
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
		
		exit( 0 );
	}
	
	void handleKeyUp( GLWindow window, Event event ) {
        KeyUpEvent keyEvent = cast(KeyUpEvent)event;
		int keyCode = keyEvent.keyCode;
	}
	
	void handleRedraw( GLWindow window, Event event ) {
	    glLoadIdentity( );
	    
	    glAlphaFunc(GL_GREATER, 0.0f);
	    
	    glTranslatef( 0.0f, 0.0f, -10.0f );
	    
	    double t = cast(double)timer.microsec / 1000000;
	    
	    Vector3D rotation;
	    rotation.x = 30.0f;
	    rotation.y = t*10;
	    rotation.z = 0.0f;
	    
	    float scale = 0.6;
	    float blobSize = 0.2;//0.8;
	    
	    glRotatef( rotation.x, 1.0f, 0.0f, 0.0f );
	    glRotatef( rotation.y, 0.0f, 1.0f, 0.0f );
	    glRotatef( rotation.z, 0.0f, 0.0f, 1.0f );
	    
	    float offset = (8)/2;
	    glScalef( scale, scale, scale );
	    glTranslatef( -offset, -offset, -offset );
	    
	    // disable depth testing so that the alpha doesn't break
	    glDisable (GL_DEPTH_TEST);
	    
	    float distances[];
	    distances.length = points.length;
	    
	    Vector3D origin = Vector3D( 0, 0, 0 );
	    
	    foreach ( i, point; points ) {
	        glColor4f( point.r, point.g, point.b, point.a );
	        
	        glPushMatrix( );
	        
	        // move to the blob's position
	        glTranslatef( point.x, point.y, point.z );
	        
	        // un-rotate so the blob faces the camera
    	    glRotatef( -rotation.z, 0.0f, 0.0f, 1.0f );
            glRotatef( -rotation.y, 0.0f, 1.0f, 0.0f );
      	    glRotatef( -rotation.x, 1.0f, 0.0f, 0.0f );
      	    
      	    // hax the gl matrix
      	    GLfloat m[16];
      	    glGetFloatv( GL_MODELVIEW_MATRIX, m.ptr );
      	    Vector3D p;
      	    p.x = m[12];
      	    p.y = m[13];
      	    p.z = m[14];
      	    
      	    //writefln( "%s", m );
      	    
      	    //writefln( "%s,%s,%s", p.x, p.y, p.z );
      	    
      	    distances[i] = p.distance( origin );
      	    //writefln( "%s", distances[i] );
	        
	        glPopMatrix( );
	    }
	    
	    //exit( 0 );
	    
	    void renderPoint( int i ) {
	        auto point = points[i];
	    
	        glColor4f( point.r, point.g, point.b, point.a );
	        
	        glPushMatrix( );
	        
	        // move to the blob's position
	        glTranslatef( point.x, point.y, point.z );
	        
	        // un-rotate so the blob faces the camera
    	    glRotatef( -rotation.z, 0.0f, 0.0f, 1.0f );
            glRotatef( -rotation.y, 0.0f, 1.0f, 0.0f );
      	    glRotatef( -rotation.x, 1.0f, 0.0f, 0.0f );
      	    
      	    // render the sprite
	        Primitives.renderSprite( blobSize, blobSize, tex );
	        
	        glPopMatrix( );
	    }
	    
		version (ZOrdering) {
		    // sorry
		    int findFurthestPoint( ) {
		        int furthest = -1;
		        float furthestDist = -1;
	        
		        foreach ( i, point; points ) {
		            if ( distances[i] < 0 )
		                continue; // skip seen point
	            
		            if ( distances[i] > furthestDist ) {
		                furthestDist = distances[i];
		                furthest = i;
		            }
		        }
	        
		        assert( furthest != -1 );
	        
		        return furthest;
		    }
	    
		    // sorry
		    foreach ( i, point; points ) {
		        int furthest = findFurthestPoint( );
		        renderPoint( furthest );
		        distances[furthest] = -1;
		    }
		} else {
			glEnable( GL_BLEND );
			glBlendFunc(GL_SRC_ALPHA,GL_ONE);
			glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
			glHint(GL_POINT_SMOOTH_HINT,GL_NICEST);

			foreach ( i, point; points ) {
				renderPoint( i );
			}
		}
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
