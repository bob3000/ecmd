Exec {
    path => "/bin:/usr/bin:/sbin:/usr/sbin",
    user => "root",
    logoutput => on_failure,
}

Package {
    ensure => "latest",
    require => Exec["update"],
}

class base {
    exec { "update":
        command => "apt-get update && touch /root/.updated",
        creates => "/root/.updated",
    }

    file { "/home/vagrant/.bash_login":
        content => "
        alias ecmd='PYTHONPATH=/home/vagrant/ecmd/ python3 -m ecmd'
        cd /home/vagrant/ecmd
        ",
    }

    file { "/usr/share/bash-completion/completions/ecmd":
        ensure => "link",
        target => "/home/vagrant/ecmd/completion/ecmd",
    }

    file { "/usr/share/man/man1/ecmd.1":
        ensure => "link",
        target => "/home/vagrant/ecmd/man/ecmd.1",
    }

    # basic dependencies
    package { "python3": }
    package { "python-dev": }
    package { "python3-setuptools": }
    package { "pep8": }
    package { "python3-flake8": }

    # install coverage
    exec { "easy_install3 coverage":
        creates => "/usr/local/bin/coverage3",
        require => [
            Package["python-dev"],
        Package["python3"],
        Package["python3-setuptools"],
        ]
    }
}

class {"base":}
