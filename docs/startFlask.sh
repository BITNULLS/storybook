cd storybook
sudo nohup python3 -m edu_storybook.app > ../$(date +'%m-%d-%Y-%H-%M').log 2>&1 &
cd ..
