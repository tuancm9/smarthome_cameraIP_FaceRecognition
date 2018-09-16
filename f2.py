from onvif import ONVIFCamera
import os
def perform_move(ptz, request, timeout):
    # Start continuous move
    ptz.ContinuousMove(request)
    # Wait a certain time
    sleep(timeout)
    # Stop continuous move
    ptz.Stop({'ProfileToken': request.ProfileToken})

# Set up camera - you'll need to change these as necessary
mycam = ONVIFCamera('192.168.1.100:554/onvif1', 5000, '', '')
# Create media service object
print "ok"
media = mycam.create_media_service()
# Create ptz service object
ptz = mycam.create_ptz_service()

# Get target profile
media_profile = media.GetProfiles()[0];

# Get PTZ configuration options for getting continuous move range
request = ptz.create_type('GetConfigurationOptions')
request.ConfigurationToken = media_profile.PTZConfiguration._token
ptz_configuration_options = ptz.GetConfigurationOptions(request)

request = ptz.create_type('ContinuousMove')
request.ProfileToken = media_profile._token

ptz.Stop({'ProfileToken': media_profile._token})


# THIS BIT IS MY GUESS!
request.Velocity.Zoom._x = 0.5
perform_move(ptz, request, 1)