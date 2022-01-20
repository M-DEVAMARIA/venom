if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/M-DEVAMARIA/venom.git /venom
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /venom 
fi
cd /venom
pip3 install -U -r requirements.txt
echo "Starting venom Bot ...."
python3 bot.py
