# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "3scale/docker"

  config.vm.network "private_network", ip: "192.168.33.10"

  config.ssh.forward_agent = true

  config.vm.synced_folder ".", "/home/vagrant/mcrouter"
  
  config.vm.provider "virtualbox" do |v|
    v.memory = 4084
    v.cpus = 2
  end
end
