if [ -z $BRANCH ]
then
  echo "Cloning main Repository"
  git clone https://github.com/M-DEVAMARIA/venom /venom  
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone https://github.com/M-DEVAMARIA/venom -b $BRANCH /venom 
fi
cd /venom
pip3 install -U -r requirements.txt
echo "Starting venom Bot ...."
python3 bot.py
