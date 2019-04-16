#!/bin/bash
set -e

echo "This is travis-build.bash..."

echo "Installing the packages that CKAN requires..."
sudo apt-get update -qq
#sudo apt-get install postgresql-$PGVERSION solr-jetty libcommons-fileupload-java:amd64=1.2.2-1

# We need to install PostgreSQL v9.6. On Ubuntu 18.04 PostgreSQL v10 is the default version.
# Therefore we have adapted these instructions from this page
# https://wiki.postgresql.org/wiki/Apt
#sudo apt install curl ca-certificates
#curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
#sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main 9.6" > /etc/apt/sources.list.d/pgdg.list'
#sudo apt update
#sudo apt install postgresql-9.6 postgresql-server-dev-9.6

# Install Tomcat:
sudo apt-get install solr-tomcat

# Use this command to install the required packages:
sudo apt-get install python-dev  python-pip python-virtualenv git-core openjdk-8-jdk redis-server

echo "Installing CKAN and its Python dependencies..."
git clone https://github.com/aptivate/ckan
cd ckan
export ckan_branch=mapaction-dev
echo "CKAN branch: $ckan_branch"
git checkout $ckan_branch
python setup.py develop
pip install -r requirements.txt
pip install -r dev-requirements.txt 
cd -

echo "Creating the PostgreSQL user and database..."
sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'pass';"
sudo -u postgres psql -c 'CREATE DATABASE ckan_test WITH OWNER ckan_default;'

echo "Initialising the database..."
cd ckan
paster db init -c test-core.ini
cd -

echo "Installing ckanext-mapactiontheme and its requirements..."
python setup.py develop
pip install -r dev-requirements.txt

echo "Moving test.ini into a subdir..."
mkdir subdir
mv test.ini subdir

echo "travis-build.bash is done."
