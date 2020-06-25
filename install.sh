
# enable non-free repos
cat << EOF | sudo tee /etc/apt/sources.list.d/nonfree.list
deb http://mirrordirector.raspbian.org/raspbian/ stretch main contrib non-free rpi firmware
EOF

#install packages
sudo apt-get update && \
sudo apt-get install --no-install-recommends -y \
    sudo \
    cmake \
    xorg \
    openbox \
    lightdm \
    python3 \
    python3-tk \
    python3-rpi.gpio \
    xserver-xorg-legacy \
    xserver-xorg-video-fbdev \
    python3-pip \
    python3-evdev \
    inotify-tools \
    ffmpeg \
    ffmpeg-python \
    python-pyaudio \
    python-pydub \
    omxplayer \
    espeak \
    python3-espeak \
    speech-dispatcher-espeak \
    alsa-base \
    alsa-tools \
    alsa-utils \
    omxplayer-wrapper \
    jackd2

#set audio to use headphone jack, 2=hdmi
amixer -c 1


#configure alsa
#update /usr/share/alsa/alsa.conf  with
#defaults.ctl.card 1
#defaults.pcm.card 1
#pcm.default cards.pcm.default
#pcm.sysdefault cards.pcm.default
#OR
cat config/.asoundrc > ~/.asoundrc
cat config/.alsa > /usr/share/alsa/alsa.conf
echo "export PA_ALSA_PLUGHW=1">/etc/environment

#disable all shortcuts
cp config/rc.xml ~/.config/openbox


#enable auto login
cat << EOF | sudo tee /etc/lightdm/lightdm.conf
[SeatDefaults]
autologin-user=pi
# Prevent the screen from shutting off automatically.
xserver-command=X -s 0 dpms
EOF



#setup app

mkdir -p $HOME/.config/openbox

cat << EOF > $HOME/.config/openbox/autostart
# redirect all output to a log file
# -u so that output is flushed immediately to the log
python3 -u $HOME/app.py > $HOME/app.log 2>&1 &
EOF
