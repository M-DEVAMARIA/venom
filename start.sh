if [ -z $BRANCH ]
then
  echo "Cloning main Repository"
  git clone https://github.com/M-DEVAMARIA/venom /venom  
else
  echo "Cloning $BRANCH branch from Repository "
  git clone https://github.com/M-DEVAMARIA/venom -b $BRANCH /venom 
fi
cd /venom
pip3 install -U -r requirements.txt
echo "Starting venom Bot ...."
python3 bot.py
