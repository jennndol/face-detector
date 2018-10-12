#!/usr/bin/env zsh
title1="tab 1"
title2="tab 2"
title3="tab 3"

cmd1="export WORKON_HOME=/home/luthfi/.virtualenvs && export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 && source /usr/local/bin/virtualenvwrapper.sh && workon cv && python socket-serv.py"
cmd2="export WORKON_HOME=/home/luthfi/.virtualenvs && export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 && source /usr/local/bin/virtualenvwrapper.sh && workon cv && python recognizer.py"
cmd3="live-server"

gnome-terminal --tab --title="$title1" --command="bash -c '$cmd1; $SHELL'" \
               --tab --title="$title2" --command="bash -c '$cmd2; $SHELL'" \
               --tab --title="$title3" --command="bash -c '$cmd3; $SHELL'"
