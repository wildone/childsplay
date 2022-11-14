## Install file to automate the installation of the program
#

# enable non-free repos
if [[ $(cat /etc/apt/sources.list.d/nonfree.list 2>/dev/null | grep "non-free rpi firmware") == "" ]]; then
cat << EOF | sudo tee /etc/apt/sources.list.d/nonfree.list
deb http://mirrordirector.raspbian.org/raspbian/ stretch main contrib non-free rpi firmware
EOF
fi

#install packages
sudo apt-get update --allow-releaseinfo-change && \
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
    python-pyaudio \
    python-pydub \
    omxplayer \
    espeak \
    python3-espeak \
    speech-dispatcher-espeak \
    alsa-base \
    alsa-tools \
    alsa-utils

python3 -m pip install omxplayer-wrapper ffmpeg-python pynput

#set headphone jack volume to 100%
amixer -c 1 sset Headphone 100%

#configure alsa
#update /usr/share/alsa/alsa.conf  with
#defaults.ctl.card 1
#defaults.pcm.card 1
#pcm.default cards.pcm.default
#pcm.sysdefault cards.pcm.default
#OR
cat config/.asoundrc > ~/.asoundrc
sudo cat config/.alsa > /usr/share/alsa/alsa.conf
if [[ $(sudo cat /etc/environment 2>/dev/null | grep "export PA_ALSA_PLUGHW=1") == "" ]]; then
sudo bash -c 'echo "export PA_ALSA_PLUGHW=1">/etc/environment'
fi

#disable all shortcuts
cp config/rc.xml ~/.config/openbox

#enable auto login, only once
if [[ $(cat /etc/lightdm/lightdm.conf 2>/dev/null | grep "autologin-user=pi") == "" ]]; then
cat << EOF | sudo tee /etc/lightdm/lightdm.conf
[SeatDefaults]
autologin-user=pi
# Prevent the screen from shutting off automatically.
xserver-command=X -s 0 dpms
EOF
fi


#setup app, only once
if [[ ! -d $HOME/.config/openbox ]]; then
    mkdir -p $HOME/.config/openbox
fi
if [[ $(cat $HOME/.config/openbox/autostart 2>/dev/null | grep "python3 -u $HOME/app.py") == "" ]]; then
cat << EOF > $HOME/.config/openbox/autostart
# redirect all output to a log file
# -u so that output is flushed immediately to the log
python3 -u $HOME/app.py > $HOME/app.log 2>&1 &
EOF
fi

#test
espeak "hello" --stdout | aplay --device=hw:1,0
omxplayer /usr/share/sounds/speech-dispatcher/dummy-message.wav
