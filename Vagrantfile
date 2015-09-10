# -*- mode: ruby -*-
# vi: set ft=ruby :

# This Vagranfile produces a VM with heroku-toolbelt ready to go.
# It opens up port 5000 from inside the guest VM machine, and binds
# it to port 8080 of the host os.
# To use heroku, do a 'vagrant ssh' and start hacking.

Vagrant.configure(2) do |config|
  config.vm.box = "janihur/ubuntu-1404-desktop"
  config.vm.network "forwarded_port", guest: 5000, host: 8080
  config.vm.synced_folder "src", "/home/vagrant/src"
  config.vm.provider "virtualbox" do |vb|
    vb.gui = true
    vb.memory = "1024"
  end

  # Provisioning
  $script = <<-SHELL
# Heroku toolbelt dependencies
sudo apt-get install -y python python-pip python-virtualenv

# Heroku toolbelt
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
sudo apt-get install -y heroku-toolbelt

SHELL
  config.vm.provision "shell", inline: $script
end
