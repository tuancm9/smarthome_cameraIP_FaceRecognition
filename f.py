from time import sleep

from onvif import ONVIFCamera

XMAX = 1
XMIN = -1
YMAX = 1
YMIN = -1

def perform_move(ptz, request, timeout):
    # Start continuous move
    ptz.ContinuousMove(request)
    # Wait a certain time
    sleep(timeout)
    # Stop continuous move
    ptz.Stop({'ProfileToken': request.ProfileToken})

def move_up(ptz, request, timeout=1):
    print 'move up...'
    request.Velocity.PanTilt._x = 0
    request.Velocity.PanTilt._y = YMAX
    perform_move(ptz, request, timeout)

def move_down(ptz, request, timeout=1):
    print 'move down...'
    request.Velocity.PanTilt._x = 0
    request.Velocity.PanTilt._y = YMIN
    perform_move(ptz, request, timeout)

def move_right(ptz, request, timeout=1):
    print 'move right...'
    request.Velocity.PanTilt._x = XMAX
    request.Velocity.PanTilt._y = 0
    perform_move(ptz, request, timeout)

def move_left(ptz, request, timeout=1):
    print 'move left...'
    request.Velocity.PanTilt._x = XMIN
    request.Velocity.PanTilt._y = 0
    perform_move(ptz, request, timeout)

def continuous_move():
    mycam = ONVIFCamera('rtsp://192.168.1.101:554/onvif1', 5000, 'admin', '123','/usr/local/lib/python2.7/dist-packages/onvif-0.2.0-py2.7.egg/wsdl/')
    # Create media service object
    resp = mycam.devicemgmt.GetHostname()
    print 'My camera`s hostname: ' + str(resp.Name)
    media = mycam.create_media_service()
    print "tao doi tuong..."
    # Create ptz service object
    ptz = mycam.create_ptz_service()
    print "tao doi project..."
    # Get target profile
    media_profile = media.GetProfiles()[0];
    print "tao profile.."
    # Get PTZ configuration options for getting continuous move range
    request = ptz.create_type('GetConfigurationOptions')
    print "tao conf.."
    request.ConfigurationToken = media_profile.PTZConfiguration._token
    ptz_configuration_options = ptz.GetConfigurationOptions(request)

    request = ptz.create_type('ContinuousMove')
    request.ProfileToken = media_profile._token

    ptz.Stop({'ProfileToken': media_profile._token})

    # Get range of pan and tilt
    # NOTE: X and Y are velocity vector
    global XMAX, XMIN, YMAX, YMIN
    XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
    XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
    YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
    YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min

    # move right
    print "right"
    move_right(ptz, request)
    print "left"
    # move left
    move_left(ptz, request)

    # Move up
    move_up(ptz, request)

    # move down
    move_down(ptz, request)

if __name__ == '__main__':
    continuous_move()