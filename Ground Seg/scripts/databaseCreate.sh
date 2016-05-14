#!/bin/bash 

read -r -p "This action will DELETE the fakeTelemetry table. Are you sure? [y/n]" response

reponse=${response,,} # response toLower
if [[ $response =~ ^(yes|y)$ ]]
then
    mysql -u root -pP0l@r3ubE -e "USE fakeSatellite;DROP TABLE IF EXISTS `fakeTelemetry`;"

    mysql -u root -pP0l@r3ubE -e "USE fakeSatellite;CREATE TABLE fakeTelemetry;"
else
    exit 1
fi

