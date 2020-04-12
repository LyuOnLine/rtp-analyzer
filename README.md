**RTP-Analyzer**
---------
Python h264 RTP package inspector and analyzer.

### Usage:
- Step 0: Restore python virtual environment using pipenv
  
    ```
    pip3 install pipenv
    pipenv sync
    ```

- Step 1: dump rtp packets using gstreamer:

    ```
    gst-launch-1.0 -e -v rtspsrc location=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov debug=1 medias=0 ! multifilesink location=/tmp/rtp/%06d.dat
    ```
- Step 2: analyse dumped rtp packets
    
    ```
    pipenv run python test/test_rtp.py /tmp/rtp/*.dat |sort -n -k 8
    ```

    Output result is following:

    ```
    000000.dat : timestamp = 0 number = 1 payloadType = 97 type = STAP_A:[SPS,PPS,SEI,IFrame] size = 823
    000001.dat : timestamp = 22500 number = 7 payloadType = 97 type = PFrame size = 158
    000002.dat : timestamp = 41220 number = 12 payloadType = 97 type = PFrame size = 134
    000003.dat : timestamp = 52470 number = 15 payloadType = 97 type = PFrame size = 69
    000004.dat : timestamp = 67500 number = 19 payloadType = 97 type = PFrame size = 206
    ...
    ```
