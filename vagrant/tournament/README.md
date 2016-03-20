# Swiss Tournament Tracker

This python module is designed to help track the results of a Swiss tournament. It uses a PostgreSQL database backend to store and sort results. Python takes care of the rest.

## Getting Started
* Clone this repo
* [Install virtualbox] (https://www.virtualbox.org/wiki/Download_Old_Builds_4_3)
* [Install vagrant] (https://www.vagrantup.com/downloads.html)
* In the repo folder, run 'vagrant up' from a terminal/shell
* Once the vagrant machine is up and running, 'vagrant ssh'
* 'cd /vagrant/tournament'
* 'psql'
* '\\i tournament.sql'
* '\q'
* Make sure the tests pass: 'python tournament_test.py'
* If they do, go on ahead and use the python library, by importing tournament at the top of your own python script! If they don't, either fix it and file a pull request, or contact me!
