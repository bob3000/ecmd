# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "trusty64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/raring/current/trusty-server-cloudimg-vagrant-amd64-disk1.box"
  config.vm.host_name = "ecmd"
  config.vm.define :ecmd do |config|
    config.vm.synced_folder ".", "/home/vagrant/ecmd"
    config.vm.provision :puppet do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file = "ecmd.pp"
    end
  end
end
