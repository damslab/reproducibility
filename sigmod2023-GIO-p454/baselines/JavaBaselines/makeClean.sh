#!/bin/bash

rm -rf target

#mvn clean package
mvn clean package -P distribution
