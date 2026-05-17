
echo 'Installing uhubctl'
# sudo apt install uhubctl

echo 'Giving permissions to run uhubctl without root'
# https://github.com/mvp/uhubctl#linux-usb-permissions
sudo tee /etc/udev/rules.d/52-uhubctl.rules << 'EOF'
# Grant permissions for the Pi 3B USB Controller and Internal Hub
SUBSYSTEM=="usb", ATTR{idVendor}=="0424", ATTR{idProduct}=="9514", MODE="0664", GROUP="dialout"
SUBSYSTEM=="usb", ATTR{idVendor}=="0424", ATTR{idProduct}=="ec00", MODE="0664", GROUP="dialout"
EOF

echo 'Checking the changes to udev rules are valid'
sudo udevadm control --reload-rules && sudo udevadm trigger

echo 'Adding user to dialout group (now with access to control USB)'
sudo usermod -a -G dialout $USER

echo 'Restarting USB subsystem for changes to take effect (or reboot)'
sudo udevadm trigger --attr-match=subsystem=usb
