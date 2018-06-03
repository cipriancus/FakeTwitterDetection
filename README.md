# Distributed Twitter News Identification using SVM, Naive Bayes and Random Forest

Using machine learning, a system capable of different tweet classification ( fake or not ) has been developed.

## Coordinators:
* Petru Rebeja petru.rebeja@gmail.com  
* Breaban Mihaela  pmihaela@info.uaic.ro
* Adrian Iftene adiftene@info.uaic.ro

## Students:
* Cușmuliuc Ciprian   cipriancus@gmail.com
* Coca Georgiana   cocageorgiana@gmail.com
* Groza Vasile   vasilegroza3@gmail.com

## OUR VM SETTINGS:
* 4 CPU cores
* 4 GB RAM
* SSD
* UBUNTU 16.04 LTS
* PYTHON 3 
* PYSPARK version 2.3.0
* Scala version 2.11.8
* OpenJDK 64-Bit Server VM, 1.8.0_171

## GOOGLE SETTINGS:
*  one DataProc cluster with three machines: one master and two slaves
*  master n1-standard-2 (2 vCPU, 7.50 GB memory)
*  worker n1-standard-4 (4 vCPU, 15.0 GB memory)
*  disk 500 GB
*  UBUNTU 16.04 LTS
*  PYTHON 3 
*  PYSPARK version 2.3.0
*  Scala version 2.11.8
*  OpenJDK 64-Bit Server VM, 1.8.0_171

* we also tested with 10 workers and very high hardware resources but the results were about the same, no noticeable improvement

## Introduction

Today, using Facebook and Twitter for news information is something usual, users from these networks create a lot of content: posts (with text, images, videos, links), comments, likes, but also redistribution of information with retweet option or with simple copy/paste operations thus a common problem is the detection of fake users or fake news. The present work aims to analyze different techniques of detecting fake news, their performance and how we can do fine tuning in order to improve the actual results.


